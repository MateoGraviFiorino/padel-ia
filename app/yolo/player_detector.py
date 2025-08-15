from .abstract import AbstractYoloDetector
from app.settings import Settings
from ultralytics import YOLO
from dataclasses import dataclass, field
import cv2
from tqdm import tqdm
from numpy import ndarray
from app.data_models import DetectionResultFrame, DetectionResultVideo
import numpy as np

@dataclass
class PlayerYoloDetector(AbstractYoloDetector):
    model_path: str = Settings.PLAYER_MODEL_PATH
    model_threshold: float = 0.60
    max_distance: float = 80.0
    next_player_id: int = field(default=0, init=False)
    tracked_players: dict[int, list[float]] = field(default_factory=dict, init=False)
    player_frames_missing: dict[int, int] = field(default_factory=dict, init=False)

    @property
    def load_model(self):
        return YOLO(self.model_path)

    @property
    def class_name(self) -> str:
        return "player"

    def _get_iou(self, box_a: list[float], box_b: list[float]) -> float:
        x_a = max(box_a[0], box_b[0])
        y_a = max(box_a[1], box_b[1])
        x_b = min(box_a[2], box_b[2])
        y_b = min(box_a[3], box_b[3])

        inter_area = max(0, x_b - x_a) * max(0, y_b - y_a)
        box_a_area = (box_a[2] - box_a[0]) * (box_a[3] - box_a[1])
        box_b_area = (box_b[2] - box_b[0]) * (box_b[3] - box_b[1])
        iou = inter_area / float(box_a_area + box_b_area - inter_area + 1e-6)
        return iou

    def _assign_player_id(self, box: list[float]) -> int:
        best_iou = 0
        best_id = None
        
        # Buscar el jugador con mayor IoU
        for player_id, prev_box in self.tracked_players.items():
            iou = self._get_iou(box, prev_box)
            if iou > best_iou and iou > 0.3:  # Aumentar el umbral para ser más estricto
                best_iou = iou
                best_id = player_id

        if best_id is not None:
            # Actualizar la posición del jugador trackeado y resetear contador de frames faltantes
            self.tracked_players[best_id] = box
            self.player_frames_missing[best_id] = 0
            return best_id
        else:
            # Si no hay coincidencia, crear un nuevo jugador
            player_id = self.next_player_id
            self.tracked_players[player_id] = box
            self.player_frames_missing[player_id] = 0
            self.next_player_id += 1
            return player_id

    def _cleanup_missing_players(self):
        """Limpia jugadores que no se han visto por varios frames"""
        max_frames_missing = 10  # Máximo número de frames que puede faltar un jugador
        
        players_to_remove = []
        for player_id, frames_missing in self.player_frames_missing.items():
            if frames_missing > max_frames_missing:
                players_to_remove.append(player_id)
        
        for player_id in players_to_remove:
            del self.tracked_players[player_id]
            del self.player_frames_missing[player_id]
        
        # Incrementar contador de frames faltantes para todos los jugadores
        for player_id in self.player_frames_missing:
            self.player_frames_missing[player_id] += 1

    def process_frame(self, frame: ndarray) -> list[DetectionResultFrame]:
        model = self.load_model
        results = model(frame)
        detections: list[DetectionResultFrame] = []

        # Limpiar jugadores que no se han visto por varios frames
        self._cleanup_missing_players()
        
        # No limpiar el tracking aquí, mantenerlo entre frames
        current_frame_detections = []

        for result in results:
            for box in result.boxes:
                conf = float(box.conf[0])
                if conf >= self.model_threshold:
                    xyxy = box.xyxy[0].cpu().numpy().tolist()
                    current_frame_detections.append(xyxy)

        # Asignar IDs a las detecciones del frame actual
        for box in current_frame_detections:
            player_id = self._assign_player_id(box)
            # Encontrar la confianza correspondiente
            for result in results:
                for result_box in result.boxes:
                    if float(result_box.conf[0]) >= self.model_threshold:
                        result_xyxy = result_box.xyxy[0].cpu().numpy().tolist()
                        if result_xyxy == box:
                            conf = float(result_box.conf[0])
                            detections.append(
                                DetectionResultFrame(
                                    box=box,
                                    confidence=conf,
                                    class_name=self.class_name,
                                    class_id=str(player_id)
                                )
                            )
                            break

        return detections

    def process_video(self, video_path: str) -> DetectionResultVideo:
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        frame_detections: list[DetectionResultFrame] = []

        self.next_player_id = 0
        self.tracked_players.clear()
        self.player_frames_missing.clear()

        with tqdm(total=total_frames, desc=f"Processing {self.class_name} detections", unit="frames") as pbar:
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
            import os
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            output_path = f"data/output_{base_name}_detected.mp4"
        
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Configurar el writer de video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        frame_detections: list[DetectionResultFrame] = []
        
        # Reiniciar tracking
        self.next_player_id = 0
        self.tracked_players.clear()
        self.player_frames_missing.clear()
        
        # Colores para diferentes jugadores (círculo cromático)
        colors = [
            (255, 0, 0),    # Azul
            (0, 255, 0),    # Verde
            (0, 0, 255),    # Rojo
            (255, 255, 0),  # Cian
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Amarillo
            (128, 0, 128),  # Púrpura
            (255, 165, 0),  # Naranja
        ]
        
        with tqdm(total=total_frames, desc=f"Processing {self.class_name} with output", unit="frames") as pbar:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                detections = self.process_frame(frame)
                frame_detections.extend(detections)
                
                # Dibujar las detecciones en el frame
                annotated_frame = frame.copy()
                for detection in detections:
                    x1, y1, x2, y2 = map(int, detection.box)
                    player_id = int(detection.class_id)
                    confidence = detection.confidence
                    
                    # Seleccionar color basado en el ID del jugador
                    color = colors[player_id % len(colors)]
                    
                    # Dibujar bounding box
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                    
                    # Dibujar etiqueta con ID y confianza
                    label = f"Player {player_id} ({confidence:.2f})"
                    label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                    cv2.rectangle(annotated_frame, (x1, y1 - label_size[1] - 10), 
                                (x1 + label_size[0], y1), color, -1)
                    cv2.putText(annotated_frame, label, (x1, y1 - 5), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                # Escribir el frame al video de salida
                out.write(annotated_frame)
                pbar.update(1)
        
        cap.release()
        out.release()
        
        print(f"Video procesado guardado en: {output_path}")
        return DetectionResultVideo(frame_detections=frame_detections)