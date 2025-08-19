# PadelAI - Análisis de Padel con Inteligencia Artificial

Este repositorio contiene la aplicación web frontend para **PadelAI**, una plataforma innovadora que utiliza inteligencia artificial para analizar partidos de padel, detectar jugadores, contar golpes y generar estadísticas detalladas de rendimiento.

## 🎾 Características Principales

- **Análisis Automático de Video**: Sube videos de partidos y obtén análisis instantáneo
- **Detección de Jugadores**: Identifica y rastrea a cada jugador en tiempo real
- **Conteo de Golpes**: Cuenta automáticamente los golpes por jugador
- **Estadísticas Avanzadas**: Métricas completas de rendimiento y duración
- **Interfaz Moderna**: Diseño responsive con animaciones fluidas
- **API REST**: Backend robusto con FastAPI y Python

## 🚀 Tecnologías Utilizadas

### Frontend
- **React 18** - Biblioteca de UI moderna y eficiente
- **Vite** - Build tool rápido para desarrollo
- **Tailwind CSS** - Framework de CSS utility-first
- **Framer Motion** - Animaciones fluidas y atractivas
- **Lucide React** - Iconos modernos y consistentes

### Backend
- **FastAPI** - Framework web moderno y rápido
- **Python 3.8+** - Lenguaje de programación principal
- **YOLO** - Detección de objetos en tiempo real
- **OpenCV** - Procesamiento de video avanzado

## 📁 Estructura del Proyecto

```
app/web/
├── frontend/                 # Aplicación React principal
│   ├── public/              # Archivos estáticos
│   ├── src/
│   │   ├── components/      # Componentes reutilizables
│   │   │   ├── NadelNavBar.jsx      # Barra de navegación
│   │   │   ├── PadelHeroSection.jsx # Sección principal
│   │   │   ├── VideoUploadSection.jsx # Subida de videos
│   │   │   ├── AnalyticsDashboard.jsx # Dashboard de resultados
│   │   │   └── Footer.jsx           # Pie de página
│   │   ├── pages/           # Páginas de la aplicación
│   │   │   └── PadelAnalyticsPage.jsx # Página principal
│   │   ├── services/        # Servicios de API
│   │   │   └── padelApi.js  # Cliente de API
│   │   ├── config/          # Configuración
│   │   │   └── api.js       # Configuración de API
│   │   ├── App.jsx          # Componente principal
│   │   ├── main.jsx         # Punto de entrada
│   │   └── index.css        # Estilos globales
│   ├── package.json         # Dependencias del frontend
│   ├── tailwind.config.js   # Configuración de Tailwind
│   └── vite.config.js       # Configuración de Vite
├── package.json              # Dependencias del web
└── README.md                 # Este archivo
```

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Node.js 16+ 
- npm o yarn
- Backend de FastAPI ejecutándose

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd padel-ia/app/web
   ```

2. **Instalar dependencias del frontend**
   ```bash
   npm run install-frontend
   ```

3. **Configurar variables de entorno**
   ```bash
   # Crear archivo .env.local en frontend/
   REACT_APP_API_URL=http://localhost:8000
   ```

4. **Ejecutar en desarrollo**
   ```bash
   npm run dev
   ```

5. **Construir para producción**
   ```bash
   npm run build
   ```

## 🔧 Configuración

### API Configuration
El archivo `frontend/src/config/api.js` contiene toda la configuración:

```javascript
export const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  TIMEOUT: 30000,
  MAX_FILE_SIZE: 100 * 1024 * 1024, // 100MB
  ALLOWED_VIDEO_TYPES: ['video/mp4', 'video/avi', 'video/mov', ...]
};
```

### Variables de Entorno
- `REACT_APP_API_URL`: URL base de la API backend
- `NODE_ENV`: Entorno de ejecución (development/production)

## 📱 Uso de la Aplicación

### 1. Subir Video
- Arrastra y suelta un archivo de video en la zona de subida
- O haz clic para seleccionar un archivo
- Formatos soportados: MP4, AVI, MOV, WMV, FLV, WebM
- Tamaño máximo: 100MB

### 2. Procesamiento
- El video se envía al backend para análisis
- La IA detecta jugadores y cuenta golpes
- Progreso en tiempo real durante el procesamiento

### 3. Resultados
- Dashboard con estadísticas detalladas
- Métricas por jugador
- Análisis de rendimiento
- Opción de descargar reporte

## 🔌 API Endpoints

### Status
- `GET /status/health` - Estado de la API
- `GET /status/system` - Información del sistema
- `GET /status/api` - Información de la API

### Match Analysis
- `POST /match/upload-video` - Subir y procesar video
- `GET /match/history` - Historial de análisis (futuro)
- `GET /match/report/{id}` - Descargar reporte (futuro)

## 🎨 Personalización

### Temas y Colores
Los colores principales se pueden modificar en `frontend/tailwind.config.js`:

```javascript
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          500: '#22c55e', // Verde principal
          600: '#16a34a'
        },
        secondary: {
          500: '#3b82f6', // Azul secundario
          600: '#2563eb'
        }
      }
    }
  }
}
```

### Componentes
Cada componente está diseñado para ser fácilmente personalizable:
- Modifica los textos en los archivos JSX
- Ajusta los estilos usando clases de Tailwind
- Cambia los iconos importando desde Lucide React

## 🚀 Despliegue

### Build de Producción
```bash
npm run build
```

### Servidor Web
Los archivos generados en `frontend/dist/` se pueden servir con cualquier servidor web estático:
- Nginx
- Apache
- Servicios de hosting estático (Netlify, Vercel, etc.)

### Variables de Entorno de Producción
```bash
REACT_APP_API_URL=https://tu-api-backend.com
NODE_ENV=production
```

## 🐛 Solución de Problemas

### Error de Conexión API
- Verifica que el backend esté ejecutándose
- Confirma la URL en la configuración
- Revisa los logs del backend

### Problemas de Subida de Video
- Verifica el formato del archivo
- Confirma que no exceda el tamaño máximo
- Revisa la consola del navegador para errores

### Problemas de Rendimiento
- Optimiza el tamaño de los videos
- Usa formatos de video eficientes (MP4, WebM)
- Considera comprimir videos grandes

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas:
- Abre un issue en GitHub
- Contacta al equipo de desarrollo
- Revisa la documentación de la API

---

**PadelAI** - Transformando el análisis de padel con inteligencia artificial 🎾✨
