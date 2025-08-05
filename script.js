document.addEventListener("DOMContentLoaded", () => {
    const navbar = document.querySelector('.navbar');
    const hamburger = document.querySelector('.hamburger');

    hamburger.addEventListener('click', () => {
        navbar.classList.toggle('active');
    });

    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', () => {
            navbar.classList.remove('active');
        });
    });
});

function scrollToPoses() {
    document.querySelector('#poses').scrollIntoView({ behavior: 'smooth' });
}

function startPractice() {
    document.querySelector('#practice').scrollIntoView({ behavior: 'smooth' });
}

function showPoseDetails(pose) {
    const modal = document.querySelector('#poseModal');
    const modalContent = document.querySelector('#poseModalContent');

    const posesData = {
        mountain: {
            name: "Mountain Pose",
            sanskrit: "Tadasana",
            benefits: "Builds a solid foundation for all standing poses and improves posture.",
            description: "Stand tall with feet together. Engage the thighs and keep shoulders relaxed."
        },
        tree: {
            name: "Tree Pose",
            sanskrit: "Vrikshasana",
            benefits: "Improves balance and strengthens legs.",
            description: "Balance on one foot, place the other foot on your inner thigh, hands at prayer."
        },
        sukasana: {
            name: "Easy Pose",
            sanskrit: "Sukasana",
            benefits: "Promotes meditative practices and calms the mind.",
            description: "Sit comfortably cross-legged, spine straight, hands resting on knees."
        },
        childs_pose: {
            name: "Child's Pose",
            sanskrit: "Balasana",
            benefits: "Relieves stress and gently stretches the back.",
            description: "Sit back on the heels, forehead on the mat, arms extended forward."
        },
        warrior2: {
            name: "Warrior II",
            sanskrit: "Virabhadrasana II",
            benefits: "Strengthens the legs and improves concentration.",
            description: "Step legs wide apart, bend front knee, extend arms parallel to the ground."
        }
    };

    const poseData = posesData[pose];

    modalContent.innerHTML = `
        <h2 class="modal-title">${poseData.name} - ${poseData.sanskrit}</h2>
        <p class="modal-benefits"><strong>Benefits:</strong> ${poseData.benefits}</p>
        <p class="modal-description"><strong>Description:</strong> ${poseData.description}</p>
    `;

    modal.style.display = "block";
}

function closePoseModal() {
    const modal = document.querySelector('#poseModal');
    modal.style.display = "none";
}

let pose, camera;
let currentPose = 'mountain';
let poseDetectionActive = false;

async function initializeCamera() {
    const videoElement = document.getElementById('videoElement');
    const canvasElement = document.getElementById('canvasElement');
    const scoreElement = document.getElementById('poseScore');
    const poseNameElement = document.getElementById('currentPoseName');

    try {
        // Load MediaPipe Pose
        pose = new Pose({
            locateFile: (file) => {
                return `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`;
            }
        });

        pose.setOptions({
            modelComplexity: 1,
            smoothLandmarks: true,
            enableSegmentation: false,
            smoothSegmentation: true,
            minDetectionConfidence: 0.5,
            minTrackingConfidence: 0.5
        });

        pose.onResults(onResults);

        // Initialize camera
        camera = new Camera(videoElement, {
            onFrame: async () => {
                if (poseDetectionActive) {
                    await pose.send({ image: videoElement });
                }
            },
            width: 640,
            height: 480
        });

        await camera.start();
        poseDetectionActive = true;
        console.log('Camera and pose detection initialized successfully');
    } catch (error) {
        console.error('Error initializing camera and pose detection:', error);
        alert('Failed to initialize pose detection. Please check your internet connection.');
    }
}

function onResults(results) {
    const canvasElement = document.getElementById('canvasElement');
    const canvasCtx = canvasElement.getContext('2d');
    const scoreElement = document.getElementById('poseScore');

    canvasCtx.save();
    canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
    
    // Draw the video frame
    canvasCtx.drawImage(results.image, 0, 0, canvasElement.width, canvasElement.height);

    if (results.poseLandmarks) {
        // Analyze the pose and get feedback
        const analysis = analyzePose(results.poseLandmarks, currentPose);
        
        // Update score display
        scoreElement.textContent = analysis.score;
        
        // Draw pose landmarks and connections with color coding
        drawPoseLandmarks(canvasCtx, results.poseLandmarks, analysis);
        
        // Display feedback
        displayFeedback(analysis);
    }
    
    canvasCtx.restore();
}

function drawPoseLandmarks(ctx, landmarks, analysis) {
    const connections = [
        [11, 12], // shoulders
        [11, 13], [13, 15], // left arm
        [12, 14], [14, 16], // right arm
        [11, 23], [12, 24], // torso
        [23, 24], // hips
        [23, 25], [25, 27], [27, 29], [29, 31], // left leg
        [24, 26], [26, 28], [28, 30], [30, 32], // right leg
    ];

    const width = ctx.canvas.width;
    const height = ctx.canvas.height;

    // Draw connections
    connections.forEach(([startIdx, endIdx]) => {
        if (landmarks[startIdx] && landmarks[endIdx]) {
            const start = landmarks[startIdx];
            const end = landmarks[endIdx];
            
            // Determine color based on pose accuracy
            const color = analysis.score >= 70 ? '#00FF00' : '#FF0000'; // Green for good, red for bad
            
            ctx.beginPath();
            ctx.strokeStyle = color;
            ctx.lineWidth = 3;
            ctx.moveTo(start.x * width, start.y * height);
            ctx.lineTo(end.x * width, end.y * height);
            ctx.stroke();
        }
    });

    // Draw landmarks
    landmarks.forEach((landmark, index) => {
        if (landmark.visibility > 0.5) {
            const x = landmark.x * width;
            const y = landmark.y * height;
            
            ctx.beginPath();
            ctx.arc(x, y, 5, 0, 2 * Math.PI);
            ctx.fillStyle = analysis.score >= 70 ? '#00FF00' : '#FF0000';
            ctx.fill();
            ctx.strokeStyle = '#FFFFFF';
            ctx.lineWidth = 2;
            ctx.stroke();
        }
    });
}

