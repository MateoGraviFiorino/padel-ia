# Análisis de Tenis mediante Computer Vision

Este proyecto implementa un sistema de análisis de partidos de tenis utilizando técnicas de computer vision. El sistema detecta jugadores, la pelota, y genera estadísticas de juego en tiempo real. Posteriormente un modelo LLM analiza el punto.

## Características

- Detección y seguimiento de jugadores
- Detección y seguimiento de la pelota
- Detección de líneas de la cancha
- Visualización de mini-cancha con posiciones en tiempo real
- Cálculo de estadísticas:
  - Velocidad de los tiros
  - Velocidad de movimiento de los jugadores
  - Velocidades promedio
  - Posiciones en la cancha
- Analisis del punto usando LLM de Google Gemini
  
## Modelos Pre-entrenados

El proyecto utiliza los siguientes modelos:

- **YOLO para detección de jugadores**: Modelo entrenado para detectar y seguir a los jugadores en la cancha.
- **YOLO para detección de pelota**: Modelo especializado en detectar la pelota de tenis, aunque presenta algunos desafíos:
 - El entrenamiento fue complejo debido al pequeño tamaño de la pelota
 - La alta velocidad de la pelota causó dificultades en la detección
 - Se requirió un extenso conjunto de datos de entrenamiento para mejorar la precisión
- **Modelo personalizado para detección de líneas de la cancha**: Detector de puntos clave para identificar las líneas y dimensiones de la cancha.

### Desafíos Técnicos

#### Detección de la Pelota
- La pelota de tenis es muy pequeña en el frame del video
- El movimiento rápido causa motion blur
- Las sombras y cambios de iluminación afectan la detección
- Se necesitó entrenar durante dias el modelo y hacer mucho post processing.

#### Visualización en Mini-Court
- El seguimiento de la pelota en la vista miniatura presenta inconsistencias
- La conversión de coordenadas entre la cancha real y la miniatura requirió ajustes de perspectiva
- El movimiento de la pelota puede aparecer errático debido a:
 - Errores en la detección original
 - Imprecisiones en la transformación de coordenadas
 - Desafíos en el manejo de la perspectiva de la cancha

## Descarga de Recursos Necesarios

Antes de ejecutar el proyecto, es necesario descargar los recursos (video y modelos entrenados) desde el siguiente enlace:

[Descargar Recursos](https://drive.google.com/drive/folders/1kXu_O8Yg2R90vxw_ddSkUSCTt5j_bmA6?usp=sharing)

Tambien es necesario hacer credenciales de google cloud para usar vertexapi , bucket y gemini.

Una vez te crees tu proyecto tienes que hacer credenciales de un Service Accounts. 
Luego dentro de tu service account te vas al apartado de Keys y generas tu Json. Ese Json lo pones en la raiz del directorio /app
Luego el nombre de tu archivo json tiene que ponerlo en el docker-compose.yml en la linea: - ./rich-suprstate-442213-c5-77b993f9b67b.json:/app/rich-suprstate-442213-c5-77b993f9b67b.json
cambias el (rich-suprstate-442213-c5-77b993f9b67b) por el tuyo y tambien en el main.py en la linea de CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), "rich-suprstate-442213-c5-77b993f9b67b.json")


Los notebooks estan dentro de la carpeta app/train.


### Instrucciones de instalación

1. Descarga todos los archivos del enlace proporcionado
2. Coloca las carpetas descargadas dentro del directorio `app/` de tu proyecto:

## Instalación y Ejecución

### 1. Clonar el Repositorio
```bash
git clone https://github.com/MarcoAloisi/tennisvision.git
cd app
```

### 2. Construir y Ejecutar con Docker Compose
```bash
docker compose up --build
```

Este comando:
* Construirá la imagen Docker con todas las dependencias necesarias.
* Iniciará los servicios definidos en el `docker-compose.yml`.
* Configurará el entorno necesario para la ejecución.

### 3. Acceder a la Aplicación
Una vez que el contenedor esté en ejecución:
1. Abre tu navegador web.
2. Visita [http://localhost:8000](http://localhost:8000).

### Uso de la Aplicación
1. En tu navegador, accede a [http://localhost:8000](http://localhost:8000).
2. La interfaz te permitirá:
   * Seleccionar un video de tenis para analizar
3. Sube el video de la carperta input y haz click en analizar.
4. Esperar el resultado.
```

### NOTA

EL MAIN.PY QUE ESTA A RAIZ DEL GITHUB (NO DENTRO DE LA CARPETA APP) ES DONDE REALIZE EL ENTRENAMIENTO Y POST PROCESAMIENTO ORIGINAL. YA QUE EL MAIN DENTRO DE LA CARPETA APP ES SOLO PARA LA APP DOCKER Y DONDE SE CARGA EL VIDEO. TUVE QUE HACERLO ASI YA QUE ME DABA MUCHOS PROBLEMAS DE MEMORIA

