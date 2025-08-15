from abc import ABC, abstractmethod
from dataclasses import dataclass
from numpy import ndarray
import cv2
from tqdm import tqdm
from app.data_models import DetectionResultFrame, DetectionResultVideo


@dataclass
class AbstractYoloDetector(ABC):
    model_path: str
    model_threshold: float

    @property
    @abstractmethod
    def load_model(self):
        pass

    @property
    @abstractmethod
    def class_name(self) -> str:
        pass
    
    @abstractmethod
    def process_frame(self, frame: ndarray) -> list[DetectionResultFrame]:
        pass
    
    @abstractmethod
    def process_video(self, video_path: str) -> DetectionResultVideo:
        pass