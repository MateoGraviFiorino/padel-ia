import vertexai
from vertexai.generative_models import GenerativeModel, Part
import os
from google.oauth2 import service_account
from google.cloud import storage

def analyze_tennis_video(video_path, credentials_path, bucket_name):
    """
    Args:
        video_path: Path to local MP4 file
        credentials_path: Path to service account JSON file
        bucket_name: GCS bucket name
    """
    # Load credentials
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )

    # Upload video to GCS
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    video_name = os.path.basename(video_path)
    blob = bucket.blob(f"tennis_videos/{video_name}")
    blob.upload_from_filename(video_path)

    gcs_uri = f"gs://{bucket_name}/tennis_videos/{video_name}"

    # Initialize Vertex AI
    vertexai.init(
        project="rich-suprstate-442213-c5",
        location="us-central1",
        credentials=credentials
    )

    model = GenerativeModel("gemini-1.5-pro")
    video_file = Part.from_uri(gcs_uri, mime_type="video/mp4")

    tennis_prompt = """
Analiza el punto de tenis presentado en el archivo .avi proporcionado, donde Sinner está sacando y Medvedev está recibiendo el saque.

### Información de los jugadores:
- **Sinner**:
  - Edad: 23 años
  - Altura: 1.92 metros
  - Mano dominante: Diestro
  - Posición en la cámara: Más cerca de la cámara

- **Medvedev**:
  - Edad: 28 años
  - Altura: 1.98 metros
  - Mano dominante: Diestro
  - Posición en la cámara: Más lejos de la cámara

### Instrucciones:
1. **Explicación General del Punto**:
   - Describe de manera general por qué Sinner ganó el punto.
   - Enfócate en aspectos observables como el posicionamiento en la cancha, la consistencia de los golpes, la velocidad de reacción, y la estrategia general.

2. **Sugerencias para Medvedev**:
   - Explica qué acciones o estrategias podría haber implementado Medvedev para ganar el punto.
   - Mantén las sugerencias generales, como mejorar la anticipación, variar la colocación de los golpes, aumentar la agresividad en la devolución, etc.

3. **Evitar Detalles Específicos**:
   - No menciones tipos específicos de golpes (como dropshots, smashes, etc.) a menos que sean claramente evidentes en el video.
   - Basar el análisis únicamente en lo que se puede observar en el video, evitando suposiciones sobre tácticas o movimientos no evidenciados.

### Formato de Respuesta:
Proporciona una respuesta clara y concisa siguiendo este formato:

"Sinner ganó el punto debido a [razón general basada en la observación]. Medvedev pudo haber ganado el punto si [sugerencia general basada en la observación]."

### Ejemplo de Respuesta:
"Sinner ganó el punto debido a su excelente posicionamiento y consistencia en los golpes, lo que dificultó que Medvedev respondiera eficazmente. Medvedev pudo haber ganado el punto si hubiera mejorado su anticipación y variado más la colocación de sus devoluciones."
"""


    return model.generate_content([video_file, tennis_prompt]).text

