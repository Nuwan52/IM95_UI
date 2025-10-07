// Servo motor position management
let servoPositions = {
    1: 0.0,
    2: 0.0,
    3: 0.0,
    4: 0.0,
    5: 0.0,
    6: 0.0,
    7: 0.0
};

// Position increment/decrement step
const POSITION_STEP = 0.1;

// Adjust servo position
function adjustPosition(motorId, change) {
    // Update the position
    servoPositions[motorId] += change;
    
    // Round to one decimal place to avoid floating point precision issues
    servoPositions[motorId] = Math.round(servoPositions[motorId] * 10) / 10;
    
    // Send position to backend
    setServoPosition(motorId, servoPositions[motorId]);
    
    // Update the display
    const positionElement = document.querySelector(`[data-motor="${motorId}"]`);
    if (positionElement) {
        positionElement.textContent = servoPositions[motorId].toFixed(1);
        
        // Add a subtle animation to show the change
        positionElement.style.transform = 'scale(1.1)';
        positionElement.style.color = change > 0 ? '#10b981' : '#ef4444';
        
        setTimeout(() => {
            positionElement.style.transform = 'scale(1)';
            positionElement.style.color = '';
        }, 200);
    }
    
    console.log(`Motor ${motorId} position: ${servoPositions[motorId]}`);
    
    // Save the updated positions
    saveServoPositions();
}

// Reset servo position to default (0.0)
function resetPosition(motorId) {
    servoPositions[motorId] = 0.0;
    
    // Send home command to backend
    homeServoMotor(motorId);
    
    // Update the display
    const positionElement = document.querySelector(`[data-motor="${motorId}"]`);
    if (positionElement) {
        positionElement.textContent = '0.0';
        
        // Add animation to show the reset
        positionElement.style.transform = 'scale(1.2)';
        positionElement.style.color = '#3b82f6';
        
        setTimeout(() => {
            positionElement.style.transform = 'scale(1)';
            positionElement.style.color = '';
        }, 300);
    }
    
    console.log(`Motor ${motorId} reset to default position: 0.0`);
    
    // Save the updated positions
    saveServoPositions();
}

// Save servo positions to localStorage
function saveServoPositions() {
    localStorage.setItem('servoPositions', JSON.stringify(servoPositions));
}

// Load servo positions from localStorage
function loadServoPositions() {
    const savedPositions = localStorage.getItem('servoPositions');
    if (savedPositions) {
        try {
            const loadedPositions = JSON.parse(savedPositions);
            servoPositions = { ...servoPositions, ...loadedPositions };
            
            // Update all position displays
            for (let i = 1; i <= 7; i++) {
                const positionElement = document.querySelector(`[data-motor="${i}"]`);
                if (positionElement && servoPositions[i] !== undefined) {
                    positionElement.textContent = servoPositions[i].toFixed(1);
                }
            }
        } catch (error) {
            console.error('Error loading servo positions:', error);
        }
    }
}

// Initialize servo positions on page load
document.addEventListener('DOMContentLoaded', function() {
    loadServoPositions();
});

// ===========================================
// SOLENOID CONTROL FUNCTIONS FOR BACKEND
// ===========================================

// Function to turn ON a specific solenoid
function turnOnSolenoid(solenoidId) {
    console.log(`Backend: Turning ON Solenoid ${solenoidId}`);
    // Add your backend API call here
    // Example: fetch('/api/solenoid/on', { method: 'POST', body: JSON.stringify({id: solenoidId}) })
}

// Function to turn OFF a specific solenoid
function turnOffSolenoid(solenoidId) {
    console.log(`Backend: Turning OFF Solenoid ${solenoidId}`);
    // Add your backend API call here
    // Example: fetch('/api/solenoid/off', { method: 'POST', body: JSON.stringify({id: solenoidId}) })
}

// Function to get solenoid status from backend
function getSolenoidStatus(solenoidId) {
    console.log(`Backend: Getting status for Solenoid ${solenoidId}`);
    // Add your backend API call here
    // Example: return fetch('/api/solenoid/status/' + solenoidId).then(response => response.json())
    return Promise.resolve({ id: solenoidId, status: 'off' }); // Mock response
}

// Function to get all solenoids status
function getAllSolenoidsStatus() {
    console.log('Backend: Getting all solenoids status');
    // Add your backend API call here
    // Example: return fetch('/api/solenoids/status').then(response => response.json())
    return Promise.resolve([]); // Mock response
}

// ===========================================
// SERVO MOTOR CONTROL FUNCTIONS FOR BACKEND
// ===========================================

// Function to set servo position
function setServoPosition(motorId, position) {
    console.log(`Backend: Setting Motor ${motorId} to position ${position}`);
    // Add your backend API call here
    // Example: fetch('/api/servo/position', { method: 'POST', body: JSON.stringify({id: motorId, position: position}) })
}

// Function to get servo position from backend
function getServoPosition(motorId) {
    console.log(`Backend: Getting position for Motor ${motorId}`);
    // Add your backend API call here
    // Example: return fetch('/api/servo/position/' + motorId).then(response => response.json())
    return Promise.resolve({ id: motorId, position: 0.0 }); // Mock response
}

// Function to get all servo positions
function getAllServoPositions() {
    console.log('Backend: Getting all servo positions');
    // Add your backend API call here
    // Example: return fetch('/api/servos/positions').then(response => response.json())
    return Promise.resolve({}); // Mock response
}

// Function to home/reset servo to default position
function homeServoMotor(motorId) {
    console.log(`Backend: Homing Motor ${motorId} to default position`);
    // Add your backend API call here
    // Example: fetch('/api/servo/home', { method: 'POST', body: JSON.stringify({id: motorId}) })
}

