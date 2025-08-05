import cv2
import numpy as np
import time
from pose_detector import PoseDetector
from yoga_analyzer import YogaAnalyzer
from voice_guide import VoiceGuide


def draw_ui_elements(frame, analysis_result, target_pose, pose_list, current_pose_index):
    """Draw UI elements on the frame"""
    height, width = frame.shape[:2]
    
    # Create semi-transparent overlay for UI
    overlay = frame.copy()
    
    # Draw pose selection area
    cv2.rectangle(overlay, (10, 10), (400, 120), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
    
    # Current pose info
    pose_name = target_pose.replace('_', ' ').title()
    cv2.putText(frame, f"Current Pose: {pose_name}", (20, 40), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Score display
    score = analysis_result.get('score', 0)
    score_color = (0, 255, 0) if score >= 80 else (0, 255, 255) if score >= 60 else (0, 0, 255)
    cv2.putText(frame, f"Score: {score}/100", (20, 70), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, score_color, 2)
    
    # Instructions
    cv2.putText(frame, "Press 'n' for next pose, 'p' for previous, 'q' to quit", (20, 100), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    # Feedback area
    if analysis_result.get('pose_detected', False):
        feedback = analysis_result.get('feedback', '')
        corrections = analysis_result.get('corrections', [])
        
        # Draw feedback box
        feedback_y = height - 150
        cv2.rectangle(overlay, (10, feedback_y - 30), (width - 10, height - 10), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Main feedback
        cv2.putText(frame, "Feedback:", (20, feedback_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Wrap feedback text
        words = feedback.split(' ')
        line = ""
        y_offset = feedback_y + 25
        
        for word in words:
            test_line = line + word + " "
            if len(test_line) > 60:  # Approximate character limit per line
                cv2.putText(frame, line, (20, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                line = word + " "
                y_offset += 20
            else:
                line = test_line
        
        if line:
            cv2.putText(frame, line, (20, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Show corrections
        if corrections:
            y_offset += 25
            cv2.putText(frame, "Corrections:", (20, y_offset), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)
            y_offset += 20
            
            for correction in corrections[:2]:  # Show max 2 corrections
                cv2.putText(frame, f"• {correction}", (30, y_offset), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)
                y_offset += 18
    
    return frame


def main():
    print("Starting AI Yoga Instructor...")
    print("Make sure you have a webcam connected and positioned to see your full body.")
    
    # Initialize modules
    try:
        detector = PoseDetector()
        analyzer = YogaAnalyzer()
        voice_guide = VoiceGuide()
        print("✓ Modules initialized successfully")
    except Exception as e:
        print(f"Error initializing modules: {e}")
        return

    # Available poses - 5 asanas
    pose_list = ['mountain', 'tree', 'sukasana', 'childs_pose', 'warrior2']
    current_pose_index = 0
    target_pose = pose_list[current_pose_index]

    # Start capturing from webcam
    video_capture = cv2.VideoCapture(0)

    if not video_capture.isOpened():
        print("Error: Could not open video stream. Please check your webcam.")
        return
    
    print("✓ Webcam connected successfully")
    print("\nStarting yoga session...")
    print("Controls:")
    print("- 'n': Next pose")
    print("- 'p': Previous pose")
    print("- 'i': Get instructions for current pose")
    print("- 'q': Quit")
    
    # Set video properties for better performance
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    video_capture.set(cv2.CAP_PROP_FPS, 30)

    voice_guide.speak_session_start()
    
    # Get initial instructions
    instructions = analyzer.get_pose_instructions(target_pose)
    pose_name = analyzer.yoga_poses[target_pose]['name']
    voice_guide.speak_pose_instructions(pose_name, instructions)
    
    last_feedback_time = 0
    feedback_interval = 5  # Give feedback every 5 seconds
    last_score = 0

    try:
        while video_capture.isOpened():
            ret, frame = video_capture.read()

            if not ret:
                print("Error: Failed to capture image from webcam.")
                break

            # Flip the frame horizontally for mirror view
            frame = cv2.flip(frame, 1)

            # Detect and analyze pose
            results = detector.detect_pose(frame)
            analysis_result = analyzer.analyze_pose(frame, target_pose)
            
            # Draw pose landmarks
            frame = detector.draw_landmarks(frame, results)
            
            # Draw UI elements
            frame = draw_ui_elements(frame, analysis_result, target_pose, pose_list, current_pose_index)
            
            # Provide voice feedback periodically
            current_time = time.time()
            if (current_time - last_feedback_time) > feedback_interval and analysis_result['pose_detected']:
                score = analysis_result['score']
                
                # Only provide feedback if there's a significant change or improvement
                if abs(score - last_score) > 10 or score > 80:
                    voice_guide.speak_feedback(analysis_result['feedback'], score)
                    
                    if analysis_result['corrections']:
                        voice_guide.speak_corrections(analysis_result['corrections'])
                
                last_feedback_time = current_time
                last_score = score

            # Display the frame
            cv2.imshow('AI Yoga Instructor', frame)

            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('n'):  # Next pose
                current_pose_index = (current_pose_index + 1) % len(pose_list)
                target_pose = pose_list[current_pose_index]
                instructions = analyzer.get_pose_instructions(target_pose)
                pose_name = analyzer.yoga_poses[target_pose]['name']
                voice_guide.speak_pose_instructions(pose_name, instructions)
                last_feedback_time = 0  # Reset feedback timer
            elif key == ord('p'):  # Previous pose
                current_pose_index = (current_pose_index - 1) % len(pose_list)
                target_pose = pose_list[current_pose_index]
                instructions = analyzer.get_pose_instructions(target_pose)
                pose_name = analyzer.yoga_poses[target_pose]['name']
                voice_guide.speak_pose_instructions(pose_name, instructions)
                last_feedback_time = 0  # Reset feedback timer
            elif key == ord('i'):  # Get instructions
                instructions = analyzer.get_pose_instructions(target_pose)
                pose_name = analyzer.yoga_poses[target_pose]['name']
                voice_guide.speak_pose_instructions(pose_name, instructions)

    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("\nEnding yoga session...")
        voice_guide.speak_session_end()
        time.sleep(2)  # Give time for final speech
        voice_guide.stop_all_speech()
        video_capture.release()
        cv2.destroyAllWindows()
        print("✓ Session ended successfully")


if __name__ == "__main__":
    main()

