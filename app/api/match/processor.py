import os
import base64
import datetime
import shutil

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse, StreamingResponse
from pathlib import Path
import tempfile
from app.match import PadelMatchProcessor
from .video_response import UploadVideoResponse
from app.match import PadelMatchProcessor

match_router = APIRouter(prefix="/match", tags=["match"])

def get_match_processor() -> PadelMatchProcessor:
    return PadelMatchProcessor()

@match_router.post("/upload-video", response_model=UploadVideoResponse)
async def upload_and_process_video(
    file: UploadFile = File(...),
    match_processor: PadelMatchProcessor = Depends(get_match_processor)
) -> UploadVideoResponse:
    # Validar tipo de archivo
    if not file.content_type.startswith('video/'):
        raise HTTPException(status_code=400, detail="Solo se permiten archivos de video")

    # Crear archivo temporal para el video original
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.filename.split('.')[-1]}") as temp_file:
        content = await file.read()
        temp_file.write(content)
        temp_file_path = temp_file.name

    # Preparar nombres y directorios
    base_name = file.filename
    for ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']:
        if base_name.endswith(ext):
            base_name = base_name.replace(ext, '')
            break

    import uuid
    video_id = str(uuid.uuid4())[:8]
    temp_dir = os.path.join(tempfile.gettempdir(), f"padel_video_{video_id}")
    os.makedirs(temp_dir, exist_ok=True)

    processed_video_path = os.path.join(temp_dir, f"{base_name}_{video_id}_processed.mp4")

    print(f"🎬 Procesando video: {file.filename}")
    print(f"📁 Archivo temporal original: {temp_file_path}")
    print(f"🎯 Archivo procesado destino: {processed_video_path}")
    print(f"📂 Directorio temporal: {temp_dir}")

    try:
        # Procesar el video UNA SOLA VEZ para obtener estadísticas y generar video procesado
        print("🎬 Procesando video completo (estadísticas + video procesado)...")
        final_stats = match_processor.process_video_with_output(
            temp_file_path,
            output_path=processed_video_path
        )

        print("✅ Video procesado generado exitosamente")

        # Si el match_processor actualizó la ruta, úsala
        actual_processed_path = getattr(final_stats, 'processed_video_path', None)
        if actual_processed_path and os.path.exists(actual_processed_path):
            processed_video_path = actual_processed_path
            print(f"🔄 Ruta actualizada del video procesado: {processed_video_path}")

        # Buscar mejor candidato final en el directorio (prefiere _h264, luego _reencoded, luego _processed)
        candidate = None
        if os.path.isdir(temp_dir):
            files = os.listdir(temp_dir)
            # Preferencia de nombres
            for pattern in ['_h264.mp4', '_reencoded_', '_processed.mp4']:
                for f in files:
                    if f.endswith('.mp4') and (pattern in f or f.endswith(pattern)):
                        candidate = os.path.join(temp_dir, f)
                        break
                if candidate:
                    break

        if candidate and os.path.exists(candidate):
            processed_video_path = candidate

        # Verificar que el video procesado se creó
        if os.path.exists(processed_video_path):
            file_size = os.path.getsize(processed_video_path)
            print(f"✅ Video procesado creado exitosamente: {processed_video_path}")
            print(f"📊 Tamaño del archivo: {file_size} bytes")
        else:
            print("❌ Error: No se pudo generar el video procesado")
            processed_video_path = None

        print(f"🏓 Estadísticas finales:")
        print(f"   - Total de golpes: {final_stats.total_hits}")
        print(f"   - Golpes por jugador: {final_stats.hits_per_player}")
        print(f"   - Duración: {final_stats.video_duration:.2f}s")
        print(f"   - FPS: {final_stats.fps:.2f}")

        final_path = processed_video_path
        processed_video_filename = os.path.basename(final_path) if final_path else None

        return UploadVideoResponse(
            total_hits=final_stats.total_hits,
            hits_per_player=final_stats.hits_per_player,
            total_frames=final_stats.total_frames,
            video_duration=final_stats.video_duration,
            fps=final_stats.fps,
            filename=file.filename,
            message="Video procesado exitosamente",
            processed_video_path=final_path,
            processed_video_filename=processed_video_filename
        )
    finally:
        # Limpiar archivo temporal original
        try:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                print(f"🗑️ Archivo temporal original eliminado: {temp_file_path}")
        except Exception:
            pass