// ===========================================
// CAMERA CONTROL FUNCTIONS FOR BACKEND
// ===========================================

// Function to open camera settings
function openCameraSettings(cameraId) {
    console.log(`Backend: Opening settings for Camera ${cameraId}`);
    // Add your backend API call here
    // Example: fetch('/api/camera/settings/' + cameraId).then(response => response.json())
}

// Function to capture image from camera
function captureImage(cameraId) {
    console.log(`Backend: Capturing image from Camera ${cameraId}`);
    // Add your backend API call here
    // Example: fetch('/api/camera/capture', { method: 'POST', body: JSON.stringify({id: cameraId}) })
}

// Function to get camera status from backend
function getCameraStatus(cameraId) {
    console.log(`Backend: Getting status for Camera ${cameraId}`);
    // Add your backend API call here
    // Example: return fetch('/api/camera/status/' + cameraId).then(response => response.json())
    return Promise.resolve({ id: cameraId, status: 'good', signal: true }); // Mock response
}

// Function to get all cameras status
function getAllCamerasStatus() {
    console.log('Backend: Getting all cameras status');
    // Add your backend API call here
    // Example: return fetch('/api/cameras/status').then(response => response.json())
    return Promise.resolve([]); // Mock response
}

// Function to update camera quality status display
function updateCameraStatus(cameraId, isGood) {
    const cameraItem = document.querySelector(`.camera-item:nth-child(${cameraId})`);
    if (!cameraItem) return;
    
    const qualityStatus = cameraItem.querySelector('.quality-status');
    const icon = qualityStatus.querySelector('i');
    const text = qualityStatus.querySelector('span');
    
    if (isGood) {
        qualityStatus.classList.remove('not-good');
        qualityStatus.classList.add('good');
        icon.className = 'fas fa-check-circle';
        text.textContent = 'Good';
    } else {
        qualityStatus.classList.remove('good');
        qualityStatus.classList.add('not-good');
        icon.className = 'fas fa-times-circle';
        text.textContent = 'Not Good';
    }
    
    console.log(`Camera ${cameraId} status updated to: ${isGood ? 'Good' : 'Not Good'}`);
}

// Function to update all camera statuses from backend
function updateAllCameraStatuses() {
    getAllCamerasStatus().then(cameras => {
        cameras.forEach(camera => {
            updateCameraStatus(camera.id, camera.status === 'good');
        });
    }).catch(error => {
        console.error('Error updating camera statuses:', error);
    });
}

// ===========================================
// INTEGRATION FUNCTIONS
// ===========================================

// Function to sync all states with backend
function syncWithBackend() {
    console.log('Syncing all states with backend...');
    
    // Sync servo positions
    getAllServoPositions().then(positions => {
        for (const [motorId, position] of Object.entries(positions)) {
            if (servoPositions[motorId] !== undefined) {
                servoPositions[motorId] = position;
                const positionElement = document.querySelector(`[data-motor="${motorId}"]`);
                if (positionElement) {
                    positionElement.textContent = position.toFixed(1);
                }
            }
        }
    }).catch(error => {
        console.error('Error syncing servo positions:', error);
    });
    
    // Sync camera statuses
    updateAllCameraStatuses();
    
    // Sync solenoid statuses
    getAllSolenoidsStatus().then(solenoids => {
        solenoids.forEach(solenoid => {
            const solenoidItem = document.querySelector(`.solenoid-item:nth-child(${solenoid.id})`);
            if (solenoidItem) {
                const button = solenoidItem.querySelector('.toggle-btn');
                const statusIndicator = solenoidItem.querySelector('.status-indicator');
                const text = button.querySelector('span');
                
                if (solenoid.status === 'on') {
                    button.classList.remove('off');
                    button.classList.add('on');
                    statusIndicator.classList.remove('red');
                    statusIndicator.classList.add('green');
                    text.textContent = 'ON';
                } else {
                    button.classList.remove('on');
                    button.classList.add('off');
                    statusIndicator.classList.remove('green');
                    statusIndicator.classList.add('red');
                    text.textContent = 'OFF';
                }
            }
        });
    }).catch(error => {
        console.error('Error syncing solenoid statuses:', error);
    });
}

// Auto-sync with backend every 5 seconds (optional)
// setInterval(syncWithBackend, 5000);

// Virtual keyboard functionality
let isKeyboardVisible = false;
let activeInput = null;
let capsLock = false;

function toggleKeyboard() {
    const keyboard = document.getElementById('virtualKeyboard');
    isKeyboardVisible = !isKeyboardVisible;
    
    if (isKeyboardVisible) {
        keyboard.classList.add('show');
    } else {
        keyboard.classList.remove('show');
        activeInput = null;
    }
}

function typeKey(key) {
    if (activeInput) {
        if (capsLock && typeof key === 'string') {
            key = key.toUpperCase();
        }
        activeInput.value += key;
        activeInput.dispatchEvent(new Event('input'));
    }
}

function backspace() {
    if (activeInput) {
        activeInput.value = activeInput.value.slice(0, -1);
        activeInput.dispatchEvent(new Event('input'));
    }
}

function toggleCaps() {
    const capsButton = document.querySelector('.key.caps');
    capsLock = !capsLock;
    
    if (capsLock) {
        capsButton.classList.add('active');
    } else {
        capsButton.classList.remove('active');
    }
}

function enterKey() {
    if (activeInput) {
        activeInput.dispatchEvent(new Event('change'));
        toggleKeyboard();
    }
}

// Set active input when focusing on input fields
document.addEventListener('focusin', function(e) {
    if (e.target.matches('input[type="text"], input[type="number"], textarea')) {
        activeInput = e.target;
        if (!isKeyboardVisible) {
            toggleKeyboard();
        }
    }
});