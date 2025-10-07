let currentItem = null;
let defaultValues = {};
let currentValues = {};

// Theme toggle function
function toggleTheme() {
    const body = document.body;
    const themeToggle = document.querySelector('.theme-toggle i');
    
    if (body.classList.contains('dark-theme')) {
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        themeToggle.className = 'fas fa-sun';
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.remove('light-theme');
        body.classList.add('dark-theme');
        themeToggle.className = 'fas fa-moon';
        localStorage.setItem('theme', 'dark');
    }
}

// Load saved theme on page load
function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    const body = document.body;
    const themeToggle = document.querySelector('.theme-toggle i');
    
    if (savedTheme === 'light') {
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        themeToggle.className = 'fas fa-sun';
    } else {
        body.classList.remove('light-theme');
        body.classList.add('dark-theme');
        themeToggle.className = 'fas fa-moon';
    }
}

// Update datetime
function updateDateTime() {
    const now = new Date();
    const options = {
        month: 'numeric',
        day: 'numeric',
        year: 'numeric',
        hour: 'numeric',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
    };
    document.getElementById('datetime').textContent = now.toLocaleString('en-US', options);
}

// Initialize page
function initializePage() {
    updateDateTime();
    setInterval(updateDateTime, 1000);
    loadItemData();
    initializeDefaultValues();
}

// Initialize default values
function initializeDefaultValues() {
    defaultValues = {
        // Stacking Arm defaults
        stackingZLimit: 25.5,
        stackingXPosition: 120.0,
        stackingXStacking: 85.0,
        stackingSpeedX: 150.0,
        stackingSpeedZ: 100.0,
        stackingGapChange: 5.0,
        stackingOperatingItems: 4,
        
        // High Speed Arm defaults
        highSpeedZPosition: 45.0,
        highSpeedYBed: 200.0,
        highSpeedYEdge: 175.0,
        highSpeedMoving: 300.0,
        highSpeedOperatingItems: 4,
        
        // Moving Bed defaults
        movingBedOperatingItems: 4,
        movingBedYTaking: 150.0,
        movingBedYTakeOut: 250.0,
        movingBedSpeed: 200.0
    };
}

// Load item data
function loadItemData() {
    const editItemId = localStorage.getItem('editItemId') || 
                      (JSON.parse(localStorage.getItem('selectedItem') || '{}').id);
    if (!editItemId) {
        goBack();
        return;
    }
    
    const items = JSON.parse(localStorage.getItem('analyticsItems')) || [];
    currentItem = items.find(item => item.id == editItemId);
    
    if (!currentItem) {
        goBack();
        return;
    }
    
    // Update header
    document.getElementById('itemTitle').textContent = `${currentItem.name} Settings`;
    document.getElementById('itemSubtitle').textContent = `Configure parameters for ${currentItem.name} (${currentItem.weight}g ${currentItem.type})`;
    
    // Load saved settings
    loadSettings();
    
    // Clean up editItemId if it was used
    localStorage.removeItem('editItemId');
}

// Load settings from localStorage
function loadSettings() {
    const settingsKey = `itemSettings_${currentItem.id}`;
    const savedSettings = JSON.parse(localStorage.getItem(settingsKey)) || {};
    
    // Initialize current values with defaults
    currentValues = { ...defaultValues };
    
    // Override with saved settings
    Object.keys(savedSettings).forEach(key => {
        if (currentValues.hasOwnProperty(key)) {
            currentValues[key] = savedSettings[key];
        }
    });
    
    // Update display
    updateAllDisplays();
}

// Update all value displays
function updateAllDisplays() {
    Object.keys(currentValues).forEach(key => {
        const element = document.getElementById(key);
        if (element) {
            if (key.includes('OperatingItems')) {
                element.value = currentValues[key];
            } else {
                element.textContent = parseFloat(currentValues[key]).toFixed(1);
            }
        }
    });
}

// Adjust value function
function adjustValue(fieldId, increment) {
    if (!currentValues.hasOwnProperty(fieldId)) return;
    
    const currentValue = parseFloat(currentValues[fieldId]);
    const newValue = currentValue + increment;
    
    // Set minimum value to 0
    currentValues[fieldId] = Math.max(0, parseFloat(newValue.toFixed(1)));
    
    // Update display
    const element = document.getElementById(fieldId);
    if (element) {
        element.textContent = currentValues[fieldId].toFixed(1);
        
        // Add animation class
        const valueDisplay = element.parentElement;
        valueDisplay.classList.add('changed');
        setTimeout(() => {
            valueDisplay.classList.remove('changed');
        }, 300);
    }
}

// Individual button functions for backend connection

// Stacking Arm Functions
function stackingZLimitMinus() {
    adjustValue('stackingZLimit', -0.1);
    // Add your backend call here
    console.log('Stacking Z Limit decreased to:', currentValues.stackingZLimit);
}