@match_router.get("/download-processed-video/{filename}")
async def download_processed_video(filename: str):
    """Endpoint para descargar el video procesado con inferencias"""
    try:
        # Decodificar el nombre del archivo (por si tiene caracteres especiales)
        import urllib.parse
        decoded_filename = urllib.parse.unquote(filename)
        
        print(f"🔍 Buscando video procesado para: {decoded_filename}")
        
        # Buscar en directorios temporales de padel
        temp_dir = tempfile.gettempdir()
        possible_paths = []
        
        # Buscar en directorios temporales específicos de padel
        for item in os.listdir(temp_dir):
            if item.startswith("padel_video_"):
                padel_dir = os.path.join(temp_dir, item)
                if os.path.isdir(padel_dir):
                    # Buscar archivos procesados en este directorio
                    for file_item in os.listdir(padel_dir):
                        if file_item.endswith(("_processed.mp4", "_processed.avi")):
                            # Verificar si coincide con el nombre del archivo
                            base_name = decoded_filename
                            for ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']:
                                if base_name.endswith(ext):
                                    base_name = base_name.replace(ext, '')
                                    break
                            
                            if file_item.startswith(base_name):
                                possible_paths.append(os.path.join(padel_dir, file_item))
        
        # Si no se encuentra, buscar en el directorio temporal general
        if not possible_paths:
            for ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']:
                if decoded_filename.endswith(ext):
                    base_name = decoded_filename.replace(ext, '')
                    processed_path = os.path.join(temp_dir, f"{base_name}_processed.mp4")
                    if os.path.exists(processed_path):
                        possible_paths.append(processed_path)
                    break
        
        print(f"📁 Directorio temporal: {temp_dir}")
        print(f"🔍 Rutas posibles encontradas: {possible_paths}")
        
        if possible_paths:
            processed_video_path = possible_paths[0]
            print(f"✅ Video encontrado en: {processed_video_path}")
            print(f"📊 Tamaño del archivo: {os.path.getsize(processed_video_path)} bytes")
            
            return FileResponse(
                processed_video_path, 
                media_type='video/mp4',
                filename=f"{os.path.basename(processed_video_path)}"
            )
        else:
            print(f"❌ No se encontró video procesado para: {decoded_filename}")
            # Listar archivos en directorios temporales para debug
            padel_dirs = [d for d in os.listdir(temp_dir) if d.startswith("padel_video_")]
            print(f"📁 Directorios temporales de padel: {padel_dirs}")
            
            for padel_dir in padel_dirs[:3]:  # Solo mostrar los primeros 3
                full_path = os.path.join(temp_dir, padel_dir)
                if os.path.isdir(full_path):
                    files = os.listdir(full_path)
                    print(f"📂 Archivos en {padel_dir}: {files}")
            
            raise HTTPException(
                status_code=404, 
                detail=f"Video procesado no encontrado para: {decoded_filename}"
            )
            
    except Exception as e:
        print(f"❌ Error en download-processed-video: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error descargando video: {str(e)}")


