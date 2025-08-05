import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing AI Yoga Instructor dependencies...")
    
    # List of required packages with versions
    packages = [
        "opencv-python==4.8.1.78",
        "mediapipe==0.10.7", 
        "numpy==1.24.3",
        "pygame==2.5.2",
        "pyttsx3==2.90",
        "scipy==1.11.4",
        "scikit-learn==1.3.2",
        "matplotlib==3.7.2",
        "Pillow==10.1.0"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}: {e}")
            return False
    
    print("\n✓ All dependencies installed successfully!")
    print("You can now run the AI Yoga Instructor with: python main.py")
    return True

if __name__ == "__main__":
    install_requirements()