function stackingZLimitPlus() {
    adjustValue('stackingZLimit', 0.1);
    // Add your backend call here
    console.log('Stacking Z Limit increased to:', currentValues.stackingZLimit);
}

function stackingXPositionMinus() {
    adjustValue('stackingXPosition', -0.1);
    // Add your backend call here
    console.log('Stacking X Position decreased to:', currentValues.stackingXPosition);
}

function stackingXPositionPlus() {
    adjustValue('stackingXPosition', 0.1);
    // Add your backend call here
    console.log('Stacking X Position increased to:', currentValues.stackingXPosition);
}

function stackingXStackingMinus() {
    adjustValue('stackingXStacking', -0.1);
    // Add your backend call here
    console.log('Stacking X Stacking decreased to:', currentValues.stackingXStacking);
}

function stackingXStackingPlus() {
    adjustValue('stackingXStacking', 0.1);
    // Add your backend call here
    console.log('Stacking X Stacking increased to:', currentValues.stackingXStacking);
}

function stackingSpeedXMinus() {
    adjustValue('stackingSpeedX', -0.1);
    // Add your backend call here
    console.log('Stacking Speed X decreased to:', currentValues.stackingSpeedX);
}

function stackingSpeedXPlus() {
    adjustValue('stackingSpeedX', 0.1);
    // Add your backend call here
    console.log('Stacking Speed X increased to:', currentValues.stackingSpeedX);
}

function stackingSpeedZMinus() {
    adjustValue('stackingSpeedZ', -0.1);
    // Add your backend call here
    console.log('Stacking Speed Z decreased to:', currentValues.stackingSpeedZ);
}

function stackingSpeedZPlus() {
    adjustValue('stackingSpeedZ', 0.1);
    // Add your backend call here
    console.log('Stacking Speed Z increased to:', currentValues.stackingSpeedZ);
}

function stackingGapChangeMinus() {
    adjustValue('stackingGapChange', -0.1);
    // Add your backend call here
    console.log('Stacking Gap Change decreased to:', currentValues.stackingGapChange);
}

function stackingGapChangePlus() {
    adjustValue('stackingGapChange', 0.1);
    // Add your backend call here
    console.log('Stacking Gap Change increased to:', currentValues.stackingGapChange);
}

function stackingOperatingItemsChange(value) {
    currentValues.stackingOperatingItems = parseInt(value);
    // Add your backend call here
    console.log('Stacking Operating Items changed to:', currentValues.stackingOperatingItems);
}

// High Speed Arm Functions
function highSpeedZPositionMinus() {
    adjustValue('highSpeedZPosition', -0.1);
    // Add your backend call here
    console.log('High Speed Z Position decreased to:', currentValues.highSpeedZPosition);
}

function highSpeedZPositionPlus() {
    adjustValue('highSpeedZPosition', 0.1);
    // Add your backend call here
    console.log('High Speed Z Position increased to:', currentValues.highSpeedZPosition);
}

function highSpeedYBedMinus() {
    adjustValue('highSpeedYBed', -0.1);
    // Add your backend call here
    console.log('High Speed Y Bed decreased to:', currentValues.highSpeedYBed);
}

function highSpeedYBedPlus() {
    adjustValue('highSpeedYBed', 0.1);
    // Add your backend call here
    console.log('High Speed Y Bed increased to:', currentValues.highSpeedYBed);
}

function highSpeedYEdgeMinus() {
    adjustValue('highSpeedYEdge', -0.1);
    // Add your backend call here
    console.log('High Speed Y Edge decreased to:', currentValues.highSpeedYEdge);
}

function highSpeedYEdgePlus() {
    adjustValue('highSpeedYEdge', 0.1);
    // Add your backend call here
    console.log('High Speed Y Edge increased to:', currentValues.highSpeedYEdge);
}

function highSpeedMovingMinus() {
    adjustValue('highSpeedMoving', -0.1);
    // Add your backend call here
    console.log('High Speed Moving decreased to:', currentValues.highSpeedMoving);
}

function highSpeedMovingPlus() {
    adjustValue('highSpeedMoving', 0.1);
    // Add your backend call here
    console.log('High Speed Moving increased to:', currentValues.highSpeedMoving);
}

function highSpeedOperatingItemsChange(value) {
    currentValues.highSpeedOperatingItems = parseInt(value);
    // Add your backend call here
    console.log('High Speed Operating Items changed to:', currentValues.highSpeedOperatingItems);
}

// Moving Bed Functions
function movingBedOperatingItemsChange(value) {
    currentValues.movingBedOperatingItems = parseInt(value);
    // Add your backend call here
    console.log('Moving Bed Operating Items changed to:', currentValues.movingBedOperatingItems);
}

