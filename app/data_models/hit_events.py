from pydantic import BaseModel

class HitEvent(BaseModel):
    player_id: str
    frame_number: int
    timestamp: float
    player_confidence: float
    ball_confidence: float
    player_box: list[float]
    ball_box: list[float]
