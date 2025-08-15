from dataclasses import dataclass, field
import cv2
from tqdm import tqdm
import os
from numpy import ndarray
import numpy as np
from pydantic import BaseModel, Field
from app.yolo.player_detector import PlayerYoloDetector
from app.yolo.ball_detector import BallYoloDetector
from app.data_models import DetectionResultFrame, DetectionResultVideo


class HitEvent(BaseModel):
    player_id: str
    frame_number: int
    timestamp: float
    player_confidence: float
    ball_confidence: float
    player_box: list[float]
    ball_box: list[float]


class MatchStatistics(BaseModel):
    total_hits: int = Field(default=0)
    hits_per_player: dict[str, int] = Field(default_factory=dict)
    total_frames: int = Field(default=0)
    video_duration: float = Field(default=0.0)
    fps: float = Field(default=0.0)


@dataclass
class PadelMatchProcessor:
    hit_distance_threshold: float = 80.0
    min_frames_between_hits: int = 10
    player_detector: PlayerYoloDetector = field(default_factory=PlayerYoloDetector)
    ball_detector: BallYoloDetector = field(default_factory=BallYoloDetector)
    match_stats: MatchStatistics = field(default_factory=MatchStatistics)
    hit_events: list[HitEvent] = field(default_factory=list)
    last_hit_frame: dict[str, int] = field(default_factory=dict)
        
    def _calculate_distance(self, player_box: list[float], ball_box: list[float]) -> float:
        if len(player_box) != 4 or len(ball_box) != 4:
            return float('inf')
        
        player_center_x = (player_box[0] + player_box[2]) / 2
        player_center_y = (player_box[1] + player_box[3]) / 2

        ball_center_x = (ball_box[0] + ball_box[2]) / 2
        ball_center_y = (ball_box[1] + ball_box[3]) / 2
        
        # Distancia euclidiana
        distance = ((player_center_x - ball_center_x) ** 2 + (player_center_y - ball_center_y) ** 2) ** 0.5
        return distance
    
    def _detect_hits_in_frame(self, frame: ndarray, frame_number: int, timestamp: float) -> list[HitEvent]:
        hits = []
        
        if frame is None:
            return hits
        
        try:
            player_detections = self.player_detector.process_frame(frame)
            ball_detections = self.ball_detector.process_frame(frame)
        except Exception as e:
            print(f"Error procesando frame {frame_number}: {e}")
            return hits
        
        if not ball_detections:
            return hits
        
        for player_detection in player_detections:
            player_id = player_detection.class_id
            
            # Verificar si este jugador ya golpeó recientemente
            if player_id in self.last_hit_frame:
                frames_since_last_hit = frame_number - self.last_hit_frame[player_id]
                if frames_since_last_hit < self.min_frames_between_hits:
                    continue
            
            # Buscar la pelota más cercana a este jugador
            best_distance = float('inf')
            best_ball_detection = None
            
            for ball_detection in ball_detections:
                distance = self._calculate_distance(player_detection.box, ball_detection.box)
                if distance < best_distance:
                    best_distance = distance
                    best_ball_detection = ball_detection
            
            # Si el jugador está suficientemente cerca de la pelota, es un golpe
            if best_distance < self.hit_distance_threshold and best_ball_detection is not None:
                hit_event = HitEvent(
                    player_id=player_id,
                    frame_number=frame_number,
                    timestamp=timestamp,
                    player_confidence=player_detection.confidence,
                    ball_confidence=best_ball_detection.confidence,
                    player_box=player_detection.box,
                    ball_box=best_ball_detection.box
                )
                hits.append(hit_event)
                
                # Actualizar el último frame donde este jugador golpeó
                self.last_hit_frame[player_id] = frame_number
        
        return hits
    
    def process_video(self, video_path: str) -> MatchStatistics:
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video no encontrado: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"No se pudo abrir el video: {video_path}")
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps if fps > 0 else 0
        
        # Reiniciar estadísticas y estado interno
        self.hit_events.clear()
        self.last_hit_frame.clear()
        self.match_stats = MatchStatistics(
            total_frames=total_frames,
            video_duration=duration,
            fps=fps
        )
        
        print(f"Procesando video: {video_path}")
        print(f"Frames: {total_frames}, FPS: {fps:.2f}, Duración: {duration:.2f}s")
        print(f"Umbral de distancia: {self.hit_distance_threshold}px, Mínimo frames entre golpes: {self.min_frames_between_hits}")
        
        try:
            with tqdm(total=total_frames, desc="Analizando partido", unit="frames") as pbar:
                frame_number = 0
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    timestamp = frame_number / fps if fps > 0 else 0
                    
                    # Detectar golpes en este frame
                    frame_hits = self._detect_hits_in_frame(frame, frame_number, timestamp)
                    self.hit_events.extend(frame_hits)
                    
                    frame_number += 1
                    pbar.update(1)
                    
                    # Actualizar descripción con golpes detectados
                    if frame_hits:
                        pbar.set_description(f"Analizando partido (Golpes: {len(self.hit_events)})")
        
        except Exception as e:
            print(f"Error durante el procesamiento: {e}")
            raise
        finally:
            cap.release()
        
        # Calcular estadísticas finales
        self._calculate_final_statistics()
        
        return self.match_stats
    
    def process_video_with_output(self, video_path: str, output_path: str = None) -> MatchStatistics:
        """
        Procesa un video y genera un video de salida con anotaciones visuales
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video no encontrado: {video_path}")
        
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            output_path = f"data/output_{base_name}_match_analyzed.mp4"
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"No se pudo abrir el video: {video_path}")
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        duration = total_frames / fps if fps > 0 else 0
        
        # Configurar video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        # Reiniciar estadísticas y estado interno
        self.hit_events.clear()
        self.last_hit_frame.clear()
        self.match_stats = MatchStatistics(
            total_frames=total_frames,
            video_duration=duration,
            fps=fps
        )
        
        print(f"Procesando video: {video_path}")
        print(f"Frames: {total_frames}, FPS: {fps:.2f}, Duración: {duration:.2f}s")
        print(f"Umbral de distancia: {self.hit_distance_threshold}px, Mínimo frames entre golpes: {self.min_frames_between_hits}")
        
        try:
            with tqdm(total=total_frames, desc="Analizando partido con output", unit="frames") as pbar:
                frame_number = 0
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    timestamp = frame_number / fps if fps > 0 else 0
                    
                    # Detectar jugadores y pelota
                    player_detections = self.player_detector.process_frame(frame)
                    ball_detections = self.ball_detector.process_frame(frame)
                    
                    # Detectar golpes en este frame
                    frame_hits = self._detect_hits_in_frame(frame, frame_number, timestamp)
                    self.hit_events.extend(frame_hits)
                    
                    # Crear frame anotado
                    annotated_frame = frame.copy()
                    
                    # Dibujar detecciones de jugadores
                    for player_detection in player_detections:
                        x1, y1, x2, y2 = map(int, player_detection.box)
                        player_id = int(player_detection.class_id)
                        confidence = player_detection.confidence
                        
                        # Color basado en el ID del jugador
                        color = (0, 255, 0) if player_id % 2 == 0 else (255, 0, 0)  # Verde o Azul
                        
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                        
                        label = f"Player {player_id} ({confidence:.2f})"
                        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                        cv2.rectangle(annotated_frame, (x1, y1 - label_size[1] - 10), 
                                    (x1 + label_size[0], y1), color, -1)
                        cv2.putText(annotated_frame, label, (x1, y1 - 5), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    
                    # Dibujar detecciones de pelota
                    for ball_detection in ball_detections:
                        x1, y1, x2, y2 = map(int, ball_detection.box)
                        confidence = ball_detection.confidence
                        
                        # Color rojo para la pelota
                        color = (0, 0, 255)  # BGR - Rojo
                        
                        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                        
                        label = f"Ball ({confidence:.2f})"
                        label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
                        cv2.rectangle(annotated_frame, (x1, y1 - label_size[1] - 10), 
                                    (x1 + label_size[0], y1), color, -1)
                        cv2.putText(annotated_frame, label, (x1, y1 - 5), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    
                    # Dibujar golpes detectados en este frame
                    for hit in frame_hits:
                        # Dibujar línea entre jugador y pelota
                        player_center_x = int((hit.player_box[0] + hit.player_box[2]) / 2)
                        player_center_y = int((hit.player_box[1] + hit.player_box[3]) / 2)
                        ball_center_x = int((hit.ball_box[0] + hit.ball_box[2]) / 2)
                        ball_center_y = int((hit.ball_box[1] + hit.ball_box[3]) / 2)
                        
                        # Línea amarilla para golpes
                        cv2.line(annotated_frame, (player_center_x, player_center_y), 
                               (ball_center_x, ball_center_y), (0, 255, 255), 3)
                        
                        # Texto de golpe
                        hit_text = f"HIT! Player {hit.player_id}"
                        cv2.putText(annotated_frame, hit_text, (10, 30), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
                    
                    # Agregar información del frame
                    frame_info = f"Frame: {frame_number} | Hits: {len(self.hit_events)}"
                    cv2.putText(annotated_frame, frame_info, (10, height - 20), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    
                    out.write(annotated_frame)
                    frame_number += 1
                    pbar.update(1)
                    
                    # Actualizar descripción con golpes detectados
                    if frame_hits:
                        pbar.set_description(f"Analizando partido (Golpes: {len(self.hit_events)})")
        
        except Exception as e:
            print(f"Error durante el procesamiento: {e}")
            raise
        finally:
            cap.release()
            out.release()
        
        # Calcular estadísticas finales
        self._calculate_final_statistics()
        
        print(f"Video procesado guardado en: {output_path}")
        return self.match_stats
    
    def _calculate_final_statistics(self) -> None:
        """
        Calcula las estadísticas finales basadas en los eventos de golpe detectados
        """
        self.match_stats.total_hits = len(self.hit_events)
        
        for hit in self.hit_events:
            player_id = hit.player_id
            if player_id not in self.match_stats.hits_per_player:
                self.match_stats.hits_per_player[player_id] = 0
            self.match_stats.hits_per_player[player_id] += 1

        return self.print_statistics()
    
    def get_hit_events(self) -> list[HitEvent]:
        return self.hit_events
    
    def print_statistics(self) -> None:
        """
        Imprime las estadísticas del partido de forma legible
        """
        print("\n" + "="*50)
        print("ESTADÍSTICAS DEL PARTIDO")
        print("="*50)
        print(f"Total de golpes detectados: {self.match_stats.total_hits}")
        print(f"Duración del video: {self.match_stats.video_duration:.2f} segundos")
        print(f"FPS: {self.match_stats.fps:.2f}")
        print(f"Total de frames: {self.match_stats.total_frames}")
        
        if self.match_stats.hits_per_player:
            print("\nGolpes por jugador:")
            for player_id, hits in self.match_stats.hits_per_player.items():
                print(f"  Jugador {player_id}: {hits} golpes")
        else:
            print("\nNo se detectaron golpes en este video.")
        
        print("="*50)

    