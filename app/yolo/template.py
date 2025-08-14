from abc import ABC, abstractmethod
from dataclasses import dataclass
from numpy import ndarray
import cv2
from tqdm import tqdm
from app.data_models import DetectionResultFrame, DetectionResultVideo


@dataclass
class TemplateYoloDetector(ABC):
    model_path: str
    model_treshold: float

    @property
    @abstractmethod
    def load_model(self):
        pass

    @property
    @abstractmethod
    def class_name(self) -> str:
        pass

    def process_frame(self, frame: ndarray) -> list[DetectionResultFrame]:
        model = self.load_model
        results = model(frame)
        detections = list[DetectionResultFrame]()
        for result in results:
            for box in result.boxes:
                conf = float(box.conf[0])
                if conf >= self.model_treshold:
                    xyxy = box.xyxy[0].cpu().numpy().tolist()
                    detections.append(DetectionResultFrame(
                        box=xyxy,
                        confidence=conf,
                        class_name=self.class_name
                    ))
        return detections

    def process_video(self, video_path: str) -> DetectionResultVideo:
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        frame_detections = list[DetectionResultFrame]()
        
        with tqdm(total=total_frames, desc=f"Processing {self.class_name} detections", 
                 unit="frames") as pbar:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                    
                detections = self.process_frame(frame)
                frame_detections.extend(detections)
                pbar.update(1)
                
        cap.release()
        return DetectionResultVideo(frame_detections=frame_detections)