function analyzePose(landmarks, targetPose) {
    // Basic pose analysis - you can expand this with more sophisticated logic
    const angles = calculateAngles(landmarks);
    
    let score = 50; // Base score
    let feedback = "Keep practicing!";
    let corrections = [];
    
    switch (targetPose) {
        case 'mountain':
            score = analyzeMountainPose(landmarks, angles);
            feedback = score >= 70 ? "Great mountain pose!" : "Stand straighter and relax shoulders";
            break;
        case 'tree':
            score = analyzeTreePose(landmarks, angles);
            feedback = score >= 70 ? "Excellent balance!" : "Focus on balance and alignment";
            break;
        case 'sukasana':
            score = analyzeSukasana(landmarks, angles);
            feedback = score >= 70 ? "Perfect meditation pose!" : "Sit up straighter";
            break;
        case 'childs_pose':
            score = analyzeChildsPose(landmarks, angles);
            feedback = score >= 70 ? "Relaxing child's pose!" : "Fold forward more";
            break;
        case 'warrior2':
            score = analyzeWarrior2(landmarks, angles);
            feedback = score >= 70 ? "Strong warrior!" : "Bend front knee and extend arms";
            break;
    }
    
    return { score: Math.round(score), feedback, corrections };
}

function calculateAngles(landmarks) {
    // Calculate key angles for pose analysis
    const angles = {};
    
    // Helper function to calculate angle between three points
    function calculateAngle(a, b, c) {
        const radians = Math.atan2(c.y - b.y, c.x - b.x) - Math.atan2(a.y - b.y, a.x - b.x);
        let angle = Math.abs(radians * 180.0 / Math.PI);
        if (angle > 180.0) {
            angle = 360 - angle;
        }
        return angle;
    }
    
    // Left arm angle
    if (landmarks[11] && landmarks[13] && landmarks[15]) {
        angles.leftArm = calculateAngle(landmarks[11], landmarks[13], landmarks[15]);
    }
    
    // Right arm angle
    if (landmarks[12] && landmarks[14] && landmarks[16]) {
        angles.rightArm = calculateAngle(landmarks[12], landmarks[14], landmarks[16]);
    }
    
    // Left leg angle
    if (landmarks[23] && landmarks[25] && landmarks[27]) {
        angles.leftLeg = calculateAngle(landmarks[23], landmarks[25], landmarks[27]);
    }
    
    // Right leg angle
    if (landmarks[24] && landmarks[26] && landmarks[28]) {
        angles.rightLeg = calculateAngle(landmarks[24], landmarks[26], landmarks[28]);
    }
    
    return angles;
}

function analyzeMountainPose(landmarks, angles) {
    let score = 100;
    
    // Check if standing straight
    if (landmarks[11] && landmarks[23]) {
        const shoulderHipAlignment = Math.abs(landmarks[11].x - landmarks[23].x);
        if (shoulderHipAlignment > 0.05) score -= 20;
    }
    
    // Check arm position
    if (angles.leftArm < 160 || angles.rightArm < 160) score -= 15;
    
    return Math.max(0, score);
}

function analyzeTreePose(landmarks, angles) {
    let score = 100;
    
    // Check balance (one leg should be bent)
    if (angles.leftLeg && angles.rightLeg) {
        const legDifference = Math.abs(angles.leftLeg - angles.rightLeg);
        if (legDifference < 30) score -= 30; // Both legs shouldn't be the same angle
    }
    
    return Math.max(0, score);
}

function analyzeSukasana(landmarks, angles) {
    let score = 100;
    
    // Check if sitting (hips should be lower than shoulders)
    if (landmarks[11] && landmarks[23]) {
        if (landmarks[23].y < landmarks[11].y) score -= 30;
    }
    
    return Math.max(0, score);
}

function analyzeChildsPose(landmarks, angles) {
    let score = 100;
    
    // Check if folded forward (head should be low)
    if (landmarks[0] && landmarks[23]) {
        if (landmarks[0].y < landmarks[23].y) score -= 40;
    }
    
    return Math.max(0, score);
}

function analyzeWarrior2(landmarks, angles) {
    let score = 100;
    
    // Check leg position (one should be bent)
    if (angles.leftLeg && angles.rightLeg) {
        const minLegAngle = Math.min(angles.leftLeg, angles.rightLeg);
        if (minLegAngle > 120) score -= 30; // At least one leg should be bent
    }
    
    return Math.max(0, score);
}

function displayFeedback(analysis) {
    // You can add more sophisticated feedback display here
    console.log(`Pose Score: ${analysis.score}, Feedback: ${analysis.feedback}`);
}

function selectPose(pose) {
    const poseData = {
        mountain: "Mountain Pose",
        tree: "Tree Pose",
        sukasana: "Easy Pose",
        childs_pose: "Child's Pose",
        warrior2: "Warrior II"
    };

    currentPose = pose;
    document.getElementById('currentPoseName').textContent = poseData[pose];
    
    // Update button styling
    document.querySelectorAll('.pose-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
}

