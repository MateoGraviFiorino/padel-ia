// Configuración de la API de Padel Analytics
export const API_CONFIG = {
  // URL base de la API (ajusta según tu configuración)
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  
  // Endpoints de la API
  ENDPOINTS: {
    HEALTH: '/status/health',
    SYSTEM: '/status/system',
    API_INFO: '/status/api',
    UPLOAD_VIDEO: '/match/upload-video',
    HISTORY: '/match/history',
    REPORT: '/match/report',
  },
  
  // Configuración de timeout
  TIMEOUT: 30000, // 30 segundos
  
  // Configuración de reintentos
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000, // 1 segundo
  
  // Configuración de archivos
  MAX_FILE_SIZE: 100 * 1024 * 1024, // 100MB
  ALLOWED_VIDEO_TYPES: [
    'video/mp4',
    'video/avi',
    'video/mov',
    'video/wmv',
    'video/flv',
    'video/webm'
  ],
  
  // Configuración de desarrollo
  USE_MOCK_DATA: process.env.NODE_ENV === 'development',
  MOCK_DELAY: 2000, // 2 segundos para simulación
};

// Función para construir URLs completas
export const buildApiUrl = (endpoint) => {
  return `${API_CONFIG.BASE_URL}${endpoint}`;
};

// Función para validar tipos de archivo
export const isValidVideoFile = (file) => {
  return API_CONFIG.ALLOWED_VIDEO_TYPES.includes(file.type);
};

// Función para validar tamaño de archivo
export const isValidFileSize = (file) => {
  return file.size <= API_CONFIG.MAX_FILE_SIZE;
};

// Función para formatear tamaño de archivo
export const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};
