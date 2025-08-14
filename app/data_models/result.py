from pydantic import BaseModel, Field
from typing import Literal


class DetectionResultFrame(BaseModel):
    box: list[float]
    confidence: float = Field(ge=0, le=1)
    class_name: Literal["ball", "player"]


class DetectionResultVideo(BaseModel):
    frame_detections: list[DetectionResultFrame]