from pydantic import BaseModel, Field

class MatchStatistics(BaseModel):
    total_hits: int = Field(default=0)
    hits_per_player: dict[str, int] = Field(default_factory=dict)
    total_frames: int = Field(default=0)
    video_duration: float = Field(default=0.0)
    fps: float = Field(default=0.0)
