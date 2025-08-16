from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from pathlib import Path
from .video_response import UploadVideoResponse
from app.match import PadelMatchProcessor, MatchStatistics

match_router = APIRouter(prefix="/match", tags=["match"])

def get_match_processor() -> PadelMatchProcessor:
    return PadelMatchProcessor()


@match_router.post("/upload-video", response_model=UploadVideoResponse)
async def upload_and_process_video(
    file: UploadFile = File(...),
    match_processor: PadelMatchProcessor = Depends(get_match_processor)
) -> UploadVideoResponse:
    stats = match_processor.process_video(file.filename)
    
    return UploadVideoResponse(
        total_hits=stats.total_hits,
        hits_per_player=stats.hits_per_player,
        total_frames=stats.total_frames,
        video_duration=stats.video_duration,
        fps=stats.fps,
        filename=file.filename,
        message="Video procesado exitosamente"
    )
