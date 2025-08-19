import os
import shutil
from fastapi import APIRouter, File, UploadFile, Depends
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
    video_path = os.path.join("data", file.filename)

    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    stats = match_processor.process_video(video_path)
    
    return UploadVideoResponse(
        total_hits=stats.total_hits,
        hits_per_player=stats.hits_per_player,
        total_frames=stats.total_frames,
        video_duration=stats.video_duration,
        fps=stats.fps,
        filename=file.filename,
        message="Video procesado exitosamente"
    )

