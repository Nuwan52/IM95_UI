// Simple JavaScript functions for the machine control interface

var socket = io();

socket.on('INIT_BACKEND', function (data) {
    console.log(data.message)

    if (initBtn.classList.contains('active')) {
        initBtn.classList.remove('active');
        initBtn.innerHTML = '<i class="fas fa-check"></i><span>Initialized</span>';
        updateMachineStatus('initialized');
    }
});



function updateMachineStatus(status, description, icon) {
    const statusIndicator = document.querySelector('.status-indicator');
    const statusIcon = document.querySelector('.status-icon i');
    const statusTitle = document.querySelector('.status-title');
    const statusDescription = document.querySelector('.status-description');

    // Remove all status classes
    statusIndicator.classList.remove('running', 'stopped', 'initializing');

    // Update content based on status
    switch (status) {
        case 'running':
            statusIndicator.classList.add('running');
            statusIcon.className = 'fas fa-play-circle';
            statusTitle.textContent = 'Running';
            statusDescription.textContent = 'Machine is operating normally';
            break;
        case 'paused':
            statusIcon.className = 'fas fa-pause-circle';
            statusTitle.textContent = 'Paused';
            statusDescription.textContent = 'Machine operation paused';
            break;
        case 'stopped':
            statusIndicator.classList.add('stopped');
            statusIcon.className = 'fas fa-stop-circle';
            statusTitle.textContent = 'Emergency Stop';
            statusDescription.textContent = 'Machine stopped for safety';
            break;
        case 'initializing':
            statusIndicator.classList.add('initializing');
            statusIcon.className = 'fas fa-cog fa-spin';
            statusTitle.textContent = 'Initializing';
            statusDescription.textContent = 'System initialization in progress';
            break;
        case 'initialized':
            statusIndicator.classList.add('initializing');
            statusIcon.className = 'fas fa-check-circle';
            statusTitle.textContent = 'Initialized';
            statusDescription.textContent = 'System ready for operation';
            break;
    }
}

function initializeSystem() {
    const initBtn = document.getElementById('initBtn');
    socket.emit('INIT');

    if (initBtn.classList.contains('active')) {
        // Stop initialization
        initBtn.classList.remove('active');
        initBtn.innerHTML = '<i class="fas fa-cog"></i><span>Initializing</span>';
        updateMachineStatus('paused');
        console.log('System initialization stopped');
    } else {
        // Start initialization
        initBtn.classList.add('active');
        initBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Initializing...</span>';
        updateMachineStatus('initializing');
        console.log('System initialization started');

        // Simulate initialization process (optional)
        // setTimeout(() => {
        //     if (initBtn.classList.contains('active')) {
        //         initBtn.classList.remove('active');
        //         initBtn.innerHTML = '<i class="fas fa-check"></i><span>Initialized</span>';
        //         updateMachineStatus('initialized');

        //         // Reset button after 3 seconds
        //         setTimeout(() => {
        //             initBtn.innerHTML = '<i class="fas fa-cog"></i><span>Initializing</span>';
        //             updateMachineStatus('paused');
        //         }, 3000);
        //     }
        // }, 5000); // 5 second initialization process
    }
}

function toggleStartPause() {
    const startBtn = document.getElementById('startBtn');

    if (startBtn.classList.contains('running')) {
        // Change to Start state
        startBtn.classList.remove('running');
        startBtn.innerHTML = '<i class="fas fa-play"></i><span>Start</span>';
        updateMachineStatus('paused');
        console.log('Machine paused');
    } else {
        // Change to Pause state
        startBtn.classList.add('running');
        startBtn.innerHTML = '<i class="fas fa-pause"></i><span>Pause</span>';
        updateMachineStatus('running');
        console.log('Machine started');
    }
}

function emergencyStop() {
    const emergencyBtn = document.getElementById('emergencyBtn');
    const startBtn = document.getElementById('startBtn');
    const initBtn = document.getElementById('initBtn');

    if (emergencyBtn.classList.contains('active')) {
        // Reset emergency stop
        emergencyBtn.classList.remove('active');
        emergencyBtn.innerHTML = '<i class="fas fa-hand-paper"></i><span>Emergency Stop</span>';
        updateMachineStatus('paused');
        console.log('Emergency stop reset');
    } else {
        // Activate emergency stop
        emergencyBtn.classList.add('active');
        emergencyBtn.innerHTML = '<i class="fas fa-exclamation-triangle"></i><span>STOPPED</span>';
        updateMachineStatus('stopped');

        // Reset other buttons to safe state
        startBtn.classList.remove('running');
        startBtn.innerHTML = '<i class="fas fa-play"></i><span>Start</span>';

        initBtn.classList.remove('active');
        initBtn.innerHTML = '<i class="fas fa-cog"></i><span>Initializing</span>';

        console.log('Emergency stop activated');
    }
}

function toggleTheme() {
    const body = document.body;
    const themeToggle = document.querySelector('.theme-toggle i');

    if (body.classList.contains('dark-theme')) {
        // Switch to light theme
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        themeToggle.className = 'fas fa-sun';
        console.log('Switched to light theme');
        localStorage.setItem('theme', 'light');
    } else {
        // Switch to dark theme
        body.classList.remove('light-theme');
        body.classList.add('dark-theme');
        themeToggle.className = 'fas fa-moon';
        console.log('Switched to dark theme');
        localStorage.setItem('theme', 'dark');
    }
}

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

function toggleKeyboard() {
    // Existing keyboard toggle functionality
    console.log('Keyboard toggled');
}

function typeKey(key) {
    // Existing key typing functionality
    console.log('Key typed:', key);
}

function backspace() {
    // Existing backspace functionality
    console.log('Backspace pressed');
}

function enterKey() {
    // Existing enter key functionality
    console.log('Enter pressed');
}

function toggleCaps() {
    // Existing caps lock functionality
    console.log('Caps toggled');
}

loadTheme();