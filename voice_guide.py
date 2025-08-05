import pyttsx3
import threading
import queue
import time
from typing import List, Optional

class VoiceGuide:
    def __init__(self, rate=150, volume=0.8):
        """Initialize text-to-speech engine"""
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)
        
        # Set voice properties (optional)
        voices = self.engine.getProperty('voices')
        if voices:
            # Try to use a female voice if available
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
        
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self.speech_thread = None
        self.last_feedback_time = 0
        self.feedback_interval = 3  # Minimum seconds between feedback
        
    def speak_async(self, text: str, priority: bool = False):
        """Add text to speech queue"""
        current_time = time.time()
        
        # Avoid too frequent feedback unless it's high priority
        if not priority and (current_time - self.last_feedback_time) < self.feedback_interval:
            return
        
        if priority:
            # Clear queue for high priority messages
            while not self.speech_queue.empty():
                try:
                    self.speech_queue.get_nowait()
                except queue.Empty:
                    break
        
        self.speech_queue.put(text)
        self.last_feedback_time = current_time
        
        # Start speech thread if not running
        if not self.speech_thread or not self.speech_thread.is_alive():
            self.speech_thread = threading.Thread(target=self._speech_worker)
            self.speech_thread.daemon = True
            self.speech_thread.start()
    
    def _speech_worker(self):
        """Worker thread for text-to-speech"""
        while True:
            try:
                text = self.speech_queue.get(timeout=1)
                self.is_speaking = True
                self.engine.say(text)
                self.engine.runAndWait()
                self.is_speaking = False
                self.speech_queue.task_done()
            except queue.Empty:
                break
            except Exception as e:
                print(f"Speech error: {e}")
                self.is_speaking = False
    
    def speak_immediate(self, text: str):
        """Speak text immediately (blocking)"""
        self.engine.say(text)
        self.engine.runAndWait()
    
    def speak_pose_instructions(self, pose_name: str, instructions: List[str]):
        """Speak instructions for a yoga pose"""
        intro_text = f"Let's practice {pose_name}. Here are the steps:"
        self.speak_async(intro_text, priority=True)
        
        time.sleep(2)  # Brief pause
        
        for i, instruction in enumerate(instructions, 1):
            instruction_text = f"Step {i}: {instruction}"
            self.speak_async(instruction_text, priority=True)
            time.sleep(1)  # Pause between instructions
    
    def speak_feedback(self, feedback: str, score: int):
        """Speak pose feedback"""
        if score >= 80:
            feedback_text = f"Great! Your score is {score}. {feedback}"
        elif score >= 60:
            feedback_text = f"Good effort! Your score is {score}. {feedback}"
        else:
            feedback_text = f"Keep practicing! Your score is {score}. {feedback}"
        
        self.speak_async(feedback_text)
    
    def speak_corrections(self, corrections: List[str]):
        """Speak pose corrections"""
        if not corrections:
            return
        
        if len(corrections) == 1:
            correction_text = f"Try this: {corrections[0]}"
        else:
            correction_text = "Here are some adjustments: " + ". ".join(corrections)
        
        self.speak_async(correction_text)
    
    def speak_encouragement(self, score: int):
        """Speak encouraging messages based on score"""
        if score >= 90:
            messages = [
                "Excellent form! You're a natural!",
                "Perfect! Your alignment is beautiful!",
                "Outstanding! You've mastered this pose!"
            ]
        elif score >= 70:
            messages = [
                "Great job! You're getting better!",
                "Nice work! Keep focusing on your breath!",
                "Good progress! Feel the strength in your pose!"
            ]
        else:
            messages = [
                "Keep practicing! Every attempt makes you stronger!",
                "Don't worry, yoga is a journey. You're doing great!",
                "Remember to breathe and listen to your body!"
            ]
        
        import random
        self.speak_async(random.choice(messages))
    
    def speak_session_start(self):
        """Welcome message for yoga session"""
        welcome_text = ("Welcome to your AI yoga instructor! "
                       "I'll guide you through poses and help improve your form. "
                       "Remember to breathe deeply and listen to your body. "
                       "Let's begin!")
        self.speak_async(welcome_text, priority=True)
    
    def speak_session_end(self):
        """Closing message for yoga session"""
        closing_text = ("Great session! Remember, yoga is about progress, not perfection. "
                       "Take a moment to appreciate your practice today. Namaste!")
        self.speak_async(closing_text, priority=True)
    
    def stop_all_speech(self):
        """Stop all speech and clear queue"""
        self.engine.stop()
        while not self.speech_queue.empty():
            try:
                self.speech_queue.get_nowait()
            except queue.Empty:
                break
    
    def set_rate(self, rate: int):
        """Set speech rate (words per minute)"""
        self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float):
        """Set speech volume (0.0 to 1.0)"""
        self.engine.setProperty('volume', volume)
