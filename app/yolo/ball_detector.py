from .abstract import AbstractYoloDetector
from app.settings import Settings
from ultralytics import YOLO
from dataclasses import dataclass
from numpy import ndarray
from app.data_models import DetectionResultFrame, DetectionResultVideo


@dataclass
class BallYoloDetector(AbstractYoloDetector):
    model_path: str = Settings.BALL_MODEL_PATH
    model_threshold: float = 0.60

    @property
    def load_model(self):
        return YOLO(self.model_path)

    @property
    def class_name(self) -> str:
        return "ball"

    def process_frame(self, frame: ndarray) -> list[DetectionResultFrame]:
        model = self.load_model
        results = model(frame)
        detections = list[DetectionResultFrame]()
        for result in results:
            for box in result.boxes:
                conf = float(box.conf[0])
                if conf >= self.model_threshold:
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
