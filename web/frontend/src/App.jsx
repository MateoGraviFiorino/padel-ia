import React, { useState } from "react";

function App() {
  const [matchData, setMatchData] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState(null);
  const [isGeneratingReport, setIsGeneratingReport] = useState(false);
  const [report, setReport] = useState(null);
  const [processedVideoUrl, setProcessedVideoUrl] = useState(null);
  const [useMjpegFallback, setUseMjpegFallback] = useState(false);

  // Función para renderizar Markdown a HTML
  const renderMarkdown = (markdown) => {
    if (!markdown) return '';
    
    // Convertir Markdown básico a HTML
    let html = markdown
      // Headers
      .replace(/^### (.*$)/gim, '<h3 class="text-xl font-semibold text-white mb-3">$1</h3>')
      .replace(/^## (.*$)/gim, '<h2 class="text-2xl font-bold text-white mb-4 mt-6">$1</h2>')
      .replace(/^# (.*$)/gim, '<h1 class="text-3xl font-bold text-white mb-6">$1</h1>')
      
      // Listas
      .replace(/^\* (.*$)/gim, '<li class="text-gray-300 mb-1">$1</li>')
      .replace(/^- (.*$)/gim, '<li class="text-gray-300 mb-1">$1</li>')
      .replace(/^1\. (.*$)/gim, '<li class="text-gray-300 mb-1">$1</li>')
      
      // Negrita e itálica
      .replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-white">$1</strong>')
      .replace(/\*(.*?)\*/g, '<em class="italic text-gray-300">$1</em>')
      
      // Enlaces
      .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-blue-400 hover:text-blue-300 underline">$1</a>')
      
      // Código inline
      .replace(/`([^`]+)`/g, '<code class="bg-gray-800 px-2 py-1 rounded text-green-400 font-mono">$1</code>')
      
      // Líneas horizontales
      .replace(/^---$/gim, '<hr class="border-gray-600 my-6">')
      
      // Párrafos
      .replace(/\n\n/g, '</p><p class="text-gray-300 mb-4">')
      .replace(/\n/g, '<br>');
    
    // Envolver en párrafo si no hay headers
    if (!html.includes('<h')) {
      html = `<p class="text-gray-300 mb-4">${html}</p>`;
    }
    
    // Envolver listas
    html = html.replace(/(<li.*<\/li>)/g, '<ul class="list-disc list-inside text-gray-300 mb-4">$1</ul>');
    
    return html;
  };

  // Función para llamar a tu API de FastAPI
  const callPadelAPI = async (file, onProgress) => {
    try {
      // Validar archivo
      if (!file.type.startsWith('video/')) {
        throw new Error(`Tipo de archivo no soportado. Solo se permiten archivos de video.`);
      }
      
      if (file.size > 100 * 1024 * 1024) {
        throw new Error(`Archivo demasiado grande. Tamaño máximo: 100MB`);
      }

      const formData = new FormData();
      formData.append('file', file);

      // Progreso inicial
      onProgress(10);

      console.log('🎬 Intentando conectar con la API en: http://localhost:8000/match/upload-video');
      console.log('📁 Archivo a enviar:', file.name, 'Tamaño:', file.size, 'bytes');

      // Llamar a tu endpoint de FastAPI
      const response = await fetch('http://localhost:8000/match/upload-video', {
        method: 'POST',
        body: formData,
        // Agregar headers para evitar problemas de CORS
        headers: {
          'Accept': 'application/json',
        },
      });

      console.log('📡 Respuesta de la API:', response.status, response.statusText);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `Error HTTP: ${response.status} - ${response.statusText}`);
      }

      onProgress(100);
      const result = await response.json();
      console.log('✅ Resultado de la API:', result);
      return result;
      
    } catch (error) {
      console.error('❌ Error detallado al procesar el video:', error);
      
      // Mensajes de error más específicos
      if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
        throw new Error('No se pudo conectar con el servidor. Verifica que tu backend de FastAPI esté ejecutándose en http://localhost:8000');
      }
      
      if (error.message.includes('CORS')) {
        throw new Error('Error de CORS. El servidor no permite conexiones desde este origen.');
      }
      
      throw error;
    }
  };

  // Función para generar reporte con ChatGPT
  const generateReport = async () => {
    if (!matchData) return;

    setIsGeneratingReport(true);
    try {
      const response = await fetch('http://localhost:8000/match/generate-report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(matchData),
      });

      if (!response.ok) {
        throw new Error('Error generando reporte');
      }

      const reportData = await response.json();
      setReport(reportData);
    } catch (error) {
      console.error('Error generando reporte:', error);
      setError('Error generando reporte. Por favor intenta de nuevo.');
    } finally {
      setIsGeneratingReport(false);
    }
  };

  // Función para descargar reporte
  const downloadReport = () => {
    if (!report) return;

    const blob = new Blob([report.report], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = report.filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleFileUpload = async (file) => {
    if (!file) return;

    // Validar tipo de archivo
    if (!file.type.startsWith('video/')) {
      setError('Por favor selecciona un archivo de video válido');
      return;
    }

    // Validar tamaño (100MB máximo)
    if (file.size > 100 * 1024 * 1024) {
      setError('El archivo es demasiado grande. Tamaño máximo: 100MB');
      return;
    }

    try {
      setIsProcessing(true);
      setError(null);
      setUploadProgress(10);
      setReport(null);
      setProcessedVideoUrl(null);

      // Llamar a tu función real de análisis
      const result = await callPadelAPI(file, setUploadProgress);
      
      // Procesar los resultados
      setMatchData(result);
      setIsProcessing(false);
      setUploadProgress(0);
      
      // Si hay video procesado, crear URL para mostrarlo
      if (result.processed_video_filename) {
        // Usar el nombre real del archivo procesado devuelto por el backend
        const videoUrl = `http://localhost:8000/videos/${encodeURIComponent(result.processed_video_filename)}`;
        setProcessedVideoUrl(videoUrl);
      }
      
    } catch (error) {
      console.error('Error al procesar el video:', error);
      setError(error.message || 'Error al procesar el video. Por favor intenta de nuevo.');
      setIsProcessing(false);
      setUploadProgress(0);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-7xl mx-auto px-6">
        {/* Header */}
        <div className="text-center py-20">
          <h1 className="text-6xl font-bold mb-6 text-green-400">PadelAI</h1>
          <p className="text-2xl text-gray-300 mb-8">
            Análisis de Padel con Inteligencia Artificial
          </p>
        </div>

        {/* Video Upload Section */}
        <div className="py-20">
          <div className="max-w-4xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
                Analiza tu Partido de Padel
              </h2>
              <p className="text-xl text-gray-300 max-w-2xl mx-auto">
                Sube un video de tu partido y obtén análisis detallado con estadísticas 
                de rendimiento, conteo de golpes, velocidad de pelota y más métricas 
                para mejorar tu juego.
              </p>
            </div>

            <div className="bg-white/5 backdrop-blur-sm rounded-3xl border border-white/10 p-8 md:p-12">
              <div className="border-2 border-dashed border-gray-600 rounded-2xl p-12 text-center">
                <div className="flex justify-center mb-6">
                  <div className="w-20 h-20 bg-gradient-to-r from-green-500/20 to-blue-500/20 rounded-full flex items-center justify-center">
                    <span className="text-4xl">📹</span>
                  </div>
                </div>
                <h3 className="text-2xl font-semibold text-white mb-4">
                  Arrastra tu video de padel aquí
                </h3>
                <p className="text-gray-400 mb-6">
                  O haz clic para seleccionar un archivo de video
                </p>
                
                {/* Botón de selección de archivo */}
                <button
                  onClick={() => {
                    const input = document.createElement('input');
                    input.type = 'file';
                    input.accept = 'video/*';
                    input.onchange = (e) => {
                      if (e.target.files && e.target.files[0]) {
                        handleFileUpload(e.target.files[0]);
                      }
                    };
                    input.click();
                  }}
                  disabled={isProcessing}
                  className="bg-gradient-to-r from-green-500 to-blue-500 text-white px-8 py-3 rounded-full hover:from-green-600 hover:to-blue-600 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isProcessing ? 'Procesando...' : 'Seleccionar Video de Padel'}
                </button>
                
                <p className="text-sm text-gray-500 mt-4">
                  Formatos soportados: MP4, AVI, MOV, WMV, FLV, WebM
                </p>
              </div>

              {/* Barra de progreso */}
              {isProcessing && (
                <div className="mt-8">
                  <div className="flex items-center justify-between text-sm text-gray-400 mb-2">
                    <span>Analizando partido con IA (5x más rápido)...</span>
                    <span>{uploadProgress}%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div 
                      className="bg-gradient-to-r from-green-500 to-blue-500 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    ></div>
                  </div>
                  <p className="text-xs text-gray-500 mt-2 text-center">
                    ⚡ Procesando 1 de cada 5 frames para mayor velocidad
                  </p>
                </div>
              )}

              {/* Mensaje de error */}
              {error && (
                <div className="mt-6 p-4 bg-red-500/20 border border-red-500/30 rounded-lg">
                  <p className="text-red-400 text-center">{error}</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Video Procesado con Inferencias */}
        {processedVideoUrl ? (
          <div className="py-20">
            <div className="max-w-4xl mx-auto">
              <h2 className="text-3xl font-bold text-white mb-8 text-center">
                Video Procesado con Análisis de IA
              </h2>
              <div className="bg-white/5 backdrop-blur-sm rounded-3xl border border-white/10 p-8">
                {/* Información de debug */}
                <div className="mb-6 p-4 bg-blue-500/20 border border-blue-500/30 rounded-lg">
                  <p className="text-blue-400 text-sm">
                    🔍 URL del video: {processedVideoUrl}
                  </p>
                  <p className="text-blue-400 text-sm">
                    📁 Nombre del archivo: {matchData?.filename}
                  </p>
                </div>
                
                {/* Video player */}
                <video 
                  controls 
                  preload="metadata"
                  crossOrigin="anonymous"
                  className="w-full rounded-lg"
                  src={processedVideoUrl}
                  onError={(e) => {
                    console.error('Error cargando video:', e);
                    console.error('Video URL:', processedVideoUrl);
                    console.error('Error details:', e.target.error);
                    // Activar fallback MJPEG
                    setUseMjpegFallback(true);
                  }}
                  onLoadStart={() => console.log('Iniciando carga del video...')}
                  onCanPlay={() => console.log('Video listo para reproducir')}
                  onLoadedMetadata={() => console.log('Metadatos del video cargados')}
                  onLoadedData={() => console.log('Datos del video cargados')}
                  onProgress={() => console.log('Video cargando...')}
                >
                  Tu navegador no soporta el elemento video.
                </video>
                {/* MJPEG fallback si el elemento video falla */}
                {useMjpegFallback && processedVideoUrl && (
                  <div className="mt-4">
                    <p className="text-yellow-300 text-sm text-center">Usando fallback MJPEG (frames) porque el video no es reproducible directamente.</p>
                    <img
                      alt="MJPEG stream"
                      className="w-full rounded-lg"
                      src={processedVideoUrl.replace('/stream-processed-video/', '/stream-frames/')}
                    />
                  </div>
                )}
                
                <div className="mt-6 text-center space-y-4">
                  <p className="text-gray-400">
                    Video con detecciones de jugadores, pelota y golpes marcados
                  </p>
                  <div className="flex justify-center space-x-4">
                    <button
                      onClick={() => {
                        console.log('Abriendo video en nueva pestaña:', processedVideoUrl);
                        window.open(processedVideoUrl, '_blank');
                      }}
                      className="bg-gradient-to-r from-blue-500 to-purple-500 text-white px-6 py-2 rounded-full hover:from-blue-600 hover:to-purple-600 transition-all duration-300"
                    >
                      🔗 Ver en Nueva Pestaña
                    </button>
                    <a
                      href={processedVideoUrl}
                      download={`${matchData?.filename?.replace(/\.[^/.]+$/, '')}_processed.mp4`}
                      className="bg-gradient-to-r from-green-500 to-blue-500 text-white px-6 py-2 rounded-full hover:from-green-600 hover:to-blue-600 transition-all duration-300"
                    >
                      📥 Descargar Video Procesado
                    </a>
                  </div>
                  
                  {/* Botón de prueba del endpoint */}
                  <button
                    onClick={async () => {
                      try {
                        const response = await fetch(processedVideoUrl);
                        console.log('Respuesta del endpoint:', response.status, response.statusText);
                        if (response.ok) {
                          alert('✅ Endpoint funcionando correctamente');
                        } else {
                          alert(`❌ Error en endpoint: ${response.status}`);
                        }
                      } catch (error) {
                        console.error('Error probando endpoint:', error);
                        alert(`❌ Error: ${error.message}`);
                      }
                    }}
                    className="bg-gradient-to-r from-yellow-500 to-orange-500 text-white px-4 py-2 rounded-full hover:from-yellow-600 hover:to-orange-600 transition-all duration-300 text-sm"
                  >
                    🧪 Probar Endpoint
                  </button>
                </div>
              </div>
            </div>
          </div>
        ) : matchData && (
          <div className="py-20">
            <div className="max-w-4xl mx-auto">
              <h2 className="text-3xl font-bold text-white mb-8 text-center">
                ⚠️ Video Procesado No Disponible
              </h2>
              <div className="bg-white/5 backdrop-blur-sm rounded-3xl border border-white/10 p-8">
                <div className="text-center space-y-4">
                  <div className="w-20 h-20 bg-yellow-500/20 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-4xl">⚠️</span>
                  </div>
                  <h3 className="text-xl font-semibold text-yellow-400 mb-2">
                    Video Procesado No Generado
                  </h3>
                  <p className="text-gray-300 mb-4">
                    El análisis se completó exitosamente, pero no se pudo generar el video procesado con inferencias.
                  </p>
                  <p className="text-gray-400 text-sm">
                    Esto puede deberse a limitaciones técnicas o errores en el procesamiento de video.
                  </p>
                  <div className="mt-6 p-4 bg-blue-500/20 border border-blue-500/30 rounded-lg">
                    <p className="text-blue-400 text-sm">
                      📊 Estadísticas disponibles: {matchData.total_hits} golpes detectados
                    </p>
                    <p className="text-blue-400 text-sm">
                      🎯 Puedes generar el reporte profesional con los datos analizados
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Results Display */}
        {matchData && (
          <div className="py-20">
            <div className="max-w-4xl mx-auto">
              <h2 className="text-3xl font-bold text-white mb-8 text-center">
                Resultados del Análisis
              </h2>
              <div className="bg-white/5 backdrop-blur-sm rounded-3xl border border-white/10 p-8">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                  <div className="bg-green-500/20 border border-green-500/30 rounded-lg p-6">
                    <h3 className="text-xl font-semibold text-green-400 mb-2">Total de Golpes</h3>
                    <p className="text-4xl font-bold text-white">{matchData.total_hits}</p>
                  </div>
                  <div className="bg-blue-500/20 border border-blue-500/30 rounded-lg p-6">
                    <h3 className="text-xl font-semibold text-blue-400 mb-2">Duración</h3>
                    <p className="text-4xl font-bold text-white">
                      {Math.floor(matchData.video_duration / 60)}:{(matchData.video_duration % 60).toString().padStart(2, '0')}
                    </p>
                  </div>
                  <div className="bg-yellow-500/20 border border-yellow-500/30 rounded-lg p-6">
                    <h3 className="text-xl font-semibold text-yellow-400 mb-2">FPS del Video</h3>
                    <p className="text-4xl font-bold text-white">{matchData.fps}</p>
                  </div>
                  <div className="bg-purple-500/20 border border-purple-500/30 rounded-lg p-6">
                    <h3 className="text-xl font-semibold text-purple-400 mb-2">Total de Frames</h3>
                    <p className="text-4xl font-bold text-white">{matchData.total_frames}</p>
                  </div>
                </div>
                
                {/* Golpes por jugador */}
                <div className="mb-8">
                  <h3 className="text-2xl font-bold text-white mb-4 text-center">Golpes por Jugador</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {Object.entries(matchData.hits_per_player).map(([player, hits]) => (
                      <div key={player} className="bg-white/10 border border-white/20 rounded-lg p-4">
                        <h4 className="text-lg font-semibold text-white mb-2">{player}</h4>
                        <p className="text-3xl font-bold text-green-400">{hits} golpes</p>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="text-center">
                  <p className="text-gray-300 text-lg">{matchData.message}</p>
                  <p className="text-gray-400 text-sm mt-2">Archivo: {matchData.filename}</p>
                </div>

                {/* Botón para generar reporte */}
                <div className="mt-8 text-center">
                  <button
                    onClick={generateReport}
                    disabled={isGeneratingReport}
                    className="bg-gradient-to-r from-purple-500 to-pink-500 text-white px-8 py-3 rounded-full hover:from-purple-600 hover:to-pink-600 transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isGeneratingReport ? (
                      <div className="flex items-center space-x-2">
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                        <span>Generando Reporte con IA...</span>
                      </div>
                    ) : (
                      <div className="flex items-center space-x-2">
                        <span className="text-xl">🤖</span>
                        <span>Reporte Profesional</span>
                      </div>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Reporte Generado */}
        {report && (
          <div className="py-20">
            <div className="max-w-4xl mx-auto">
              <h2 className="text-3xl font-bold text-white mb-8 text-center">
                Reporte Profesional Generado por IA
              </h2>
              <div className="bg-white/5 backdrop-blur-sm rounded-3xl border border-white/10 p-8">
                {/* Renderizar Markdown */}
                <div className="bg-white/10 rounded-lg p-6 mb-6">
                  <div 
                    className="prose prose-invert prose-lg max-w-none"
                    dangerouslySetInnerHTML={{
                      __html: renderMarkdown(report.report)
                    }}
                  />
                </div>
                <div className="text-center space-y-4">
                  <button
                    onClick={downloadReport}
                    className="bg-gradient-to-r from-green-500 to-blue-500 text-white px-8 py-3 rounded-full hover:from-green-600 hover:to-blue-600 transition-all duration-300"
                  >
                    📥 Descargar Reporte
                  </button>
                  {report.metadata && (
                    <div className="mt-4 p-4 bg-blue-500/20 border border-blue-500/30 rounded-lg">
                      <p className="text-blue-400 text-sm">
                        📊 Reporte generado el {new Date(report.metadata.generated_at).toLocaleString()}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
