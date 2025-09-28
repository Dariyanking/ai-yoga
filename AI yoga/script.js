// Yoga Pose Data - 2 poses per category
const poseData = {
    'weight-loss': [
        {
            name: 'Warrior III (Virabhadrasana III)',
            shortName: 'Warrior III',
            description: 'A powerful balancing pose that engages the entire core and burns calories.',
            instructions: [
                'Stand in Mountain Pose',
                'Step your left foot back into a lunge',
                'Straighten your back leg and lift it parallel to the floor',
                'Extend your arms forward for balance',
                'Hold for 30-60 seconds, then switch sides'
            ],
            benefits: 'Burns calories, strengthens core, improves balance and coordination',
            duration: '30-60 seconds',
            illustration: 'warrior3'
        },
        {
            name: 'Chair Pose (Utkatasana)',
            shortName: 'Chair Pose',
            description: 'An intense standing pose that targets large muscle groups for maximum calorie burn.',
            instructions: [
                'Stand with feet hip-width apart',
                'Bend your knees and lower your hips as if sitting in a chair',
                'Raise your arms overhead',
                'Keep your weight in your heels',
                'Hold for 30-60 seconds'
            ],
            benefits: 'High calorie burn, strengthens thighs and glutes, builds endurance',
            duration: '30-60 seconds',
            illustration: 'chair'
        }
    ],
    'weight-gain': [
        {
            name: 'Camel Pose (Ustrasana)',
            shortName: 'Camel Pose',
            description: 'A deep backbend that opens the chest and stimulates appetite.',
            instructions: [
                'Kneel on the floor with shins parallel',
                'Place your hands on your lower back',
                'Slowly arch back, reaching for your heels',
                'Open your chest and breathe deeply',
                'Hold for 15-30 seconds'
            ],
            benefits: 'Stimulates appetite, improves digestion, opens chest and shoulders',
            duration: '15-30 seconds',
            illustration: 'camel'
        },
        {
            name: 'Fish Pose (Matsyasana)',
            shortName: 'Fish Pose',
            description: 'A restorative backbend that aids digestion and hormone regulation.',
            instructions: [
                'Lie on your back with legs extended',
                'Place your hands under your hips',
                'Lift your chest and arch your back',
                'Rest the crown of your head on the floor',
                'Hold for 15-30 seconds'
            ],
            benefits: 'Improves digestion, stimulates thyroid, enhances nutrient absorption',
            duration: '15-30 seconds',
            illustration: 'fish'
        }
    ],
    'beginner': [
        {
            name: 'Mountain Pose (Tadasana)',
            shortName: 'Mountain Pose',
            description: 'The foundation of all standing poses, perfect for beginners to learn alignment.',
            instructions: [
                'Stand with feet hip-width apart',
                'Distribute weight evenly on both feet',
                'Engage your leg muscles',
                'Lengthen your spine',
                'Relax your shoulders and breathe normally'
            ],
            benefits: 'Improves posture, builds foundation for other poses, increases awareness',
            duration: '1-2 minutes',
            illustration: 'mountain'
        },
        {
            name: 'Child\'s Pose (Balasana)',
            shortName: 'Child\'s Pose',
            description: 'A gentle resting pose that provides comfort and relaxation.',
            instructions: [
                'Kneel on the floor with toes together',
                'Sit back on your heels',
                'Separate your knees hip-width apart',
                'Fold forward and rest your forehead on the floor',
                'Extend your arms forward or rest them by your sides'
            ],
            benefits: 'Relieves stress, stretches hips and thighs, calms the mind',
            duration: '1-3 minutes',
            illustration: 'child'
        }
    ],
    'regular': [
        {
            name: 'Downward Facing Dog (Adho Mukha Svanasana)',
            shortName: 'Downward Dog',
            description: 'A classic yoga pose that strengthens and stretches the entire body.',
            instructions: [
                'Start on hands and knees',
                'Tuck your toes under and lift your hips up',
                'Straighten your legs and arms',
                'Create an inverted V shape with your body',
                'Hold for 30-60 seconds'
            ],
            benefits: 'Full body stretch, strengthens arms and legs, improves circulation',
            duration: '30-60 seconds',
            illustration: 'downdog'
        },
        {
            name: 'Tree Pose (Vrksasana)',
            shortName: 'Tree Pose',
            description: 'A standing balance pose that improves focus and stability.',
            instructions: [
                'Stand in Mountain Pose',
                'Shift weight to your left foot',
                'Place your right foot on your inner left thigh',
                'Press your palms together at heart center',
                'Hold for 30-60 seconds, then switch sides'
            ],
            benefits: 'Improves balance, strengthens legs, enhances concentration',
            duration: '30-60 seconds',
            illustration: 'tree'
        }
    ]
};

