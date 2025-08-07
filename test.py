import cv2
from utils import read_video, save_video, measure_distance, convert_pixel_distance_to_meters, draw_player_stats
from trackers import PlayerTracker, BallTracker
from court_line_detector import CourtLineDetector
from mini_court import MiniCourt
import constants
import pandas as pd
from copy import deepcopy
from genai import analyze_tennis_video

def main():
    # Load video
    input_vid_path = 'videoplayback.mp4'
    frames = read_video(input_vid_path)

    # Initialize trackers and detectors
    player_tracker = PlayerTracker(model_path='models/yolo11x.pt')
    ball_tracker = BallTracker(model_path='models/yolo11v2_best.pt')
    court_model_path = 'models/keypoints_model_v5.pth'
    court_line_detector = CourtLineDetector(court_model_path)

    # Get initial court keypoints for player filtering
    initial_keypoints = court_line_detector.predict(frames[0])

    # Detect players
    player_detections = player_tracker.detect_frames(
        frames,
        read_from_stub=True,
        stub_path='tracker_stubs/player_detections.pkl'
    )
    
    # Filter players
    player_detections = player_tracker.choose_and_filter_players(
        initial_keypoints, 
        player_detections
    )

    # Detect ball frames
    ball_detections = ball_tracker.detect_frames(
        frames,
        read_from_stub=True,
        stub_path='tracker_stubs/ball_detections.pkl'
    )

    # Interpolate ball positions
    ball_detections = ball_tracker.interpolate_ball_positions(ball_detections)

    # Detect ball hits and get frame numbers with ball hits
    frame_nums_with_ball_hits, known_ball_positions = ball_tracker.detect_ball_hits(
        ball_detections,
        recompute=False  # Set to True if you want to recompute
    )
    ball_shot_frames = frame_nums_with_ball_hits

    # Initialize mini court
    mini_court = MiniCourt(frames[0])

    output_video_frames = []
    # Initialize lists to store mini court detections
    player_mini_court_detections = []
    ball_mini_court_detections = []

    for i, frame in enumerate(frames):
        # Write frame number
        cv2.putText(frame, f"Frame: {i}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Get court keypoints
        court_keypoints = court_line_detector.predict(frame, debug=(i == 0))
        
        # Draw court keypoints
        frame_with_keypoints = court_line_detector.draw_keypoints(frame.copy(), court_keypoints)

        # Draw players
        if i < len(player_detections):
            current_player_detections = [player_detections[i]]
            frame_with_keypoints = player_tracker.draw_bounding_boxes(
                [frame_with_keypoints],
                current_player_detections
            )[0]

        # Draw ball
        if i < len(ball_detections):
            current_ball_detections = [ball_detections[i]]
            frame_with_keypoints = ball_tracker.draw_bounding_boxes(
                [frame_with_keypoints],
                current_ball_detections
            )[0]

        # Draw mini court
        frame_with_mini = mini_court.draw_background_rectangle(frame_with_keypoints)
        frame_with_mini = mini_court.draw_court(frame_with_mini)

        # Convert current frame positions to mini court coordinates
        if i < len(player_detections) and i < len(ball_detections):
            try:
                mini_positions, mini_ball = mini_court.convert_bounding_boxes_to_mini_court_coordinates(
                    [player_detections[i]],  # Single frame
                    [ball_detections[i]],    # Single frame
                    court_keypoints
                )

                # Draw positions on mini court
                if mini_positions and mini_positions[0]:  # Check if we have valid positions
                    frame_with_mini = mini_court.draw_points_on_mini_court(
                        [frame_with_mini],
                        mini_positions,
                        color=(0, 255, 0)  # Green for players
                    )[0]
                    # Store player positions
                    player_positions_dict = {}
                    for player_id, position in mini_positions[0].items():  # Corrected iteration
                        player_positions_dict[player_id] = position
                    player_mini_court_detections.append(player_positions_dict)
                else:
                    player_mini_court_detections.append({})

                if mini_ball and mini_ball[0]:  # Check if we have valid ball position
                    ball_dict = mini_ball[0]  # This is {1: (x, y)}
                    positions_for_drawing = [ball_dict]  # Positions should be a list of dicts
                    frame_with_mini = mini_court.draw_points_on_mini_court(
                        [frame_with_mini],
                        positions_for_drawing,
                        color=(0, 0, 255)  # Red for ball
                    )[0]
                    # Store ball position
                    ball_position = list(ball_dict.values())[0]
                    ball_mini_court_detections.append(ball_position)
                else:
                    ball_mini_court_detections.append(None)
            except Exception as e:
                print(f"Error in frame {i}: {str(e)}")
                frame_with_mini = frame_with_keypoints
                player_mini_court_detections.append({})
                ball_mini_court_detections.append(None)  # Changed from {} to None
        else:
            player_mini_court_detections.append({})
            ball_mini_court_detections.append(None)  # Changed from {} to None

        output_video_frames.append(frame_with_mini)

        if i % 100 == 0:
            print(f"Processed frame {i + 1}/{len(frames)}")


    # Now that we have all detections, compute player statistics
    # Initialize player statistics data
    player_stats_data = [{
        'frame_num': 0,
        'player_1_number_of_shots': 0,
        'player_1_total_shot_speed': 0,
        'player_1_last_shot_speed': 0,
        'player_1_total_player_speed': 0,
        'player_1_last_player_speed': 0,
        'player_1_speed_measurements': 0,  # New counter

        'player_2_number_of_shots': 0,
        'player_2_total_shot_speed': 0,
        'player_2_last_shot_speed': 0,
        'player_2_total_player_speed': 0,
        'player_2_last_player_speed': 0,
        'player_2_speed_measurements': 0,  # New counter
    }]

    for ball_shot_ind in range(len(ball_shot_frames) - 1):
        start_frame = ball_shot_frames[ball_shot_ind]
        end_frame = ball_shot_frames[ball_shot_ind + 1]
        ball_shot_time_in_seconds = (end_frame - start_frame) / 30  # Assuming 24fps
        # Get distance covered by the ball
        try:
            ball_start = ball_mini_court_detections[start_frame]
            ball_end = ball_mini_court_detections[end_frame]

            # Check if both ball positions are available
            if ball_start is None or ball_end is None:
                print(f"Missing ball position at frame {start_frame} or {end_frame}")
                continue  # Skip if ball position is missing

            distance_covered_by_ball_pixels = measure_distance(ball_start, ball_end)
        except (KeyError, IndexError, ValueError) as e:
            print(f"Could not get or process ball positions at frames {start_frame} or {end_frame}: {e}")
            # Skip if ball position is missing or invalid
            continue

        # Convert distance from pixels to meters
        try:
            distance_covered_by_ball_meters = convert_pixel_distance_to_meters(
                distance_covered_by_ball_pixels,
                constants.DOUBLE_LINE_WIDTH,
                mini_court.get_width_of_mini_court()
            )
        except Exception as e:
            print(f"Error converting ball distance from pixels to meters: {e}")
            continue  # Skip if conversion fails

        # Calculate speed of the ball shot in km/h
        try:
            speed_of_ball_shot = (distance_covered_by_ball_meters / ball_shot_time_in_seconds) * 3.6
        except ZeroDivisionError:
            print("Time between shots is zero, cannot calculate speed.")
            continue  # Skip if time is zero to avoid division by zero

        # Identify the player who shot the ball
        try:
            if start_frame < len(player_mini_court_detections):
                player_positions = player_mini_court_detections[start_frame]
            else:
                player_positions = {}

            if not player_positions:
                print(f"No player positions at frame {start_frame}")
                continue  # Skip if player positions are missing

            # Ensure ball_position is available
            if start_frame < len(ball_mini_court_detections):
                ball_position = ball_mini_court_detections[start_frame]
            else:
                ball_position = None

            if ball_position is None:
                print(f"No ball position at frame {start_frame}")
                continue  # Skip if ball position is missing

            # Find the player closest to the ball position
            player_shot_ball = min(
                player_positions.keys(),
                key=lambda player_id: measure_distance(
                    player_positions[player_id],
                    ball_position
                )
            )
            print(f"Player {player_shot_ball} shot the ball")
        except ValueError as e:
            print(f"Error identifying player who shot the ball at frame {start_frame}: {e}")
            continue  # Skip if distance measurement fails
        except Exception as e:
            print(f"Unexpected error identifying player who shot the ball: {e}")
            continue  # Skip on any other unexpected errors

        # Opponent player ID
        opponent_player_id = 1 if player_shot_ball == 2 else 2

        # Calculate opponent's speed
        try:
            opponent_start_pos = player_positions.get(opponent_player_id)
            if end_frame < len(player_mini_court_detections):
                opponent_end_pos = player_mini_court_detections[end_frame].get(opponent_player_id)
            else:
                opponent_end_pos = None

            if opponent_start_pos is None or opponent_end_pos is None:
                print(f"Missing opponent (Player {opponent_player_id}) positions at frames {start_frame} or {end_frame}")
                continue  # Skip if opponent positions are missing

            distance_covered_by_opponent_pixels = measure_distance(opponent_start_pos, opponent_end_pos)

            # Convert opponent distance from pixels to meters
            distance_covered_by_opponent_meters = convert_pixel_distance_to_meters(
                distance_covered_by_opponent_pixels,
                constants.DOUBLE_LINE_WIDTH,
                mini_court.get_width_of_mini_court()
            )

            # Calculate opponent's speed in km/h
            speed_of_opponent = (distance_covered_by_opponent_meters / ball_shot_time_in_seconds) * 3.6
        except (KeyError, IndexError, ValueError) as e:
            continue  # Skip if opponent data is missing or invalid
        except Exception as e:
            continue  # Skip on any other unexpected errors

        # Measure speed of player who hit the ball
        try:
            player_shot_start_pos = player_positions.get(player_shot_ball)
            if end_frame < len(player_mini_court_detections):
                player_shot_end_pos = player_mini_court_detections[end_frame].get(player_shot_ball)
            else:
                player_shot_end_pos = None

            if player_shot_start_pos is None or player_shot_end_pos is None:
                speed_of_player_shot_ball = 0  # Set speed to zero if data is missing
            else:
                distance_covered_by_player_shot_pixels = measure_distance(player_shot_start_pos, player_shot_end_pos)

                # Convert player distance from pixels to meters
                distance_covered_by_player_shot_meters = convert_pixel_distance_to_meters(
                    distance_covered_by_player_shot_pixels,
                    constants.DOUBLE_LINE_WIDTH,
                    mini_court.get_width_of_mini_court()
                )

                # Calculate player's speed in km/h
                speed_of_player_shot_ball = (distance_covered_by_player_shot_meters / ball_shot_time_in_seconds) * 3.6
        except (KeyError, IndexError, ValueError) as e:
            speed_of_player_shot_ball = 0  # Set speed to zero if data is missing or invalid
        except Exception as e:
            speed_of_player_shot_ball = 0  # Set speed to zero on any other unexpected errors

        # Update player statistics
        current_player_stats = deepcopy(player_stats_data[-1])
        current_player_stats['frame_num'] = start_frame

        # Update stats for player who hit the ball
        current_player_stats[f'player_{player_shot_ball}_number_of_shots'] += 1
        current_player_stats[f'player_{player_shot_ball}_total_shot_speed'] += speed_of_ball_shot
        current_player_stats[f'player_{player_shot_ball}_last_shot_speed'] = speed_of_ball_shot

        current_player_stats[f'player_{player_shot_ball}_total_player_speed'] += speed_of_player_shot_ball
        current_player_stats[f'player_{player_shot_ball}_last_player_speed'] = speed_of_player_shot_ball
        current_player_stats[f'player_{player_shot_ball}_speed_measurements'] += 1

        # Update stats for opponent player
        current_player_stats[f'player_{opponent_player_id}_total_player_speed'] += speed_of_opponent
        current_player_stats[f'player_{opponent_player_id}_last_player_speed'] = speed_of_opponent
        current_player_stats[f'player_{opponent_player_id}_speed_measurements'] += 1

        player_stats_data.append(current_player_stats)

    # Create player statistics DataFrame
    player_stats_data_df = pd.DataFrame(player_stats_data)
    frames_df = pd.DataFrame({'frame_num': list(range(len(output_video_frames)))})
    player_stats_data_df = pd.merge(frames_df, player_stats_data_df, on='frame_num', how='left')
    player_stats_data_df = player_stats_data_df.ffill()

    # Compute average speeds, handling division by zero
    player_stats_data_df['player_1_average_shot_speed'] = player_stats_data_df.apply(
        lambda row: row['player_1_total_shot_speed'] / row['player_1_number_of_shots']
        if row['player_1_number_of_shots'] > 0 else 0, axis=1)
    player_stats_data_df['player_2_average_shot_speed'] = player_stats_data_df.apply(
        lambda row: row['player_2_total_shot_speed'] / row['player_2_number_of_shots']
        if row['player_2_number_of_shots'] > 0 else 0, axis=1)
    player_stats_data_df['player_1_average_player_speed'] = player_stats_data_df.apply(
        lambda row: row['player_1_total_player_speed'] / row['player_1_speed_measurements']
        if row['player_1_speed_measurements'] > 0 else 0, axis=1)
    player_stats_data_df['player_2_average_player_speed'] = player_stats_data_df.apply(
        lambda row: row['player_2_total_player_speed'] / row['player_2_speed_measurements']
        if row['player_2_speed_measurements'] > 0 else 0, axis=1)

    # Draw player statistics on frames
    output_video_frames = draw_player_stats(output_video_frames, player_stats_data_df)

    # Save video
    save_video(output_video_frames, 'output_files/sinner.avi')
    print("Video processing complete.")

    # Usage
    credentials_path = "rich-suprstate-442213-c5-7550f7495a7a.json"
    video_path = "output_files/sinner.avi"
    bucket_name = "tennis-data-marcoaloisi"
    analysis = analyze_tennis_video(video_path, credentials_path, bucket_name)
    print(analysis)


if __name__ == "__main__":
    main()
