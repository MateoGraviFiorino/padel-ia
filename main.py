from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import cv2
import os
import logging
import sys
from genai import analyze_tennis_video

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/output_files", StaticFiles(directory="output_files"), name="output_files")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):
    try:
        # Prepare output filename
        output_filename = f"uploaded_{file.filename}"
        output_path = os.path.join("output_files", output_filename)
        
        # Save the uploaded file directly
        with open(output_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Generate analysis
        credentials_path = "neat-fin-468000-i5-ddabf952e9d8.json"
        bucket_name = "tennis-data-marcoaloisi"
        analysis = analyze_tennis_video(output_path, credentials_path, bucket_name)

        return JSONResponse(content={
            "status": "success",
            "video_url": f"/output_files/{output_filename}",
            "analysis": analysis
        })

    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        return JSONResponse(content={
            "status": "error",
            "message": str(e)
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)