// Pose Illustrations (Simple CSS-based illustrations)
const poseIllustrations = {
    warrior3: `
        <div class="stick-figure warrior3">
            <div class="head"></div>
            <div class="body"></div>
            <div class="left-arm extended"></div>
            <div class="right-arm extended"></div>
            <div class="left-leg standing"></div>
            <div class="right-leg extended-back"></div>
        </div>
        <p class="pose-name-small">Warrior III</p>
    `,
    chair: `
        <div class="stick-figure chair">
            <div class="head"></div>
            <div class="body bent"></div>
            <div class="left-arm raised"></div>
            <div class="right-arm raised"></div>
            <div class="left-leg bent"></div>
            <div class="right-leg bent"></div>
        </div>
        <p class="pose-name-small">Chair Pose</p>
    `,
    camel: `
        <div class="stick-figure camel">
            <div class="head back"></div>
            <div class="body arched"></div>
            <div class="left-arm back"></div>
            <div class="right-arm back"></div>
            <div class="left-leg kneeling"></div>
            <div class="right-leg kneeling"></div>
        </div>
        <p class="pose-name-small">Camel Pose</p>
    `,
    fish: `
        <div class="stick-figure fish">
            <div class="head tilted"></div>
            <div class="body arched-back"></div>
            <div class="left-arm side"></div>
            <div class="right-arm side"></div>
            <div class="left-leg straight"></div>
            <div class="right-leg straight"></div>
        </div>
        <p class="pose-name-small">Fish Pose</p>
    `,
    mountain: `
        <div class="stick-figure mountain">
            <div class="head"></div>
            <div class="body straight"></div>
            <div class="left-arm side"></div>
            <div class="right-arm side"></div>
            <div class="left-leg straight"></div>
            <div class="right-leg straight"></div>
        </div>
        <p class="pose-name-small">Mountain Pose</p>
    `,
    child: `
        <div class="stick-figure child">
            <div class="head down"></div>
            <div class="body folded"></div>
            <div class="left-arm extended-front"></div>
            <div class="right-arm extended-front"></div>
            <div class="left-leg tucked"></div>
            <div class="right-leg tucked"></div>
        </div>
        <p class="pose-name-small">Child's Pose</p>
    `,
    downdog: `
        <div class="stick-figure downdog">
            <div class="head down"></div>
            <div class="body inverted"></div>
            <div class="left-arm planted"></div>
            <div class="right-arm planted"></div>
            <div class="left-leg straight-up"></div>
            <div class="right-leg straight-up"></div>
        </div>
        <p class="pose-name-small">Downward Dog</p>
    `,
    tree: `
        <div class="stick-figure tree">
            <div class="head"></div>
            <div class="body straight"></div>
            <div class="left-arm prayer"></div>
            <div class="right-arm prayer"></div>
            <div class="left-leg standing"></div>
            <div class="right-leg bent-up"></div>
        </div>
        <p class="pose-name-small">Tree Pose</p>
    `
};

// Application State
let currentState = {
    category: null,
    poseIndex: 0,
    isVoiceActive: false,
    isCameraActive: false,
    recognition: null,
    stream: null,
    timer: null,
    timerSeconds: 0
};