@match_router.get("/stream-processed-video/{filename}")
async def stream_processed_video(filename: str):
    """Endpoint para streaming del video procesado (reproducción en navegador)"""
    try:
        # Decodificar el nombre del archivo
        import urllib.parse
        decoded_filename = urllib.parse.unquote(filename)
        
        print(f"🎥 Streaming video procesado para: {decoded_filename}")
        
        # Buscar en directorios temporales de padel
        temp_dir = tempfile.gettempdir()
        possible_paths = []
        
        # Buscar en directorios temporales específicos de padel
        for item in os.listdir(temp_dir):
            if item.startswith("padel_video_"):
                padel_dir = os.path.join(temp_dir, item)
                if os.path.isdir(padel_dir):
                    # Buscar archivos procesados en este directorio
                    for file_item in os.listdir(padel_dir):
                        if file_item.endswith(("_processed.mp4", "_processed.avi")):
                            # Verificar si coincide con el nombre del archivo
                            base_name = decoded_filename
                            for ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']:
                                if base_name.endswith(ext):
                                    base_name = base_name.replace(ext, '')
                                    break
                            
                            if file_item.startswith(base_name):
                                possible_paths.append(os.path.join(padel_dir, file_item))
        
        if possible_paths:
            processed_video_path = possible_paths[0]
            print(f"✅ Video encontrado para streaming: {processed_video_path}")
            
            # Verificar que el archivo existe y tiene tamaño adecuado
            if os.path.exists(processed_video_path) and os.path.getsize(processed_video_path) > 1000:
                # Usar StreamingResponse para mejor compatibilidad con navegadores
                from fastapi.responses import StreamingResponse
                
                # Determinar media type según extensión
                file_extension = os.path.splitext(processed_video_path)[1].lower()
                media_type = 'video/mp4' if file_extension == '.mp4' else 'video/x-msvideo'
                
                # Para MP4, usar FileResponse que es más eficiente
                if file_extension == '.mp4':
                    from fastapi.responses import FileResponse
                    return FileResponse(
                        processed_video_path,
                        media_type='video/mp4',
                        headers={
                            'Accept-Ranges': 'bytes',
                            'Content-Disposition': f'inline; filename="{os.path.basename(processed_video_path)}"',
                            'Cache-Control': 'no-cache, no-store, must-revalidate',
                            'Pragma': 'no-cache',
                            'Expires': '0',
                            'Access-Control-Allow-Origin': '*',
                            'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
                            'Access-Control-Allow-Headers': 'Range, Accept, Accept-Encoding, Accept-Language, Cache-Control, Connection, Host, If-Modified-Since, If-None-Match, If-Range, Range, Referer, User-Agent',
                            'Access-Control-Expose-Headers': 'Content-Length, Content-Range, Accept-Ranges',
                            'X-Content-Type-Options': 'nosniff',
                            'X-Frame-Options': 'SAMEORIGIN'
                        }
                    )
                
                # Para otros formatos, usar StreamingResponse
                def video_stream():
                    with open(processed_video_path, 'rb') as video_file:
                        while True:
                            chunk = video_file.read(8192)  # 8KB chunks
                            if not chunk:
                                break
                            yield chunk
                
                return StreamingResponse(
                    video_stream(),
                    media_type=media_type,
                    headers={
                        'Accept-Ranges': 'bytes',
                        'Content-Disposition': f'inline; filename="{os.path.basename(processed_video_path)}"',
                        'Cache-Control': 'no-cache, no-store, must-revalidate',
                        'Pragma': 'no-cache',
                        'Expires': '0',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
                        'Access-Control-Allow-Headers': 'Range, Accept, Accept-Encoding, Accept-Language, Cache-Control, Connection, Host, If-Modified-Since, If-None-Match, If-Range, Range, Referer, User-Agent',
                        'Access-Control-Expose-Headers': 'Content-Length, Content-Range, Accept-Ranges',
                        'X-Content-Type-Options': 'nosniff',
                        'X-Frame-Options': 'SAMEORIGIN'
                    }
                )
            else:
                raise HTTPException(
                    status_code=404, 
                    detail="Video procesado no válido o muy pequeño"
                )
        else:
            raise HTTPException(
                status_code=404, 
                detail=f"Video procesado no encontrado para: {decoded_filename}"
            )
            
    except Exception as e:
        print(f"❌ Error en stream-processed-video: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error streaming video: {str(e)}")


