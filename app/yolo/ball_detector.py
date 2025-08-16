from .abstract import AbstractYoloDetector
from app.settings import Settings
from ultralytics import YOLO
from dataclasses import dataclass
from numpy import ndarray
from app.data_models import DetectionResultFrame, DetectionResultVideo
import cv2
from tqdm import tqdm
from .config import COLORS
import os


@dataclass
class BallYoloDetector(AbstractYoloDetector):
    model_path: str = Settings.BALL_MODEL_PATH
    model_threshold: float = 0.50

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
                        class_name=self.class_name,
                        class_id="1"
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

    def process_video_with_output(self, video_path: str, output_path: str = None) -> DetectionResultVideo:
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            output_path = f"data/output_{base_name}_ball_detected.mp4"
        
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_detections: list[DetectionResultFrame] = []
        
        with tqdm(total=total_frames, desc=f"Processing {self.class_name} with output", unit="frames") as pbar:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                detections = self.process_frame(frame)
                frame_detections.extend(detections)
                
                annotated_frame = frame.copy()
                for detection in detections:
                    x1, y1, x2, y2 = map(int, detection.box)
                    confidence = detection.confidence
                    
                    color = (0, 0, 255) 
                    
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                    
                    label = f"Ball ({confidence:.2f})"
                    label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                    cv2.rectangle(annotated_frame, (x1, y1 - label_size[1] - 10), 
                                (x1 + label_size[0], y1), color, -1)
                    cv2.putText(annotated_frame, label, (x1, y1 - 5), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                out.write(annotated_frame)
                pbar.update(1)
        
        cap.release()
        out.release()
        
        print(f"Video procesado guardado en: {output_path}")
        return DetectionResultVideo(frame_detections=frame_detections)


    