// DOM Elements
const elements = {
    categorySection: document.getElementById('categorySection'),
    poseSection: document.getElementById('poseSection'),
    categoryCards: document.querySelectorAll('.category-card'),
    toggleVoice: document.getElementById('toggleVoice'),
    micIndicator: document.getElementById('micIndicator'),
    statusText: document.getElementById('statusText'),
    currentCategory: document.getElementById('currentCategory'),
    poseTabs: document.getElementById('poseTabs'),
    poseName: document.getElementById('poseName'),
    poseCounter: document.getElementById('poseCounter'),
    poseDescription: document.getElementById('poseDescription'),
    poseInstructions: document.getElementById('poseInstructions'),
    poseBenefits: document.getElementById('poseBenefits'),
    poseIllustration: document.getElementById('poseIllustration'),
    poseImageCaption: document.getElementById('poseImageCaption'),
    cameraPreview: document.getElementById('cameraPreview'),
    startCamera: document.getElementById('startCamera'),
    stopCamera: document.getElementById('stopCamera'),
    startTimer: document.getElementById('startTimer'),
    stopTimer: document.getElementById('stopTimer'),
    timerDisplay: document.getElementById('timerDisplay'),
    backBtn: document.getElementById('backBtn'),
    prevPose: document.getElementById('prevPose'),
    nextPose: document.getElementById('nextPose')
};

// Initialize the application
function init() {
    setupEventListeners();
    setupSpeechRecognition();
    updateVoiceStatus('Click "Start Listening" to use voice commands');
}

// Event Listeners
function setupEventListeners() {
    // Category selection
    elements.categoryCards.forEach(card => {
        card.addEventListener('click', () => {
            const category = card.dataset.category;
            selectCategory(category);
        });
    });

    // Navigation
    elements.backBtn.addEventListener('click', goBack);
    elements.prevPose.addEventListener('click', previousPose);
    elements.nextPose.addEventListener('click', nextPose);

    // Voice control
    elements.toggleVoice.addEventListener('click', toggleVoiceRecognition);

    // Camera controls
    elements.startCamera.addEventListener('click', startCamera);
    elements.stopCamera.addEventListener('click', stopCamera);

    // Timer controls
    elements.startTimer.addEventListener('click', startTimer);
    elements.stopTimer.addEventListener('click', stopTimer);
}

// Speech Recognition Setup
function setupSpeechRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        currentState.recognition = new SpeechRecognition();
        
        currentState.recognition.continuous = true;
        currentState.recognition.interimResults = false;
        currentState.recognition.lang = 'en-US';

        currentState.recognition.onstart = () => {
            updateVoiceStatus('Listening... Speak your command');
            elements.micIndicator.classList.add('listening');
        };

        currentState.recognition.onresult = (event) => {
            const command = event.results[event.results.length - 1][0].transcript.toLowerCase().trim();
            handleVoiceCommand(command);
            updateVoiceStatus(`Heard: "${command}"`);
        };

        currentState.recognition.onerror = (event) => {
            updateVoiceStatus(`Error: ${event.error}`);
            elements.micIndicator.classList.remove('listening');
        };

        currentState.recognition.onend = () => {
            elements.micIndicator.classList.remove('listening');
            if (currentState.isVoiceActive) {
                // Restart recognition if it should still be active
                setTimeout(() => {
                    if (currentState.isVoiceActive) {
                        currentState.recognition.start();
                    }
                }, 1000);
            }
        };
    } else {
        updateVoiceStatus('Speech recognition not supported in this browser');
        elements.toggleVoice.disabled = true;
    }
}