@match_router.get("/stream-frames/{filename}")
async def stream_frames(filename: str):
    """Endpoint MJPEG que transmite frames anotados como multipart/x-mixed-replace (compatible con <img src=>)."""
    try:
        import urllib.parse
        decoded_filename = urllib.parse.unquote(filename)
        print(f"🎥 MJPEG stream para: {decoded_filename}")

        temp_dir = tempfile.gettempdir()
        possible_paths = []
        for item in os.listdir(temp_dir):
            if item.startswith("padel_video_"):
                padel_dir = os.path.join(temp_dir, item)
                if os.path.isdir(padel_dir):
                    for file_item in os.listdir(padel_dir):
                        if file_item.endswith('.mp4') or file_item.endswith('.avi'):
                            base_name = decoded_filename
                            for ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']:
                                if base_name.endswith(ext):
                                    base_name = base_name.replace(ext, '')
                                    break
                            if file_item.startswith(base_name):
                                possible_paths.append(os.path.join(padel_dir, file_item))

        if not possible_paths:
            raise HTTPException(status_code=404, detail=f"Video procesado no encontrado para: {decoded_filename}")

        processed_video_path = possible_paths[0]
        print(f"✅ Video MJPEG encontrado: {processed_video_path}")

        # Generador de frames JPEG
        def frame_generator():
            import cv2
            cap = cv2.VideoCapture(processed_video_path)
            try:
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    # Encode JPEG
                    ok, jpg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
                    if not ok:
                        continue
                    chunk = jpg.tobytes()
                    yield (b"--frame\r\n"
                           b"Content-Type: image/jpeg\r\n\r\n" + chunk + b"\r\n")
            finally:
                try:
                    cap.release()
                except Exception:
                    pass

        return StreamingResponse(frame_generator(), media_type='multipart/x-mixed-replace; boundary=frame')

    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error en stream-frames: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error streaming frames: {str(e)}")


@match_router.head("/stream-processed-video/{filename}")
async def head_processed_video(filename: str):
    """Endpoint HEAD para verificar el video procesado"""
    try:
        # Decodificar el nombre del archivo
        import urllib.parse
        decoded_filename = urllib.parse.unquote(filename)
        
        # Buscar en directorios temporales de padel
        temp_dir = tempfile.gettempdir()
        possible_paths = []
        
        # Buscar en directorios temporales específicos de padel
        for item in os.listdir(temp_dir):
            if item.startswith("padel_video_"):
                padel_dir = os.path.join(temp_dir, item)
                if os.path.isdir(padel_dir):
                    # Buscar archivos procesados en este directorio
                    for file_item in os.listdir(padel_dir):
                        if file_item.endswith(("_processed.mp4", "_processed.avi")):
                            # Verificar si coincide con el nombre del archivo
                            base_name = decoded_filename
                            for ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']:
                                if base_name.endswith(ext):
                                    base_name = base_name.replace(ext, '')
                                    break
                            
                            if file_item.startswith(base_name):
                                possible_paths.append(os.path.join(padel_dir, file_item))
        
        if possible_paths:
            processed_video_path = possible_paths[0]
            
            # Verificar que el archivo existe y tiene tamaño adecuado
            if os.path.exists(processed_video_path) and os.path.getsize(processed_video_path) > 1000:
                file_size = os.path.getsize(processed_video_path)
                
                from fastapi.responses import Response
                return Response(
                    status_code=200,
                    headers={
                        'Content-Type': 'video/mp4',
                        'Content-Length': str(file_size),
                        'Accept-Ranges': 'bytes',
                        'Content-Disposition': f'inline; filename="{os.path.basename(processed_video_path)}"',
                        'Cache-Control': 'no-cache',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'GET, HEAD',
                        'Access-Control-Allow-Headers': 'Range'
                    }
                )
            else:
                raise HTTPException(status_code=404, detail="Video procesado no válido")
        else:
            raise HTTPException(status_code=404, detail="Video procesado no encontrado")
            
    except Exception as e:
        print(f"❌ Error en HEAD video: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error verificando video: {str(e)}")


@match_router.options("/stream-processed-video/{filename}")
async def options_processed_video(filename: str):
    """Endpoint OPTIONS para CORS preflight"""
    from fastapi.responses import Response
    return Response(
        status_code=200,
        headers={
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
            'Access-Control-Allow-Headers': 'Range, Accept, Accept-Encoding, Accept-Language, Cache-Control, Connection, Host, If-Modified-Since, If-None-Match, If-Range, Range, Referer, User-Agent',
            'Access-Control-Expose-Headers': 'Content-Length, Content-Range, Accept-Ranges',
            'Access-Control-Max-Age': '86400',  # 24 horas
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'SAMEORIGIN'
        }
    )


