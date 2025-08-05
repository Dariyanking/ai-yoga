import numpy as np
import mediapipe as mp
from pose_detector import PoseDetector
from typing import Dict, List, Tuple, Optional

class YogaAnalyzer:
    def __init__(self):
        self.pose_detector = PoseDetector()
        self.mp_pose = mp.solutions.pose
        
        # Define yoga poses with ideal angles and key points
        self.yoga_poses = {
            'mountain': {
                'name': 'Mountain Pose (Tadasana)',
                'key_angles': {
                    'left_arm': (150, 180),  # Shoulder-elbow-wrist
                    'right_arm': (150, 180),
                    'left_leg': (170, 180),  # Hip-knee-ankle
                    'right_leg': (170, 180),
                    'spine': (170, 180)      # Shoulder-hip-knee alignment
                },
                'feedback': {
                    'good': "Great posture! Keep your spine straight and shoulders relaxed.",
                    'improve': "Try to straighten your spine and distribute weight evenly on both feet."
                }
            },
            'warrior1': {
                'name': 'Warrior I (Virabhadrasana I)',
                'key_angles': {
                    'front_knee': (80, 100),    # Hip-knee-ankle of front leg
                    'back_leg': (160, 180),     # Hip-knee-ankle of back leg
                    'arms_up': (160, 180),      # Shoulder-elbow-wrist
                    'spine': (170, 180)         # Torso alignment
                },
                'feedback': {
                    'good': "Excellent Warrior I! Your front knee is properly bent and back leg is strong.",
                    'improve': "Bend your front knee more and keep your back leg straight. Lift your arms higher."
                }
            },
            'downward_dog': {
                'name': 'Downward Facing Dog (Adho Mukha Svanasana)',
                'key_angles': {
                    'body_angle': (130, 150),   # Shoulder-hip-knee
                    'arm_body': (150, 180),     # Arm to torso
                    'leg_body': (120, 140)      # Leg to torso
                },
                'feedback': {
                    'good': "Perfect downward dog! Your body forms a beautiful inverted V.",
                    'improve': "Press your hands firmly down and lift your hips higher to create a better V-shape."
                }
            },
            'tree': {
                'name': 'Tree Pose (Vrikshasana)',
                'key_angles': {
                    'standing_leg': (170, 180),  # Hip-knee-ankle of standing leg
                    'bent_knee': (80, 120),      # Hip-knee-ankle of bent leg
                    'arms': (160, 180)           # Arms raised above head
                },
                'feedback': {
                    'good': "Beautiful tree pose! Great balance and alignment.",
                    'improve': "Focus on your balance and keep your standing leg straight."
                }
            },
            'sukasana': {
                'name': 'Easy Pose (Sukasana)',
                'key_angles': {
                    'spine': (170, 180),         # Shoulder-hip alignment
                    'left_knee': (80, 120),      # Hip-knee-ankle for crossed legs
                    'right_knee': (80, 120),     # Hip-knee-ankle for crossed legs
                    'shoulders': (160, 180)      # Shoulder alignment
                },
                'feedback': {
                    'good': "Perfect sukasana! Your spine is straight and you look comfortable.",
                    'improve': "Sit up straighter and relax your shoulders. Keep your spine tall."
                }
            },
            'childs_pose': {
                'name': 'Child\'s Pose (Balasana)',
                'key_angles': {
                    'hip_fold': (40, 70),        # Hip flexion angle
                    'knee_bend': (30, 60),       # Knee flexion
                    'spine_curve': (120, 150),   # Natural spine curve
                    'arms': (160, 180)           # Arms extended forward
                },
                'feedback': {
                    'good': "Wonderful child\'s pose! Very relaxing and restorative.",
                    'improve': "Sink your hips back more and extend your arms forward."
                }
            },
            'warrior2': {
                'name': 'Warrior II (Virabhadrasana II)',
                'key_angles': {
                    'front_knee': (80, 100),     # Front leg hip-knee-ankle
                    'back_leg': (160, 180),      # Back leg straight
                    'torso': (170, 180),         # Torso upright
                    'arms': (160, 180)           # Arms parallel to ground
                },
                'feedback': {
                    'good': "Excellent Warrior II! Strong and stable with good alignment.",
                    'improve': "Bend your front knee more and keep your torso upright. Extend arms parallel to the ground."
                }
            }
        }
    
    def analyze_pose(self, image, target_pose='mountain'):
        """Analyze the current pose and provide feedback"""
        results = self.pose_detector.detect_pose(image)
        
        if not results.pose_landmarks:
            return {
                'pose_detected': False,
                'score': 0,
                'feedback': "No pose detected. Please ensure you're fully visible in the camera.",
                'angles': {},
                'corrections': []
            }
        
        # Get landmark coordinates
        landmarks = self.pose_detector.get_all_landmarks(results, image.shape)
        
        # Calculate angles based on the target pose
        angles = self.calculate_pose_angles(landmarks, target_pose)
        
        # Score the pose
        score = self.score_pose(angles, target_pose)
        
        # Generate feedback
        feedback, corrections = self.generate_feedback(angles, target_pose, score)
        
        return {
            'pose_detected': True,
            'score': score,
            'feedback': feedback,
            'angles': angles,
            'corrections': corrections,
            'landmarks': landmarks
        }
    
    def calculate_pose_angles(self, landmarks, pose_type):
        """Calculate relevant angles for the specified pose"""
        angles = {}
        
        if not landmarks:
            return angles
        
        try:
            if pose_type == 'mountain':
                # Left arm angle (shoulder-elbow-wrist)
                if all(idx in landmarks for idx in [11, 13, 15]):
                    angles['left_arm'] = self.pose_detector.calculate_angle(
                        landmarks[11], landmarks[13], landmarks[15]
                    )
                
                # Right arm angle
                if all(idx in landmarks for idx in [12, 14, 16]):
                    angles['right_arm'] = self.pose_detector.calculate_angle(
                        landmarks[12], landmarks[14], landmarks[16]
                    )
                
                # Spine alignment (shoulder-hip-knee)
                if all(idx in landmarks for idx in [12, 24, 26]):
                    angles['spine'] = self.pose_detector.calculate_angle(
                        landmarks[12], landmarks[24], landmarks[26]
                    )
            
            elif pose_type == 'warrior1':
                # Front knee angle (assuming left leg is front)
                if all(idx in landmarks for idx in [23, 25, 27]):
                    angles['front_knee'] = self.pose_detector.calculate_angle(
                        landmarks[23], landmarks[25], landmarks[27]
                    )
                
                # Back leg angle (right leg)
                if all(idx in landmarks for idx in [24, 26, 28]):
                    angles['back_leg'] = self.pose_detector.calculate_angle(
                        landmarks[24], landmarks[26], landmarks[28]
                    )
                
                # Arms up angle
                if all(idx in landmarks for idx in [11, 13, 15]):
                    angles['arms_up'] = self.pose_detector.calculate_angle(
                        landmarks[11], landmarks[13], landmarks[15]
                    )
            
            elif pose_type == 'downward_dog':
                # Body angle (shoulder-hip-knee)
                if all(idx in landmarks for idx in [12, 24, 26]):
                    angles['body_angle'] = self.pose_detector.calculate_angle(
                        landmarks[12], landmarks[24], landmarks[26]
                    )
                
                # Arm to body angle
                if all(idx in landmarks for idx in [16, 14, 12]):
                    angles['arm_body'] = self.pose_detector.calculate_angle(
                        landmarks[16], landmarks[14], landmarks[12]
                    )
            
            elif pose_type == 'tree':
                # Standing leg (right leg straight)
                if all(idx in landmarks for idx in [24, 26, 28]):
                    angles['standing_leg'] = self.pose_detector.calculate_angle(
                        landmarks[24], landmarks[26], landmarks[28]
                    )
                
                # Bent knee angle (left leg)
                if all(idx in landmarks for idx in [23, 25, 27]):
                    angles['bent_knee'] = self.pose_detector.calculate_angle(
                        landmarks[23], landmarks[25], landmarks[27]
                    )
        
        except Exception as e:
            print(f"Error calculating angles: {e}")
        
        return angles
    
    def score_pose(self, calculated_angles, pose_type):
        """Score the pose based on how close angles are to ideal ranges"""
        if pose_type not in self.yoga_poses:
            return 0
        
        ideal_angles = self.yoga_poses[pose_type]['key_angles']
        total_score = 0
        scored_angles = 0
        
        for angle_name, (min_ideal, max_ideal) in ideal_angles.items():
            if angle_name in calculated_angles:
                actual_angle = calculated_angles[angle_name]
                
                if min_ideal <= actual_angle <= max_ideal:
                    # Perfect range
                    score = 100
                else:
                    # Calculate score based on deviation
                    if actual_angle < min_ideal:
                        deviation = min_ideal - actual_angle
                    else:
                        deviation = actual_angle - max_ideal
                    
                    # Score decreases with deviation (max deviation of 30 degrees gives 0 score)
                    score = max(0, 100 - (deviation / 30) * 100)
                
                total_score += score
                scored_angles += 1
        
        return int(total_score / max(scored_angles, 1))
    
    def generate_feedback(self, calculated_angles, pose_type, score):
        """Generate feedback and corrections based on pose analysis"""
        if pose_type not in self.yoga_poses:
            return "Unknown pose", []
        
        pose_info = self.yoga_poses[pose_type]
        corrections = []
        
        # Check each angle and provide specific corrections
        for angle_name, (min_ideal, max_ideal) in pose_info['key_angles'].items():
            if angle_name in calculated_angles:
                actual_angle = calculated_angles[angle_name]
                
                if actual_angle < min_ideal:
                    if 'arm' in angle_name:
                        corrections.append(f"Straighten your {angle_name.replace('_', ' ')} more")
                    elif 'leg' in angle_name or 'knee' in angle_name:
                        corrections.append(f"Straighten your {angle_name.replace('_', ' ')} more")
                    elif 'spine' in angle_name:
                        corrections.append("Keep your spine straighter")
                
                elif actual_angle > max_ideal:
                    if 'knee' in angle_name and 'front' in angle_name:
                        corrections.append("Bend your front knee more")
                    elif 'arm' in angle_name:
                        corrections.append(f"Relax your {angle_name.replace('_', ' ')} slightly")
        
        # Generate overall feedback
        if score >= 80:
            feedback = pose_info['feedback']['good']
        else:
            feedback = pose_info['feedback']['improve']
        
        return feedback, corrections
    
    def get_pose_instructions(self, pose_type):
        """Get instructions for a specific pose"""
        instructions = {
            'mountain': [
                "Stand with feet hip-width apart",
                "Keep your spine straight and tall",
                "Relax your shoulders away from your ears",
                "Let your arms hang naturally at your sides",
                "Distribute weight evenly on both feet"
            ],
            'warrior1': [
                "Step your left foot back about 3-4 feet",
                "Turn your left foot out 45 degrees",
                "Bend your right knee over your ankle",
                "Raise your arms overhead",
                "Keep your torso facing forward"
            ],
            'downward_dog': [
                "Start on hands and knees",
                "Tuck your toes under",
                "Lift your hips up and back",
                "Straighten your legs as much as possible",
                "Press your hands firmly into the ground"
            ],
            'tree': [
                "Stand on your right leg",
                "Place your left foot on your inner right thigh",
                "Press your foot into your leg and leg into your foot",
                "Bring your hands to prayer position at your chest",
                "Focus on a point ahead for balance"
            ]
        }
        
        return instructions.get(pose_type, [])
