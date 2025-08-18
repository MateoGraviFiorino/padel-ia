import { API_CONFIG, buildApiUrl, isValidVideoFile, isValidFileSize, formatFileSize } from '../config/api';

class PadelApiService {
  constructor() {
    this.baseUrl = API_CONFIG.BASE_URL;
  }

  // Verificar estado de la API
  async checkHealth() {
    try {
      const response = await fetch(buildApiUrl(API_CONFIG.ENDPOINTS.HEALTH), {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(API_CONFIG.TIMEOUT),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error checking API health:', error);
      throw error;
    }
  }

  // Obtener información del sistema
  async getSystemInfo() {
    try {
      const response = await fetch(buildApiUrl(API_CONFIG.ENDPOINTS.SYSTEM), {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(API_CONFIG.TIMEOUT),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error getting system info:', error);
      throw error;
    }
  }

  // Obtener información de la API
  async getApiInfo() {
    try {
      const response = await fetch(buildApiUrl(API_CONFIG.ENDPOINTS.API_INFO), {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(API_CONFIG.TIMEOUT),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error getting API info:', error);
      throw error;
    }
  }

  // Subir y procesar video
  async uploadAndProcessVideo(file, onProgress) {
    try {
      // Validar archivo
      if (!isValidVideoFile(file)) {
        throw new Error(`Tipo de archivo no soportado. Tipos permitidos: ${API_CONFIG.ALLOWED_VIDEO_TYPES.join(', ')}`);
      }
      
      if (!isValidFileSize(file)) {
        throw new Error(`Archivo demasiado grande. Tamaño máximo: ${formatFileSize(API_CONFIG.MAX_FILE_SIZE)}`);
      }

      const formData = new FormData();
      formData.append('file', file);

      // Simular progreso inicial
      onProgress(10);

      const response = await fetch(buildApiUrl(API_CONFIG.ENDPOINTS.UPLOAD_VIDEO), {
        method: 'POST',
        body: formData,
        signal: AbortSignal.timeout(API_CONFIG.TIMEOUT),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
      }

      onProgress(100);
      const result = await response.json();
      return result;
    } catch (error) {
      console.error('Error uploading video:', error);
      throw error;
    }
  }

  // Simular procesamiento de video (para desarrollo)
  async simulateVideoProcessing(file, onProgress) {
    return new Promise((resolve) => {
      let progress = 0;
      const interval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress >= 100) {
          progress = 100;
          clearInterval(interval);
          
          // Simular datos de respuesta de la API
          const mockData = {
            total_hits: Math.floor(Math.random() * 200) + 100,
            hits_per_player: {
              "Jugador 1": Math.floor(Math.random() * 100) + 50,
              "Jugador 2": Math.floor(Math.random() * 100) + 50
            },
            total_frames: Math.floor(Math.random() * 5000) + 3000,
            video_duration: Math.random() * 200 + 100,
            fps: 30.0,
            filename: file.name,
            message: "Video procesado exitosamente (simulación)"
          };
          
          resolve(mockData);
        }
        onProgress(progress);
      }, API_CONFIG.MOCK_DELAY / 10);
    });
  }

  // Obtener historial de análisis (futuro)
  async getAnalysisHistory() {
    try {
      const response = await fetch(buildApiUrl(API_CONFIG.ENDPOINTS.HISTORY), {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        signal: AbortSignal.timeout(API_CONFIG.TIMEOUT),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error getting analysis history:', error);
      throw error;
    }
  }

  // Descargar reporte (futuro)
  async downloadReport(analysisId) {
    try {
      const response = await fetch(buildApiUrl(`${API_CONFIG.ENDPOINTS.REPORT}/${analysisId}`), {
        method: 'GET',
        signal: AbortSignal.timeout(API_CONFIG.TIMEOUT),
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const blob = await response.blob();
      
      // Crear link de descarga
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `padel-analysis-${analysisId}.pdf`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading report:', error);
      throw error;
    }
  }

  // Función de reintento con backoff exponencial
  async retryWithBackoff(fn, retries = API_CONFIG.RETRY_ATTEMPTS) {
    try {
      return await fn();
    } catch (error) {
      if (retries > 0) {
        await new Promise(resolve => setTimeout(resolve, API_CONFIG.RETRY_DELAY));
        return this.retryWithBackoff(fn, retries - 1);
      }
      throw error;
    }
  }
}

export default new PadelApiService();