function movingBedYTakingMinus() {
    adjustValue('movingBedYTaking', -0.1);
    // Add your backend call here
    console.log('Moving Bed Y Taking decreased to:', currentValues.movingBedYTaking);
}

function movingBedYTakingPlus() {
    adjustValue('movingBedYTaking', 0.1);
    // Add your backend call here
    console.log('Moving Bed Y Taking increased to:', currentValues.movingBedYTaking);
}

function movingBedYTakeOutMinus() {
    adjustValue('movingBedYTakeOut', -0.1);
    // Add your backend call here
    console.log('Moving Bed Y Take Out decreased to:', currentValues.movingBedYTakeOut);
}

function movingBedYTakeOutPlus() {
    adjustValue('movingBedYTakeOut', 0.1);
    // Add your backend call here
    console.log('Moving Bed Y Take Out increased to:', currentValues.movingBedYTakeOut);
}

function movingBedSpeedMinus() {
    adjustValue('movingBedSpeed', -0.1);
    // Add your backend call here
    console.log('Moving Bed Speed decreased to:', currentValues.movingBedSpeed);
}

function movingBedSpeedPlus() {
    adjustValue('movingBedSpeed', 0.1);
    // Add your backend call here
    console.log('Moving Bed Speed increased to:', currentValues.movingBedSpeed);
}

// Default button functions
function stackingArmDefault() {
    resetToDefault('stacking');
    // Add your backend call here
    console.log('Stacking Arm reset to default values');
}

function highSpeedArmDefault() {
    resetToDefault('highSpeed');
    // Add your backend call here
    console.log('High Speed Arm reset to default values');
}

function movingBedDefault() {
    resetToDefault('movingBed');
    // Add your backend call here
    console.log('Moving Bed reset to default values');
}

// Reset to default values
function resetToDefault(section) {
    const sectionFields = {
        stacking: [
            'stackingZLimit', 'stackingXPosition', 'stackingXStacking',
            'stackingSpeedX', 'stackingSpeedZ', 'stackingGapChange',
            'stackingOperatingItems'
        ],
        highSpeed: [
            'highSpeedZPosition', 'highSpeedYBed', 'highSpeedYEdge',
            'highSpeedMoving', 'highSpeedOperatingItems'
        ],
        movingBed: [
            'movingBedOperatingItems', 'movingBedYTaking',
            'movingBedYTakeOut', 'movingBedSpeed'
        ]
    };
    
    const fields = sectionFields[section];
    if (!fields) return;
    
    fields.forEach(fieldId => {
        if (defaultValues.hasOwnProperty(fieldId)) {
            currentValues[fieldId] = defaultValues[fieldId];
            
            const element = document.getElementById(fieldId);
            if (element) {
                if (fieldId.includes('OperatingItems')) {
                    element.value = currentValues[fieldId];
                } else {
                    element.textContent = currentValues[fieldId].toFixed(1);
                }
                
                // Add animation class
                if (!fieldId.includes('OperatingItems')) {
                    const valueDisplay = element.parentElement;
                    valueDisplay.classList.add('changed');
                    setTimeout(() => {
                        valueDisplay.classList.remove('changed');
                    }, 300);
                }
            }
        }
    });
    
    showNotification(`${section.charAt(0).toUpperCase() + section.slice(1)} values reset to default!`, 'info');
}

// Handle select changes
document.addEventListener('change', function(e) {
    if (e.target.classList.contains('operating-items-select')) {
        const fieldId = e.target.id;
        currentValues[fieldId] = parseInt(e.target.value);
    }
});

// Save settings
function saveSettings() {
    if (!currentItem) return;
    
    const settings = { ...currentValues };
    settings.lastModified = new Date().toISOString();
    
    const settingsKey = `itemSettings_${currentItem.id}`;
    localStorage.setItem(settingsKey, JSON.stringify(settings));
    
    showNotification('Settings saved successfully!', 'success');
}

// Go back to analytics
function goBack() {
    window.location.href = 'analytics.html';
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'info' ? 'info-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    
    const bgColor = type === 'success' ? 'var(--accent-green)' : 
                    type === 'info' ? 'var(--accent-blue)' : 'var(--accent-orange)';
    
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${bgColor};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 1001;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 500;
        animation: slideInRight 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-in forwards';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
`;
document.head.appendChild(style);

// Initialize page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    loadTheme();
    initializePage();
    setActiveNavTab();
});

// Set active navigation tab - item settings should show analytics as active
function setActiveNavTab() {
    const navTabs = document.querySelectorAll('.nav-tab');
    
    navTabs.forEach(tab => {
        tab.classList.remove('active');
        const href = tab.getAttribute('href');
        if (href && href.includes('analytics.html')) {
            tab.classList.add('active');
        }
    });
}

// Virtual Keyboard Functions (kept for compatibility)
function toggleKeyboard() {
    // Virtual keyboard is no longer needed with the new interface
    // But keeping function for navigation compatibility
}