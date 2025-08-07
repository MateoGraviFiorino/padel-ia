import cv2
import numpy as np
import os
from ultralytics import YOLO
import pickle
import pandas as pd
from scipy.signal import savgol_filter
from collections import deque
from scipy.interpolate import UnivariateSpline
from matplotlib import pyplot as plt
import sys
sys.path.append('../')
from utils import get_center_of_bbox, measure_distance

class BallTracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.window_size = 5
        self.trajectory_points = []
        self.max_interp_distance = 144
        self.max_velocity = 80
        self.ball_hits_path = 'tracker_stubs/frame_nums_with_ball_hits.pkl'
        self.known_positions_path = 'tracker_stubs/known_ball_positions.pkl'

    def plot_trajectory(self, centers):
        x = np.arange(len(centers))
        y = [center[1] if center is not None else np.nan for center in centers]

        plt.figure(figsize=(12, 6))
        plt.plot(x, y, label='Trajectory')
        plt.xlabel('Frame')
        plt.ylabel('Y Position')
        plt.title('Ball Trajectory')
        plt.show()

    def plot_velocities(self, centers):
        velocities = []
        frames = []
        for i in range(1, len(centers)):
            if centers[i - 1] is not None and centers[i] is not None:
                velocity = self.calculate_velocity(centers[i - 1], centers[i])
                velocities.append(velocity)
                frames.append(i)

        plt.figure(figsize=(12, 6))
        plt.plot(frames, velocities, label='Velocity')
        plt.xlabel('Frame')
        plt.ylabel('Velocity')
        plt.title('Ball Velocity')
        plt.show()

    def detect_ball_hits(self, ball_positions, minimum_change_frames_for_hit=25, recompute=False):

        if not recompute and os.path.exists(self.ball_hits_path) and os.path.exists(self.known_positions_path):
            with open(self.ball_hits_path, 'rb') as f:
                frame_nums_with_ball_hits = pickle.load(f)
            with open(self.known_positions_path, 'rb') as f:
                known_ball_positions = pickle.load(f)
            return frame_nums_with_ball_hits, known_ball_positions

        # Convert ball_positions to DataFrame
        ball_positions_list = [pos_dict.get(1, []) for pos_dict in ball_positions]
        df_ball_positions = pd.DataFrame(ball_positions_list, columns=['x1', 'y1', 'x2', 'y2'])

        # Interpolate missing values
        df_ball_positions = df_ball_positions.interpolate()
        df_ball_positions = df_ball_positions.bfill()

        # Compute mid_y, mid_y_rolling_mean, and delta_y
        df_ball_positions['mid_y'] = (df_ball_positions['y1'] + df_ball_positions['y2']) / 2
        df_ball_positions['mid_y_rolling_mean'] = df_ball_positions['mid_y'].rolling(window=5, min_periods=1).mean()
        df_ball_positions['delta_y'] = df_ball_positions['mid_y_rolling_mean'].diff().fillna(0)

        # Initialize 'ball_hit' column
        df_ball_positions['ball_hit'] = 0

        # Detect ball hits based on delta_y
        for i in range(1, len(df_ball_positions) - int(minimum_change_frames_for_hit * 1.2)):
            negative_position_change = (
                df_ball_positions['delta_y'].iloc[i] > 0 and df_ball_positions['delta_y'].iloc[i + 1] < 0
            )
            positive_position_change = (
                df_ball_positions['delta_y'].iloc[i] < 0 and df_ball_positions['delta_y'].iloc[i + 1] > 0
            )
            if negative_position_change or positive_position_change:
                change_count = 0
                for change_frame in range(i + 1, min(i + int(minimum_change_frames_for_hit * 1.2) + 1, len(df_ball_positions))):
                    negative_position_change_following_frame = (
                        df_ball_positions['delta_y'].iloc[i] > 0
                        and df_ball_positions['delta_y'].iloc[change_frame] < 0
                    )
                    positive_position_change_following_frame = (
                        df_ball_positions['delta_y'].iloc[i] < 0
                        and df_ball_positions['delta_y'].iloc[change_frame] > 0
                    )
                    if negative_position_change and negative_position_change_following_frame:
                        change_count += 1
                    elif positive_position_change and positive_position_change_following_frame:
                        change_count += 1
                if change_count > minimum_change_frames_for_hit - 1:
                    df_ball_positions.loc[i, 'ball_hit'] = 1

        
        # Define the specific values for x1 and y1 to drop
        x1_value = 1288.377650
        y1_value = 647.037925

        # Use np.isclose for floating-point comparison
        df_ball_positions = df_ball_positions[
        ~((np.isclose(df_ball_positions['x1'], x1_value)) & (np.isclose(df_ball_positions['y1'], y1_value)))]

        # Extract frame numbers with ball hits
        frame_nums_with_ball_hits = df_ball_positions[df_ball_positions['ball_hit'] == 1].index.tolist()

        # Prepare known ball positions
        known_ball_positions = {}
        for frame_num in frame_nums_with_ball_hits:
            row = df_ball_positions.loc[frame_num]
            x1, y1, x2, y2 = row['x1'], row['y1'], row['x2'], row['y2']
            known_ball_positions[frame_num] = [x1, y1, x2, y2]

        # Save the data to stubs
        with open(self.ball_hits_path, 'wb') as f:
            pickle.dump(frame_nums_with_ball_hits, f)
        with open(self.known_positions_path, 'wb') as f:
            pickle.dump(known_ball_positions, f)

        return frame_nums_with_ball_hits, known_ball_positions

    def calculate_velocity(self, p1, p2):
        """Calculate velocity between two points"""
        if p1 is None or p2 is None:
            return float('inf')
        return measure_distance(p1, p2)

    def compute_velocity_statistics(self, centers):
        velocities = []
        for i in range(1, len(centers)):
            if centers[i - 1] is not None and centers[i] is not None:
                velocity = self.calculate_velocity(centers[i - 1], centers[i])
                velocities.append(velocity)
        if velocities:
            mean_velocity = np.mean(velocities)
            std_velocity = np.std(velocities)
            median_velocity = np.median(velocities)
            percentile_95 = np.percentile(velocities, 95)
            return mean_velocity, std_velocity, median_velocity, percentile_95
        else:
            return None, None, None, None

    def is_outlier_angle(self, prev_point, current_point, next_point):
        if prev_point is None or current_point is None or next_point is None:
            return False

        # Vectors between points
        v1 = np.array([current_point[0] - prev_point[0], current_point[1] - prev_point[1]])
        v2 = np.array([next_point[0] - current_point[0], next_point[1] - current_point[1]])

        # Compute angle between vectors
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        if norm_v1 == 0 or norm_v2 == 0:
            return False  # Cannot compute angle with zero-length vector

        cos_theta = dot_product / (norm_v1 * norm_v2)
        angle = np.arccos(np.clip(cos_theta, -1.0, 1.0))

        # Threshold angle (in radians), e.g., 150 degrees
        angle_threshold = np.deg2rad(150)

        if angle > angle_threshold:
            return True
        else:
            return False

    def is_outlier(self, prev_point, current_point, next_point, mean_vel, std_vel, frame_idx, ball_hit_frames):
        if prev_point is None or current_point is None or next_point is None:
            return False

        if frame_idx in ball_hit_frames:
            return False  # Do not consider ball hit frames as outliers

        # Velocity check
        vel1 = self.calculate_velocity(prev_point, current_point)
        vel2 = self.calculate_velocity(current_point, next_point)

        if (vel1 > mean_vel + 2 * std_vel) and (vel2 > mean_vel + 2 * std_vel):
            return True

        # Angle check
        if self.is_outlier_angle(prev_point, current_point, next_point):
            return True

        return False

    def smooth_trajectory(self, ball_positions, ball_hit_frames=None):
        if ball_hit_frames is None:
            ball_hit_frames = []

        centers = []
        valid_indices = []
        xs = []
        ys = []

        # Collect valid detections
        for idx, pos_dict in enumerate(ball_positions):
            if 1 in pos_dict:
                center = get_center_of_bbox(pos_dict[1])
                centers.append(center)
                valid_indices.append(idx)
                xs.append(idx)
                ys.append(center[1])  # Use vertical position for interpolation
            else:
                centers.append(None)

        # Compute Velocity Statistics
        mean_vel, std_vel, median_vel, percentile_95_vel = self.compute_velocity_statistics(centers)
        if mean_vel is None or std_vel is None:
            mean_vel = self.max_velocity
            std_vel = 0

        # First pass: Remove obvious outliers
        filtered_centers = centers.copy()
        window_size = 5  # Increased window size for better context

        for i in range(window_size, len(centers) - window_size):
            if centers[i] is not None:
                # Skip ball hit frames
                if i in ball_hit_frames:
                    continue

                # Get window of points
                window = centers[i-window_size:i+window_size+1]
                valid_points = [p for p in window if p is not None]

                if len(valid_points) >= 3:
                    # Calculate median position in window
                    median_y = np.median([p[1] for p in valid_points])
                    current_y = centers[i][1]

                    # Check for vertical position consistency
                    max_vertical_deviation = 100  # pixels
                    if abs(current_y - median_y) > max_vertical_deviation:
                        filtered_centers[i] = None
                        if i in valid_indices:
                            valid_indices.remove(i)

                    # Check for acceleration consistency
                    if i > 0 and i < len(centers) - 1 and centers[i-1] is not None and centers[i+1] is not None:
                        v1 = self.calculate_velocity(centers[i-1], centers[i])
                        v2 = self.calculate_velocity(centers[i], centers[i+1])
                        acceleration = abs(v2 - v1)
                        max_acceleration = 50  # maximum allowed acceleration
                        if acceleration > max_acceleration:
                            filtered_centers[i] = None
                            if i in valid_indices:
                                valid_indices.remove(i)

        # Update centers and indices
        centers = filtered_centers
        xs = [i for i in valid_indices]
        ys = [filtered_centers[i][1] for i in valid_indices]

        # Store original valid indices and centers
        valid_xs = xs.copy()
        valid_centers_x = [filtered_centers[i][0] for i in valid_indices]

        # Enhanced spline interpolation with physical constraints
        if len(xs) >= 4:  # Need at least 4 points for cubic spline
            # Separate x and y interpolation
            spline_y = UnivariateSpline(xs, ys, k=3, s=len(xs)*0.1)  # Allowing some smoothing

            for idx in range(len(centers)):
                if centers[idx] is None:
                    # Skip ball hit frames
                    if idx in ball_hit_frames:
                        continue

                    # Find nearest valid points
                    prev_valid = next((i for i in range(idx-1, -1, -1) if i in valid_indices), None)
                    next_valid = next((i for i in range(idx+1, len(centers)) if i in valid_indices), None)

                    if prev_valid is not None and next_valid is not None:
                        # Only interpolate if gap is not too large
                        gap_size = next_valid - prev_valid
                        if gap_size <= 10:  # Maximum allowed gap for interpolation
                            interp_y = spline_y(idx)
                            interp_x = np.interp(idx, [prev_valid, next_valid],
                                                 [centers[prev_valid][0], centers[next_valid][0]])
                            centers[idx] = (interp_x, interp_y)
        else:
            # Fallback to linear interpolation if not enough points
            for idx in range(len(centers)):
                if centers[idx] is None:
                    # Skip ball hit frames
                    if idx in ball_hit_frames:
                        continue

                    # Find previous and next valid indices
                    prev_idx = next((i for i in range(idx - 1, -1, -1) if centers[i] is not None), None)
                    next_idx = next((i for i in range(idx + 1, len(centers)) if centers[i] is not None), None)
                    if prev_idx is not None and next_idx is not None:
                        alpha = (idx - prev_idx) / (next_idx - prev_idx)
                        interp_x = centers[prev_idx][0] + alpha * (centers[next_idx][0] - centers[prev_idx][0])
                        interp_y = centers[prev_idx][1] + alpha * (centers[next_idx][1] - centers[prev_idx][1])
                        centers[idx] = (interp_x, interp_y)

        # Final smoothing pass
        xs_full = [center[0] if center is not None else np.nan for center in centers]
        ys_full = [center[1] if center is not None else np.nan for center in centers]

        # Convert to arrays and handle NaNs
        xs_full = np.array(xs_full)
        ys_full = np.array(ys_full)

        # Replace NaNs with interpolated values
        nans_x = np.isnan(xs_full)
        nans_y = np.isnan(ys_full)
        not_nans = ~nans_x  # Assuming xs_full and ys_full have NaNs at the same positions

        if np.any(nans_x):
            xs_full[nans_x] = np.interp(np.flatnonzero(nans_x), np.flatnonzero(not_nans), xs_full[not_nans])
        if np.any(nans_y):
            ys_full[nans_y] = np.interp(np.flatnonzero(nans_y), np.flatnonzero(not_nans), ys_full[not_nans])

        # Apply Savitzky-Golay with optimized parameters
        window_size = min(15, len(xs_full) // 2 * 2 + 1)
        if len(xs_full) >= window_size:
            smooth_xs = savgol_filter(xs_full, window_size, 3, mode='nearest')
            smooth_ys = savgol_filter(ys_full, window_size, 3, mode='nearest')

            # Additional physics-based smoothing
            velocities = np.sqrt(np.diff(smooth_xs)**2 + np.diff(smooth_ys)**2)
            velocity_mask = velocities > self.max_velocity
            if np.any(velocity_mask):
                # Reinterpolate points with excessive velocity
                problem_indices = np.where(velocity_mask)[0] + 1
                for idx in problem_indices:
                    if idx > 0 and idx < len(centers) - 1:
                        smooth_xs[idx] = (smooth_xs[idx-1] + smooth_xs[idx+1]) / 2
                        smooth_ys[idx] = (smooth_ys[idx-1] + smooth_ys[idx+1]) / 2
        else:
            smooth_xs = xs_full
            smooth_ys = ys_full

        centers = list(zip(smooth_xs, smooth_ys))

        # Reconstruct smoothed positions
        smoothed_positions = []
        for idx, center in enumerate(centers):
            if center is not None and not np.isnan(center[0]) and not np.isnan(center[1]):
                # Use average box size or previous valid box size
                box_width = box_height = 10  # Default size
                if valid_indices:
                    # Find the last valid index before or at idx
                    previous_valid_indices = [i for i in valid_indices if i <= idx]
                    if previous_valid_indices:
                        last_valid_idx = previous_valid_indices[-1]
                    else:
                        # No valid indices before idx, use the next valid index
                        next_valid_indices = [i for i in valid_indices if i > idx]
                        if next_valid_indices:
                            last_valid_idx = next_valid_indices[0]
                        else:
                            last_valid_idx = valid_indices[0]  # Use the first valid index
                    last_box = ball_positions[last_valid_idx][1]
                    box_width = last_box[2] - last_box[0]
                    box_height = last_box[3] - last_box[1]

                smoothed_positions.append({1: [
                    center[0] - box_width / 2,
                    center[1] - box_height / 2,
                    center[0] + box_width / 2,
                    center[1] + box_height / 2
                ]})
            else:
                smoothed_positions.append({})

        self.plot_trajectory(centers)
        self.plot_velocities(centers)

        return smoothed_positions

    def detect_frames(self, frames, read_from_stub=False, stub_path=None, ball_hit_frames=None, known_ball_positions=None):
        if read_from_stub and stub_path is not None:
            with open(stub_path, 'rb') as f:
                return pickle.load(f)

        if ball_hit_frames is None or known_ball_positions is None:
            # Load ball_hit_frames and known_ball_positions internally
            if os.path.exists(self.ball_hits_path) and os.path.exists(self.known_positions_path):
                with open(self.ball_hits_path, 'rb') as f:
                    ball_hit_frames = pickle.load(f)
                with open(self.known_positions_path, 'rb') as f:
                    known_ball_positions = pickle.load(f)
            else:
                # If they don't exist, detect ball hits first
                _, _ = self.detect_ball_hits([])
                with open(self.ball_hits_path, 'rb') as f:
                    ball_hit_frames = pickle.load(f)
                with open(self.known_positions_path, 'rb') as f:
                    known_ball_positions = pickle.load(f)

        ball_detections = []
        for i, frame in enumerate(frames):
            results = self.model.track(frame, conf=0.15)[0]
            ball_dict = {}

            highest_conf = 0
            best_detection = None
            for box in results.boxes:
                conf = float(box.conf)
                if conf > highest_conf:
                    highest_conf = conf
                    best_detection = box.xyxy.tolist()[0]

            if best_detection is not None:
                ball_dict[1] = best_detection
            else:
                # If no detection and frame is in ball_hit_frames, use known ball position
                if i in ball_hit_frames and i in known_ball_positions:
                    ball_dict[1] = known_ball_positions[i]

            ball_detections.append(ball_dict)

        ball_detections = self.smooth_trajectory(ball_detections, ball_hit_frames=ball_hit_frames)

        if stub_path is not None:
            with open(stub_path, 'wb') as f:
                pickle.dump(ball_detections, f)

        return ball_detections

    def interpolate_ball_positions(self, ball_positions, ball_hit_frames=None):
        if ball_hit_frames is None:
            # Load ball_hit_frames internally
            if os.path.exists(self.ball_hits_path):
                with open(self.ball_hits_path, 'rb') as f:
                    ball_hit_frames = pickle.load(f)
            else:
                # If ball hits have not been detected yet, run detect_ball_hits
                ball_positions, _ = self.detect_ball_hits(ball_positions)
                with open(self.ball_hits_path, 'rb') as f:
                    ball_hit_frames = pickle.load(f)
        return self.smooth_trajectory(ball_positions, ball_hit_frames=ball_hit_frames)


    def draw_bounding_boxes(self, video_frames, ball_detections):
        output_frames = []

        for frame, ball_dict in zip(video_frames, ball_detections):
            # Update trajectory points with the current detection
            if 1 in ball_dict:
                center = get_center_of_bbox(ball_dict[1])
                self.trajectory_points.append(center)

            # Limit the trajectory to the last 30 points
            self.trajectory_points = self.trajectory_points[-20:]

            # Draw the trajectory lines
            if len(self.trajectory_points) > 1:
                for i in range(1, len(self.trajectory_points)):
                    cv2.line(
                        frame,
                        self.trajectory_points[i - 1],
                        self.trajectory_points[i],
                        (0, 255, 0),
                        2
                    )

            output_frames.append(frame)

        return output_frames
