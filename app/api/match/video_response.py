from pydantic import BaseModel

class UploadVideoResponse(BaseModel):
    total_hits: int
    hits_per_player: dict[str, int]
    total_frames: int
    video_duration: float
    fps: float
    filename: str
    message: str
