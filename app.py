from flask import Flask, render_template, send_from_directory, jsonify, request
import os
import json

app = Flask(__name__)

# Serve static files
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# API endpoint for pose analysis
@app.route('/api/analyze_pose', methods=['POST'])
def analyze_pose():
    """
    This endpoint would integrate with your AI pose detection system
    For now, it returns mock data
    """
    data = request.json
    pose_type = data.get('pose_type', 'mountain')
    
    # Mock response - in real implementation, this would use your AI model
    mock_scores = {
        'mountain': 85,
        'tree': 75,
        'sukasana': 90,
        'childs_pose': 80,
        'warrior2': 70
    }
    
    mock_feedback = {
        'mountain': "Great posture! Keep your spine straight.",
        'tree': "Good balance! Try to hold for longer.",
        'sukasana': "Perfect meditation pose! Very calm.",
        'childs_pose': "Excellent relaxation. Let go of tension.",
        'warrior2': "Strong warrior! Bend your front knee more."
    }
    
    return jsonify({
        'pose_detected': True,
        'score': mock_scores.get(pose_type, 50),
        'feedback': mock_feedback.get(pose_type, "Keep practicing!"),
        'corrections': [
            "Adjust your alignment",
            "Focus on your breathing"
        ]
    })

# API endpoint to get pose instructions
@app.route('/api/pose_instructions/<pose_type>')
def get_pose_instructions(pose_type):
    """
    Get detailed instructions for a specific pose
    """
    instructions = {
        'mountain': [
            "Stand with feet hip-width apart",
            "Keep your spine straight and tall",
            "Relax your shoulders away from your ears",
            "Let your arms hang naturally at your sides",
            "Distribute weight evenly on both feet"
        ],
        'tree': [
            "Stand on your right leg",
            "Place your left foot on your inner right thigh",
            "Press your foot into your leg and leg into your foot",
            "Bring your hands to prayer position at your chest",
            "Focus on a point ahead for balance"
        ],
        'sukasana': [
            "Sit cross-legged on the floor",
            "Keep your spine straight and tall",
            "Rest your hands on your knees",
            "Relax your shoulders",
            "Breathe deeply and calmly"
        ],
        'childs_pose': [
            "Start on your hands and knees",
            "Sit back on your heels",
            "Fold forward, bringing forehead to the mat",
            "Extend your arms forward or by your sides",
            "Breathe deeply and relax"
        ],
        'warrior2': [
            "Step your feet wide apart",
            "Turn your right foot out 90 degrees",
            "Turn your left foot in 15 degrees",
            "Bend your right knee over your ankle",
            "Extend your arms parallel to the ground"
        ]
    }
    
    return jsonify({
        'pose': pose_type,
        'instructions': instructions.get(pose_type, [])
    })

if __name__ == '__main__':
    print("🧘 Starting AI Yoga Instructor Web Server...")
    print("🌐 Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