// Voice Command Handler
function handleVoiceCommand(command) {
    console.log('Voice command:', command);
    
    // Category selection
    if (command.includes('weight loss') || command.includes('weightloss')) {
        selectCategory('weight-loss');
        speak('Weight loss category selected. Starting with first pose.');
    } else if (command.includes('weight gain') || command.includes('weightgain')) {
        selectCategory('weight-gain');
        speak('Weight gain category selected. Starting with first pose.');
    } else if (command.includes('beginner')) {
        selectCategory('beginner');
        speak('Beginner category selected. Starting with first pose.');
    } else if (command.includes('regular')) {
        selectCategory('regular');
        speak('Regular category selected. Starting with first pose.');
    }
    
    // Navigation
    else if (command.includes('next pose') || command.includes('next')) {
        nextPose();
    } else if (command.includes('previous pose') || command.includes('previous') || command.includes('prev')) {
        previousPose();
    } else if (command.includes('back') || command.includes('go back')) {
        goBack();
    }
    
    // Camera controls
    else if (command.includes('start camera')) {
        startCamera();
        speak('Starting camera');
    } else if (command.includes('stop camera')) {
        stopCamera();
        speak('Stopping camera');
    }
    
    // Help
    else if (command.includes('help')) {
        speak('You can say: weight loss, weight gain, beginner, regular, next pose, previous pose, start camera, stop camera, or go back.');
    }
    
    else {
        speak('Sorry, I didn\'t understand that command. Try saying help for available commands.');
    }
}

// Text-to-Speech
function speak(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1;
        utterance.volume = 0.8;
        speechSynthesis.speak(utterance);
    }
}

// Voice Recognition Control
function toggleVoiceRecognition() {
    if (currentState.isVoiceActive) {
        stopVoiceRecognition();
    } else {
        startVoiceRecognition();
    }
}

function startVoiceRecognition() {
    if (currentState.recognition) {
        currentState.isVoiceActive = true;
        elements.toggleVoice.textContent = 'Stop Listening';
        elements.toggleVoice.classList.add('active');
        currentState.recognition.start();
        speak('Voice assistant activated. You can now use voice commands.');
    }
}

function stopVoiceRecognition() {
    currentState.isVoiceActive = false;
    elements.toggleVoice.textContent = 'Start Listening';
    elements.toggleVoice.classList.remove('active');
    elements.micIndicator.classList.remove('listening');
    
    if (currentState.recognition) {
        currentState.recognition.stop();
    }
    
    updateVoiceStatus('Voice commands stopped');
}

function updateVoiceStatus(message) {
    elements.statusText.textContent = message;
}

// Category Selection
function selectCategory(category) {
    currentState.category = category;
    currentState.poseIndex = 0;
    
    showPoseSection();
    updatePoseDisplay();
    
    const categoryName = category.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase());
    elements.currentCategory.textContent = categoryName;
}

// Pose Navigation
function nextPose() {
    if (currentState.category) {
        const poses = poseData[currentState.category];
        if (currentState.poseIndex < poses.length - 1) {
            currentState.poseIndex++;
            updatePoseDisplay();
            speak(`Moving to ${poses[currentState.poseIndex].name}`);
        } else {
            speak('This is the last pose in this category.');
        }
    }
}

function previousPose() {
    if (currentState.category && currentState.poseIndex > 0) {
        currentState.poseIndex--;
        updatePoseDisplay();
        const poses = poseData[currentState.category];
        speak(`Moving to ${poses[currentState.poseIndex].name}`);
    } else {
        speak('This is the first pose in this category.');
    }
}

function goBack() {
    showCategorySection();
    currentState.category = null;
    currentState.poseIndex = 0;
    speak('Returning to category selection.');
}

// Display Updates
function showCategorySection() {
    elements.categorySection.classList.remove('hidden');
    elements.poseSection.classList.add('hidden');
}

function showPoseSection() {
    elements.categorySection.classList.add('hidden');
    elements.poseSection.classList.remove('hidden');
}

