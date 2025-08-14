from .template import TemplateYoloDetector
from app.settings import Settings
from ultralytics import YOLO
from dataclasses import dataclass


@dataclass
class PlayerYoloDetector(TemplateYoloDetector):
    model_path: str = Settings.PLAYER_MODEL_PATH
    model_treshold: float = 0.25

    @property
    def load_model(self):
        return YOLO(self.model_path)

    @property
    def class_name(self) -> str:
        return "player"
