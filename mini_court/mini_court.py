import cv2
import numpy as np
import sys
sys.path.append('../')
import constants
from utils import (
    convert_meters_to_pixel_distance,
    convert_pixel_distance_to_meters,
    get_foot_position,
    get_closest_keypoint_index,
    get_height_of_bbox,
    measure_xy_distance,
    get_center_of_bbox,
    measure_distance
)

class MiniCourt():
    def __init__(self,frame):
        self.drawing_rectangle_width = 250
        self.drawing_rectangle_height = 500
        self.buffer = 50
        self.padding_court=20
        self.previous_positions = []
        self.trail_length = 10
        self.smoothing_window = 5  # For position smoothing
        self.min_distance_threshold = 1  # Minimum distance to record new position

        self.set_canvas_background_box_position(frame)
        self.set_mini_court_position()
        self.set_court_drawing_key_points()
        self.set_court_lines()


    def convert_meters_to_pixels(self, meters):
        return convert_meters_to_pixel_distance(meters,
                                                constants.DOUBLE_LINE_WIDTH,
                                                self.court_drawing_width
                                            )

    def set_court_drawing_key_points(self):
        drawing_key_points = [0]*28

        # point 0 
        drawing_key_points[0] , drawing_key_points[1] = int(self.court_start_x), int(self.court_start_y)
        # point 1
        drawing_key_points[2] , drawing_key_points[3] = int(self.court_end_x), int(self.court_start_y)
        # point 2
        drawing_key_points[4] = int(self.court_start_x)
        drawing_key_points[5] = self.court_start_y + self.convert_meters_to_pixels(constants.HALF_COURT_LINE_HEIGHT*2)
        # point 3
        drawing_key_points[6] = drawing_key_points[0] + self.court_drawing_width
        drawing_key_points[7] = drawing_key_points[5] 
        # #point 4
        drawing_key_points[8] = drawing_key_points[0] +  self.convert_meters_to_pixels(constants.DOUBLE_ALLY_DIFFERENCE)
        drawing_key_points[9] = drawing_key_points[1] 
        # #point 5
        drawing_key_points[10] = drawing_key_points[4] + self.convert_meters_to_pixels(constants.DOUBLE_ALLY_DIFFERENCE)
        drawing_key_points[11] = drawing_key_points[5] 
        # #point 6
        drawing_key_points[12] = drawing_key_points[2] - self.convert_meters_to_pixels(constants.DOUBLE_ALLY_DIFFERENCE)
        drawing_key_points[13] = drawing_key_points[3] 
        # #point 7
        drawing_key_points[14] = drawing_key_points[6] - self.convert_meters_to_pixels(constants.DOUBLE_ALLY_DIFFERENCE)
        drawing_key_points[15] = drawing_key_points[7] 
        # #point 8
        drawing_key_points[16] = drawing_key_points[8] 
        drawing_key_points[17] = drawing_key_points[9] + self.convert_meters_to_pixels(constants.NO_MANS_LAND_HEIGHT)
        # # #point 9
        drawing_key_points[18] = drawing_key_points[16] + self.convert_meters_to_pixels(constants.SINGLE_LINE_WIDTH)
        drawing_key_points[19] = drawing_key_points[17] 
        # #point 10
        drawing_key_points[20] = drawing_key_points[10] 
        drawing_key_points[21] = drawing_key_points[11] - self.convert_meters_to_pixels(constants.NO_MANS_LAND_HEIGHT)
        # # #point 11
        drawing_key_points[22] = drawing_key_points[20] +  self.convert_meters_to_pixels(constants.SINGLE_LINE_WIDTH)
        drawing_key_points[23] = drawing_key_points[21] 
        # # #point 12
        drawing_key_points[24] = int((drawing_key_points[16] + drawing_key_points[18])/2)
        drawing_key_points[25] = drawing_key_points[17] 
        # # #point 13
        drawing_key_points[26] = int((drawing_key_points[20] + drawing_key_points[22])/2)
        drawing_key_points[27] = drawing_key_points[21] 

        self.drawing_key_points=drawing_key_points

    def set_court_lines(self):
        self.lines = [
            (0, 2),
            (4, 5),
            (6,7),
            (1,3),
            
            (0,1),
            (8,9),
            (10,11),
            (10,11),
            (2,3)
        ]

    def set_mini_court_position(self):
        self.court_start_x = self.start_x + self.padding_court
        self.court_start_y = self.start_y + self.padding_court
        self.court_end_x = self.end_x - self.padding_court
        self.court_end_y = self.end_y - self.padding_court
        self.court_drawing_width = self.court_end_x - self.court_start_x

    def set_canvas_background_box_position(self,frame):
        frame= frame.copy()

        self.end_x = frame.shape[1] - self.buffer
        self.end_y = self.buffer + self.drawing_rectangle_height
        self.start_x = self.end_x - self.drawing_rectangle_width
        self.start_y = self.end_y - self.drawing_rectangle_height

    def draw_court(self, frame):
        # Set court background color to blue
        court_color = (191, 147, 101)  # Blue in BGR
        cv2.rectangle(frame, (self.start_x, self.start_y), (self.end_x, self.end_y), court_color, -1)

        # Draw keypoints
        for i in range(0, len(self.drawing_key_points), 2):
            x = int(self.drawing_key_points[i])
            y = int(self.drawing_key_points[i + 1])
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)  # Red for keypoints

        # Draw lines with white color
        line_color = (255, 255, 255)  # White
        for line in self.lines:
            start_point = (int(self.drawing_key_points[line[0] * 2]), int(self.drawing_key_points[line[0] * 2 + 1]))
            end_point = (int(self.drawing_key_points[line[1] * 2]), int(self.drawing_key_points[line[1] * 2 + 1]))
            cv2.line(frame, start_point, end_point, line_color, 2)

        # Draw the middle net line in red
        net_start_point = (int(self.drawing_key_points[0]), int((self.drawing_key_points[1] + self.drawing_key_points[5]) / 2))
        net_end_point = (int(self.drawing_key_points[2]), int((self.drawing_key_points[1] + self.drawing_key_points[5]) / 2))
        cv2.line(frame, net_start_point, net_end_point, (0, 0, 255), 2)  # Red

        return frame

    def draw_background_rectangle(self,frame):
        shapes = np.zeros_like(frame,np.uint8)
        # Draw the rectangle
        cv2.rectangle(shapes, (self.start_x, self.start_y), (self.end_x, self.end_y), (255, 255, 255), cv2.FILLED)
        out = frame.copy()
        alpha=0.5
        mask = shapes.astype(bool)
        out[mask] = cv2.addWeighted(frame, alpha, shapes, 1 - alpha, 0)[mask]

        return out

    def draw_mini_court(self,frames):
        output_frames = []
        for frame in frames:
            frame = self.draw_background_rectangle(frame)
            frame = self.draw_court(frame)
            output_frames.append(frame)
        return output_frames

    def get_start_point_of_mini_court(self):
        return (self.court_start_x,self.court_start_y)
    def get_width_of_mini_court(self):
        return self.court_drawing_width
    def get_court_drawing_keypoints(self):
        return self.drawing_key_points

    def get_mini_court_coordinates(self,
                                object_position,
                                closest_key_point, 
                                closest_key_point_index, 
                                player_height_in_pixels,
                                player_height_in_meters
                                ):
        
        # Get relative distances from the closest keypoint
        distance_from_keypoint_x_pixels, distance_from_keypoint_y_pixels = measure_xy_distance(object_position, closest_key_point)

        # Add perspective correction based on y-position
        # Objects higher in the frame (smaller y) appear more distorted
        perspective_factor = 1.0
        if object_position[1] < closest_key_point[1]:
            # Object is above the reference point
            y_diff = closest_key_point[1] - object_position[1]
            perspective_factor = 1.0 + (y_diff / 1000.0)  # Adjust divisor to tune correction
        
        # Apply perspective correction to x distance
        corrected_x_pixels = distance_from_keypoint_x_pixels * perspective_factor

        # Convert distances to meters using player height as reference
        distance_from_keypoint_x_meters = convert_pixel_distance_to_meters(
            corrected_x_pixels,
            player_height_in_meters,
            player_height_in_pixels
        )
        distance_from_keypoint_y_meters = convert_pixel_distance_to_meters(
            distance_from_keypoint_y_pixels,
            player_height_in_meters,
            player_height_in_pixels
        )

        # Convert back to mini court pixels
        mini_court_x_distance_pixels = self.convert_meters_to_pixels(distance_from_keypoint_x_meters)
        mini_court_y_distance_pixels = self.convert_meters_to_pixels(distance_from_keypoint_y_meters)

        # Get the reference point in mini court coordinates
        closest_mini_court_keypoint = (
            self.drawing_key_points[closest_key_point_index*2],
            self.drawing_key_points[closest_key_point_index*2+1]
        )

        # Apply direction correction based on which side of the keypoint the object is
        x_direction = 1 if object_position[0] > closest_key_point[0] else -1
        y_direction = 1 if object_position[1] > closest_key_point[1] else -1

        # Calculate final position with direction
        mini_court_position = (
            closest_mini_court_keypoint[0] + (x_direction * mini_court_x_distance_pixels),
            closest_mini_court_keypoint[1] + (y_direction * mini_court_y_distance_pixels)
        )

        # Add boundary checking to keep points within the mini court
        mini_court_position = (
            max(self.court_start_x, min(self.court_end_x, mini_court_position[0])),
            max(self.court_start_y, min(self.court_end_y, mini_court_position[1]))
        )

        return mini_court_position

    def convert_bounding_boxes_to_mini_court_coordinates(self, player_boxes, ball_boxes, original_court_key_points):
        player_heights = {
            1: constants.PLAYER_1_HEIGHT_METERS,
            2: constants.PLAYER_2_HEIGHT_METERS
        }

        output_player_boxes = []
        output_ball_boxes = []

        # Calculate court dimensions and midpoint
        court_top = original_court_key_points[1]  
        court_bottom = original_court_key_points[5]  
        court_left = original_court_key_points[0]  
        court_right = original_court_key_points[2] 
        court_mid_y = (court_top + court_bottom) / 2

        for frame_num, player_bbox in enumerate(player_boxes):
            ball_box = ball_boxes[frame_num][1]
            ball_position = get_center_of_bbox(ball_box)
            closest_player_id_to_ball = min(player_bbox.keys(), 
                                        key=lambda x: measure_distance(ball_position, get_center_of_bbox(player_bbox[x])))

            output_player_bboxes_dict = {}
            for player_id, bbox in player_bbox.items():
                foot_position = get_foot_position(bbox)

                # Get The closest keypoint in pixels for players - using baseline corners
                closest_key_point_index = get_closest_keypoint_index(foot_position, 
                                                                original_court_key_points, 
                                                                [0, 1, 2, 3])  # Baseline corners
                closest_key_point = (original_court_key_points[closest_key_point_index*2], 
                                original_court_key_points[closest_key_point_index*2+1])

                # Calculate player positions
                frame_index_min = max(0, frame_num-20)
                frame_index_max = min(len(player_boxes), frame_num+50)
                bboxes_heights_in_pixels = [get_height_of_bbox(player_boxes[i][player_id]) 
                                        for i in range(frame_index_min, frame_index_max)]
                max_player_height_in_pixels = max(bboxes_heights_in_pixels)

                mini_court_player_position = self.get_mini_court_coordinates(
                    foot_position,
                    closest_key_point, 
                    closest_key_point_index, 
                    max_player_height_in_pixels,
                    player_heights[player_id]
                )
                
                output_player_bboxes_dict[player_id] = mini_court_player_position

                if closest_player_id_to_ball == player_id:
                    ball_x, ball_y = ball_position
                    
                    # Determine reference points based on ball location
                    if ball_y < court_mid_y:
                        # Ball is in top half
                        if ball_x < (court_left + court_right) / 2:
                            # Top left quadrant - use points 4 (doubles alley) and 8 (service line)
                            reference_points = [4, 8]
                        else:
                            # Top right quadrant - use points 6 (doubles alley) and 9 (service line)
                            reference_points = [6, 9]
                    else:
                        # Ball is in bottom half
                        if ball_x < (court_left + court_right) / 2:
                            # Bottom left quadrant - use points 5 (doubles alley) and 10 (service line)
                            reference_points = [5, 10]
                        else:
                            # Bottom right quadrant - use points 7 (doubles alley) and 11 (service line)
                            reference_points = [7, 11]

                    closest_key_point_index = get_closest_keypoint_index(
                        ball_position,
                        original_court_key_points, 
                        reference_points
                    )
                    closest_key_point = (original_court_key_points[closest_key_point_index*2], 
                                    original_court_key_points[closest_key_point_index*2+1])
                    
                    mini_court_ball_position = self.get_mini_court_coordinates(
                        ball_position,
                        closest_key_point, 
                        closest_key_point_index, 
                        max_player_height_in_pixels,
                        player_heights[player_id]
                    )
                    
                    output_ball_boxes.append({1: mini_court_ball_position})
                    
            output_player_boxes.append(output_player_bboxes_dict)

        return output_player_boxes, output_ball_boxes
    
    def smooth_position(self, new_pos):
        """Apply smoothing to the ball position"""
        if not self.previous_positions:
            return new_pos
            
        # Get recent positions for smoothing
        recent_positions = self.previous_positions[-self.smoothing_window:]
        if not recent_positions:
            return new_pos
            
        # Calculate weighted average of recent positions
        weights = [i/len(recent_positions) for i in range(1, len(recent_positions) + 1)]
        sum_weights = sum(weights)
        
        smoothed_x = sum(p[0] * w for p, w in zip(recent_positions, weights)) / sum_weights
        smoothed_y = sum(p[1] * w for p, w in zip(recent_positions, weights)) / sum_weights
        
        # Blend with new position
        alpha = 0.7  # Smoothing factor
        final_x = int((1 - alpha) * smoothed_x + alpha * new_pos[0])
        final_y = int((1 - alpha) * smoothed_y + alpha * new_pos[1])
        
        return (final_x, final_y)

    def draw_points_on_mini_court(self, frames, positions, color=(0,255,0)):
        output_frames = []
        player_names = {1: "Sinner", 2: "Medvedev"}

        for frame_num, frame in enumerate(frames):
            frame_copy = frame.copy()
            
            for player_id, position in positions[frame_num].items():
                x, y = position
                x, y = int(x), int(y)
                
                if color == (0, 0, 255):  # Ball drawing
                    # Apply smoothing
                    smooth_pos = self.smooth_position((x, y))
                    x, y = smooth_pos
                    
                    # Only add position if it's significantly different
                    if not self.previous_positions or measure_distance(
                        self.previous_positions[-1], (x, y)) > self.min_distance_threshold:
                        self.previous_positions.append((x, y))
                    
                    # Maintain trail length
                    while len(self.previous_positions) > self.trail_length:
                        self.previous_positions.pop(0)
                    
                    # Draw trail with enhanced interpolation
                    if len(self.previous_positions) > 1:
                        # Draw connecting lines with gradient effect
                        for i in range(1, len(self.previous_positions)):
                            alpha = i / len(self.previous_positions)
                            pt1 = self.previous_positions[i-1]
                            pt2 = self.previous_positions[i]
                            
                            # Gradient color from light to more intense
                            color_intensity = int(200 * alpha)
                            line_color = (0, color_intensity, color_intensity)
                            
                            # Thicker lines for more recent positions
                            thickness = max(1, int(3 * alpha))
                            cv2.line(frame_copy, pt1, pt2, line_color, thickness)
                    
                    # Outer glow
                    cv2.circle(frame_copy, (x, y), 8, (255, 255, 255), -1)
                    # Ball color
                    cv2.circle(frame_copy, (x, y), 6, (0, 0, 255), -1)
                    # Inner highlight
                    cv2.circle(frame_copy, (x-1, y-1), 2, (255, 255, 255), -1)
                else:
                    # Player positions
                    cv2.circle(frame_copy, (x, y), 5, color, -1)
                    player_name = player_names.get(player_id, f"Player {player_id}")
                    cv2.putText(frame_copy, player_name, (x + 10, y - 10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            output_frames.append(frame_copy)
        
        return output_frames