function updatePoseDisplay() {
    if (!currentState.category) return;
    
    const poses = poseData[currentState.category];
    const currentPose = poses[currentState.poseIndex];
    
    // Create pose tabs
    createPoseTabs();
    
    // Update pose information
    elements.poseName.textContent = currentPose.name;
    elements.poseCounter.textContent = `${currentState.poseIndex + 1} / ${poses.length}`;
    elements.poseDescription.textContent = currentPose.description;
    elements.poseBenefits.textContent = currentPose.benefits;
    
    // Update instructions
    elements.poseInstructions.innerHTML = '';
    currentPose.instructions.forEach(instruction => {
        const li = document.createElement('li');
        li.textContent = instruction;
        elements.poseInstructions.appendChild(li);
    });
    
    // Update pose illustration
    if (currentPose.illustration && poseIllustrations[currentPose.illustration]) {
        elements.poseIllustration.innerHTML = poseIllustrations[currentPose.illustration];
        elements.poseImageCaption.textContent = `${currentPose.shortName} - Hold for ${currentPose.duration}`;
    }
    
    // Reset timer
    stopTimer();
    elements.timerDisplay.textContent = '00:00';
    currentState.timerSeconds = 0;
    
    // Update navigation buttons
    elements.prevPose.disabled = currentState.poseIndex === 0;
    elements.nextPose.disabled = currentState.poseIndex === poses.length - 1;
}

// Create Pose Selection Tabs
function createPoseTabs() {
    if (!currentState.category) return;
    
    const poses = poseData[currentState.category];
    elements.poseTabs.innerHTML = '';
    
    poses.forEach((pose, index) => {
        const tab = document.createElement('button');
        tab.className = `pose-tab ${index === currentState.poseIndex ? 'active' : ''}`;
        tab.textContent = pose.shortName;
        tab.addEventListener('click', () => {
            currentState.poseIndex = index;
            updatePoseDisplay();
            speak(`Switched to ${pose.name}`);
        });
        elements.poseTabs.appendChild(tab);
    });
}

// Pose Selection by Tab
function selectPose(poseIndex) {
    if (currentState.category) {
        const poses = poseData[currentState.category];
        if (poseIndex >= 0 && poseIndex < poses.length) {
            currentState.poseIndex = poseIndex;
            updatePoseDisplay();
            speak(`Switched to ${poses[poseIndex].name}`);
        }
    }
}

// Camera Functions
async function startCamera() {
    try {
        currentState.stream = await navigator.mediaDevices.getUserMedia({ 
            video: { width: 640, height: 480 }
        });
        
        elements.cameraPreview.srcObject = currentState.stream;
        elements.startCamera.classList.add('hidden');
        elements.stopCamera.classList.remove('hidden');
        
        currentState.isCameraActive = true;
        
        // Hide the placeholder overlay when camera starts
        const overlay = document.querySelector('.camera-overlay');
        overlay.style.display = 'none';
        
    } catch (error) {
        console.error('Error accessing camera:', error);
        speak('Unable to access camera. Please check permissions.');
        updateVoiceStatus('Camera access denied or unavailable');
    }
}

function stopCamera() {
    if (currentState.stream) {
        currentState.stream.getTracks().forEach(track => track.stop());
        currentState.stream = null;
    }
    
    elements.cameraPreview.srcObject = null;
    elements.startCamera.classList.remove('hidden');
    elements.stopCamera.classList.add('hidden');
    
    currentState.isCameraActive = false;
    
    // Show the placeholder overlay when camera stops
    const overlay = document.querySelector('.camera-overlay');
    overlay.style.display = 'flex';
}

// Timer Functions
function startTimer() {
    if (currentState.timer) {
        clearInterval(currentState.timer);
    }
    
    elements.startTimer.classList.add('hidden');
    elements.stopTimer.classList.remove('hidden');
    
    currentState.timer = setInterval(() => {
        currentState.timerSeconds++;
        updateTimerDisplay();
    }, 1000);
    
    speak('Timer started');
}

function stopTimer() {
    if (currentState.timer) {
        clearInterval(currentState.timer);
        currentState.timer = null;
    }
    
    elements.startTimer.classList.remove('hidden');
    elements.stopTimer.classList.add('hidden');
}

function updateTimerDisplay() {
    const minutes = Math.floor(currentState.timerSeconds / 60);
    const seconds = currentState.timerSeconds % 60;
    const display = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    elements.timerDisplay.textContent = display;
}

// Initialize the application when the page loads
document.addEventListener('DOMContentLoaded', init);
