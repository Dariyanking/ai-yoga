# AI-Powered Yoga Instructor 🧘‍♀️

An intelligent yoga instructor that uses computer vision to detect your poses, analyze your form, and provide real-time feedback with voice guidance.

## Features

### 🎯 Pose Detection & Tracking
- Real-time pose detection using MediaPipe
- Accurate body landmark identification
- Mirror-view webcam display for natural practice

### 📊 Posture Analysis & Scoring
- Real-time pose analysis with scoring (0-100)
- Angle calculation for key body joints
- Alignment assessment based on ideal yoga poses

### 🗣️ Voice Guidance
- Text-to-speech feedback and instructions
- Encouraging messages based on performance
- Step-by-step pose instructions
- Real-time corrections and suggestions

### 🧘‍♀️ Supported Yoga Poses
1. **Mountain Pose (Tadasana)** - Foundation standing pose
2. **Warrior I (Virabhadrasana I)** - Strength and balance pose
3. **Downward Facing Dog (Adho Mukha Svanasana)** - Full-body stretch
4. **Tree Pose (Vrikshasana)** - Balance and focus pose

## Installation

### Prerequisites
- Python 3.7 or higher
- Webcam
- Windows/Mac/Linux

### Quick Setup
1. Clone or download the project
2. Navigate to the project directory
3. Run the installation script:
   ```bash
   python install.py
   ```

### Manual Installation
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Application
```bash
python main.py
```

### Controls
- **'n'** - Next pose
- **'p'** - Previous pose  
- **'i'** - Get instructions for current pose
- **'q'** - Quit application

### Setup Tips
1. **Camera Position**: Place your webcam at chest height, 6-8 feet away
2. **Lighting**: Ensure good lighting with minimal shadows
3. **Space**: Clear area with contrasting background
4. **Clothing**: Wear fitted clothing for better pose detection

## How It Works

### 1. Pose Detection
- Uses Google's MediaPipe to detect 33 body landmarks
- Processes video frames in real-time
- Calculates joint angles and body alignment

### 2. Pose Analysis
- Compares detected poses with ideal yoga pose parameters
- Calculates deviation from perfect form
- Generates specific improvement suggestions

### 3. Scoring System
- **90-100**: Excellent form
- **70-89**: Good form with minor adjustments needed
- **50-69**: Moderate form, focus on corrections
- **Below 50**: Needs significant improvement

### 4. Voice Feedback
- Provides encouraging feedback based on score
- Offers specific corrections for pose improvement
- Gives step-by-step instructions for each pose

## Technical Details

### Architecture
```
├── pose_detector.py     # MediaPipe pose detection
├── yoga_analyzer.py     # Pose analysis and scoring
├── voice_guide.py       # Text-to-speech guidance
├── main.py             # Main application
└── requirements.txt    # Dependencies
```

### Key Technologies
- **OpenCV**: Video capture and image processing
- **MediaPipe**: Real-time pose detection
- **NumPy**: Mathematical computations
- **pyttsx3**: Text-to-speech conversion

### Pose Analysis Algorithm
1. Extract body landmarks from video frame
2. Calculate angles between key joints
3. Compare with ideal pose parameters
4. Generate score based on deviations
5. Provide specific corrections

## Customization

### Adding New Poses
1. Define pose parameters in `yoga_analyzer.py`
2. Add angle calculations for key joints
3. Set ideal angle ranges
4. Create feedback messages
5. Add pose instructions

### Adjusting Sensitivity
- Modify `min_detection_confidence` and `min_tracking_confidence` in pose detector
- Adjust scoring thresholds in yoga analyzer
- Change feedback frequency in main application

## Troubleshooting

### Common Issues
1. **No webcam detected**: Check camera permissions and connections
2. **Poor pose detection**: Improve lighting and camera position
3. **No voice output**: Check audio settings and speakers
4. **Performance issues**: Close other applications, reduce video resolution

### Performance Tips
- Ensure good lighting conditions
- Use a contrasting background
- Keep the full body in frame
- Minimize background movement

## Future Enhancements

- [ ] More yoga poses (Warrior II, Triangle, etc.)
- [ ] Session tracking and progress analytics
- [ ] Pose sequence flows
- [ ] Mobile app version
- [ ] AI-powered pose recommendations
- [ ] Multiplayer yoga sessions

## Contributing

Feel free to contribute by:
- Adding new yoga poses
- Improving pose detection accuracy
- Enhancing the user interface
- Adding new features

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Google MediaPipe team for pose detection technology
- Yoga community for pose definitions and best practices
- Open source contributors for various libraries used

---

**Namaste! 🙏 Enjoy your AI-powered yoga practice!**
