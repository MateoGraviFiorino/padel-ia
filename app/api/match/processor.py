import os
import datetime
import re

import urllib

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Request
from fastapi.responses import FileResponse, StreamingResponse, Response
from pathlib import Path
import cv2
from app.match import PadelMatchProcessor
from .video_response import UploadVideoResponse
from app.match import PadelMatchProcessor

match_router = APIRouter(prefix="/match", tags=["match"])


def get_match_processor() -> PadelMatchProcessor:
    return PadelMatchProcessor()


VIDEOS_DIR = Path("videos")
VIDEOS_DIR.mkdir(parents=True, exist_ok=True)


@match_router.post("/upload-video", response_model=UploadVideoResponse)
async def upload_and_process_video(
    file: UploadFile = File(...),
    match_processor: PadelMatchProcessor = Depends(get_match_processor)
) -> UploadVideoResponse:
    input_path = VIDEOS_DIR / file.filename
    with open(input_path, "wb") as buffer:
        buffer.write(await file.read())

    # separar nombre y extensión
    base_name, ext = os.path.splitext(file.filename)

    # evitar duplicar el sufijo _h264
    if base_name.endswith("_h264"):
        base_name = base_name[:-5]

    processed_video_filename = f"processed_{base_name}_h264{ext}"
    output_path = str(VIDEOS_DIR / processed_video_filename)

    final_stats = match_processor.process_video_with_output(
        str(input_path),
        output_path=output_path
    )

    return UploadVideoResponse(
        total_hits=final_stats.total_hits,
        hits_per_player=final_stats.hits_per_player,
        total_frames=final_stats.total_frames,
        video_duration=final_stats.video_duration,
        fps=final_stats.fps,
        filename=file.filename,
        message="Video procesado exitosamente",
        processed_video_path=output_path,
        processed_video_filename=processed_video_filename
    )


@match_router.get("/download-processed-video/{filename}")
async def download_processed_video(filename: str):
    decoded_filename = urllib.parse.unquote(filename)
    file_path = VIDEOS_DIR / decoded_filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Video procesado no encontrado")

    return FileResponse(
        file_path,
        media_type="video/mp4",
        filename=decoded_filename
    )


@match_router.post("/generate-report")
async def generate_report(stats: dict):
    """Endpoint para generar reporte profesional con ChatGPT"""

    total_hits = stats.get('total_hits', 0)
    video_duration = stats.get('video_duration', 0)
    fps = stats.get('fps', 0)
    total_frames = stats.get('total_frames', 0)
    hits_per_player = stats.get('hits_per_player', {})
    filename = stats.get('filename', 'partido')

    duration_minutes = video_duration / 60 if video_duration > 0 else 0
    hits_per_minute = (total_hits / duration_minutes) if duration_minutes > 0 else 0
    intensity_level = "Alto" if hits_per_minute > 30 else "Medio" if hits_per_minute > 15 else "Bajo"

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
- **Eficiencia de detección**: {(total_hits / total_frames * 100 if total_frames>0 else 0):.1f}% de frames con actividad
- **Promedio de golpes por frame**: {(total_hits / total_frames if total_frames>0 else 0):.2f}

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
