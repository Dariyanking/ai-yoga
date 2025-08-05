import cv2
import mediapipe as mp
import numpy as np
import math
from typing import List, Tuple, Dict, Optional

class PoseDetector:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """Initialize MediaPipe pose detection"""
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
    def detect_pose(self, image):
        """Detect pose landmarks in the image"""
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_image)
        return results
    
    def draw_landmarks(self, image, results):
        """Draw pose landmarks on the image"""
        if results.pose_landmarks:
            self.mp_drawing.draw_landmarks(
                image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS
            )
        return image
    
    def get_landmark_coordinates(self, results, landmark_id, image_shape):
        """Get normalized coordinates of a specific landmark"""
        if results.pose_landmarks:
            landmark = results.pose_landmarks.landmark[landmark_id]
            h, w = image_shape[:2]
            x = int(landmark.x * w)
            y = int(landmark.y * h)
            return (x, y, landmark.visibility)
        return None
    
    def calculate_angle(self, point1, point2, point3):
        """Calculate angle between three points"""
        # Convert to numpy arrays
        a = np.array(point1[:2])  # First point (only x, y)
        b = np.array(point2[:2])  # Middle point (vertex)
        c = np.array(point3[:2])  # Third point
        
        # Calculate vectors
        ba = a - b
        bc = c - b
        
        # Calculate angle using dot product
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        
        # Ensure cosine is within valid range
        cosine_angle = np.clip(cosine_angle, -1.0, 1.0)
        
        angle = np.arccos(cosine_angle)
        return np.degrees(angle)
    
    def get_all_landmarks(self, results, image_shape):
        """Get all landmark coordinates"""
        landmarks = {}
        if results.pose_landmarks:
            for i, landmark in enumerate(results.pose_landmarks.landmark):
                h, w = image_shape[:2]
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                landmarks[i] = (x, y, landmark.visibility)
        return landmarks