@match_router.post("/generate-report")
async def generate_report(stats: dict):
    """Endpoint para generar reporte profesional con ChatGPT"""
    try:
        # Validar datos de entrada
        if not stats or not isinstance(stats, dict):
            raise HTTPException(status_code=400, detail="Datos de estadísticas inválidos")
        
        # Extraer estadísticas con valores por defecto seguros
        total_hits = stats.get('total_hits', 0)
        video_duration = stats.get('video_duration', 0)
        fps = stats.get('fps', 0)
        total_frames = stats.get('total_frames', 0)
        hits_per_player = stats.get('hits_per_player', {})
        filename = stats.get('filename', 'partido')
        
        # Calcular métricas adicionales
        duration_minutes = video_duration / 60 if video_duration > 0 else 0
        hits_per_minute = (total_hits / duration_minutes) if duration_minutes > 0 else 0
        intensity_level = "Alto" if hits_per_minute > 30 else "Medio" if hits_per_minute > 15 else "Bajo"
        
        # Generar reporte profesional en Markdown
        report = f"""# 🎾 Reporte de Análisis de Partido de Padel

## 📊 Resumen Ejecutivo

Se analizó exitosamente un partido de padel con tecnología de Inteligencia Artificial, 
procesando {total_frames:,} frames a {fps:.1f} FPS para una duración total de {duration_minutes:.1f} minutos.

## 🏓 Estadísticas Principales

| Métrica | Valor |
|---------|-------|
| **Total de Golpes Detectados** | {total_hits:,} |
| **Duración del Partido** | {duration_minutes:.1f} minutos |
| **Golpes por Minuto** | {hits_per_minute:.1f} |
| **Nivel de Intensidad** | {intensity_level} |
| **Calidad del Video** | {fps:.1f} FPS |

## 👥 Rendimiento por Jugador

"""
        
        # Agregar estadísticas por jugador
        if hits_per_player:
            for player, hits in hits_per_player.items():
                player_percentage = (hits / total_hits * 100) if total_hits > 0 else 0
                report += f"- **{player}**: {hits:,} golpes ({player_percentage:.1f}% del total)\n"
        else:
            report += "- No se detectaron jugadores específicos\n"
        
        report += f"""
## 📈 Análisis de Rendimiento

### Intensidad del Juego
El partido muestra un nivel de intensidad **{intensity_level.lower()}** con {hits_per_minute:.1f} golpes por minuto.

### Distribución de Golpes
- **Total de frames analizados**: {total_frames:,}
- **Eficiencia de detección**: {(total_hits / total_frames * 100):.1f}% de frames con actividad
- **Promedio de golpes por frame**: {(total_hits / total_frames):.2f}

## 🎯 Recomendaciones Técnicas

### Para Mejorar el Juego
1. **Consistencia**: Mantener un ritmo constante de {hits_per_minute:.1f} golpes por minuto
2. **Técnica**: Enfocarse en la precisión más que en la velocidad
3. **Estrategia**: Analizar patrones de juego para optimizar posicionamiento

### Para Futuros Análisis
- Grabar en resolución HD o superior para mejor detección
- Mantener la cámara estable durante la grabación
- Asegurar buena iluminación para detección óptima

## 🔬 Metodología del Análisis

Este reporte fue generado utilizando:
- **Detección de Jugadores**: Modelo YOLO optimizado para personas
- **Detección de Pelota**: IA especializada en objetos deportivos
- **Análisis de Golpes**: Algoritmo de proximidad y movimiento
- **Procesamiento de Video**: Análisis frame por frame con IA

## 📅 Información del Archivo

- **Nombre del archivo**: {filename}
- **Fecha de análisis**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Duración del análisis**: {video_duration:.1f} segundos
- **Calidad del análisis**: {'Alta' if fps >= 25 else 'Media' if fps >= 15 else 'Baja'}

---

*Reporte generado automáticamente por PadelAI - Análisis Inteligente de Padel*
"""
        
        return {
            "report": report,
            "filename": f"reporte_padel_{filename.replace(' ', '_').replace('.', '_')}.md",
            "metadata": {
                "total_hits": total_hits,
                "duration_minutes": duration_minutes,
                "hits_per_minute": hits_per_minute,
                "intensity_level": intensity_level,
                "generated_at": datetime.datetime.now().isoformat()
            }
        }
        
    except Exception as e:
        print(f"❌ Error generando reporte: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error generando reporte: {str(e)}")
