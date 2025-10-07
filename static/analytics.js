let items = JSON.parse(localStorage.getItem('analyticsItems')) || [];
let selectedItem = null;
let editingItemId = null;
let isTrialRunning = false;
let keyboardVisible = false;
let activeInput = null;
let capsLock = false;

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
    renderItemTable();
    setupInputFocus();
}

// ===========================================
// BACKEND CONNECTION FUNCTIONS
// ===========================================

// Individual button functions for backend connection
async function handleAddNewItem() {
    console.log('Add New Item button clicked');
    // TODO: Connect to backend API
    // Example: await fetch('/api/items/add', { method: 'POST', ... });
    showAddItemModal();
}

async function handleSelectItem(itemId) {
    console.log('Select Item button clicked for item ID:', itemId);
    // TODO: Connect to backend API
    // Example: await fetch(`/api/items/${itemId}/select`, { method: 'POST' });
    selectItem(itemId);
}

async function handleEditItem(itemId) {
    console.log('Edit Item button clicked for item ID:', itemId);
    // TODO: Connect to backend API
    // Example: const itemData = await fetch(`/api/items/${itemId}`);
    editItem(itemId);
}

async function handleClearSelection() {
    console.log('Clear Selection button clicked');
    // TODO: Connect to backend API
    // Example: await fetch('/api/selection/clear', { method: 'POST' });
    clearSelection();
}

async function handleTrialRun() {
    console.log('Trial Run button clicked for item:', selectedItem);
    // TODO: Connect to backend API
    // Example: await fetch('/api/trial-run', { method: 'POST', body: JSON.stringify(selectedItem) });
    runTrialRun();
}

async function handleEditSettings() {
    console.log('Edit Settings button clicked for item:', selectedItem);
    // TODO: Connect to backend API
    // Example: await fetch(`/api/items/${selectedItem.id}/settings`);
    editSelectedItemSettings();
}

async function handleDeleteItem() {
    console.log('Delete Item button clicked for item:', selectedItem);
    // TODO: Connect to backend API
    // Example: await fetch(`/api/items/${selectedItem.id}`, { method: 'DELETE' });
    deleteSelectedItem();
}

async function handleSaveNewItem() {
    console.log('Save New Item button clicked');
    // TODO: Connect to backend API
    // Example: await fetch('/api/items', { method: 'POST', body: JSON.stringify(itemData) });
    saveNewItem();
}

async function handleSaveEditedItem() {
    console.log('Save Edited Item button clicked');
    // TODO: Connect to backend API
    // Example: await fetch(`/api/items/${editingItemId}`, { method: 'PUT', body: JSON.stringify(itemData) });
    saveEditedItem();
}

// ===========================================
// EXISTING FUNCTIONS (Modified to use backend handlers)
// ===========================================

// Run trial run for selected item
async function runTrialRun() {
    if (!selectedItem || isTrialRunning) return;
    
    isTrialRunning = true;
    const trialRunBtn = document.getElementById('trialRunBtn');
    const trialRunText = document.getElementById('trialRunText');
    
    // Update button appearance
    trialRunBtn.classList.add('running');
    trialRunBtn.disabled = true;
    trialRunText.textContent = 'Running...';
    
    showNotification(`Starting trial run for "${selectedItem.name}"...`, 'info');
    
    try {
        // Phase 1: Initialization
        await sleep(800);
        showNotification('Initializing machine parameters...', 'info');
        
        // Phase 2: Item positioning
        await sleep(1200);
        showNotification('Positioning item for testing...', 'info');
        
        // Phase 3: Weight verification
        await sleep(1000);
        showNotification(`Verifying weight: ${selectedItem.weight}g`, 'info');
        
        // Phase 4: Trial execution
        await sleep(1500);
        showNotification('Executing trial run...', 'info');
        
        // Phase 5: Completion
        await sleep(800);
        showNotification(`Trial run completed successfully for "${selectedItem.name}"!`, 'success');
        
    } catch (error) {
        showNotification('Trial run failed. Please check machine status.', 'error');
    } finally {
        // Reset button appearance
        isTrialRunning = false;
        trialRunBtn.classList.remove('running');
        trialRunBtn.disabled = false;
        trialRunText.textContent = 'Trial Run';
    }
}

// Helper function for delays
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Show add item modal
function showAddItemModal() {
    document.getElementById('addItemModal').classList.add('show');
    document.getElementById('itemName').focus();
    // Show numeric keypad for item name input
    showNumericKeypad();
}

// Close add item modal
function closeAddItemModal() {
    document.getElementById('addItemModal').classList.remove('show');
    document.getElementById('addItemForm').reset();
    hideNumericKeypad();
}

// Save new item
function saveNewItem() {
    const form = document.getElementById('addItemForm');
    const formData = new FormData(form);
    
    const newItem = {
        id: Date.now(),
        name: formData.get('itemName').trim(),
        weight: parseInt(formData.get('itemWeight')),
        type: formData.get('itemType'),
        createdDate: new Date().toLocaleDateString(),
    };
    
    // Validate item name uniqueness
    if (items.some(item => item.name.toLowerCase() === newItem.name.toLowerCase())) {
        alert('An item with this name already exists!');
        return;
    }
    
    items.push(newItem);
    localStorage.setItem('analyticsItems', JSON.stringify(items));
    
    renderItemTable();
    closeAddItemModal();
    
    // Show success message
    showNotification('Item added successfully!', 'success');
}

// Render item table
function renderItemTable() {
    const tbody = document.getElementById('itemTableBody');
    
    if (items.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; padding: 2rem; color: var(--text-muted);">
                    <i class="fas fa-inbox" style="font-size: 2rem; margin-bottom: 1rem; display: block;"></i>
                    No items found. Click "Add New Item" to get started.
                </td>
            </tr>
        `;
        return;
    }
    
    tbody.innerHTML = items.map(item => `
        <tr ${selectedItem && selectedItem.id === item.id ? 'class="selected"' : ''}>
            <td style="font-weight: 600; color: var(--text-primary);">${item.name}</td>
            <td>${item.weight}g</td>
            <td><span class="type-badge ${item.type.toLowerCase()}">${item.type}</span></td>
            <td>${item.createdDate}</td>
            <td>
                <button class="btn btn-success btn-small" onclick="handleSelectItem(${item.id})" style="margin-right: 0.5rem;">
                    <i class="fas fa-check"></i>
                    Select
                </button>
                <button class="btn btn-primary btn-small" onclick="event.stopPropagation(); handleEditItem(${item.id})">
                    <i class="fas fa-edit"></i>
                    Edit
                </button>
            </td>
        </tr>
    `).join('');
}

// Select item
function selectItem(itemId) {
    selectedItem = items.find(item => item.id === itemId);
    // Save selected item to localStorage
    localStorage.setItem('selectedItem', JSON.stringify(selectedItem));
    renderItemTable();
    displaySelectedItem();
    
    // Enable action buttons
    document.getElementById('clearSelectionBtn').disabled = false;
    document.getElementById('trialRunBtn').disabled = false;
    document.getElementById('editSelectedSettingsBtn').disabled = false;
    document.getElementById('deleteSelectedBtn').disabled = false;
}

// Clear selection
function clearSelection() {
    selectedItem = null;
    // Remove selected item from localStorage
    localStorage.removeItem('selectedItem');
    renderItemTable();
    displaySelectedItem();
    
    // Disable action buttons
    document.getElementById('clearSelectionBtn').disabled = true;
    document.getElementById('trialRunBtn').disabled = true;
    document.getElementById('editSelectedSettingsBtn').disabled = true;
    document.getElementById('deleteSelectedBtn').disabled = true;
}

// Display selected item
function displaySelectedItem() {
    const display = document.getElementById('selectedItemDisplay');
    
    if (!selectedItem) {
        display.innerHTML = `
            <div class="no-selection">
                <i class="fas fa-mouse-pointer"></i>
                <span>No item selected. Click on an item from the list below to view details.</span>
            </div>
        `;
        return;
    }
    
    display.innerHTML = `
        <div class="selected-item-name">
            <i class="fas fa-cube"></i>
            <span>${selectedItem.name}</span>
        </div>
    `;
}

// Edit item (redirect to settings page)
function editItem(itemId) {
    const item = items.find(item => item.id === itemId);
    if (!item) return;
    
    editingItemId = itemId;
    
    // Populate edit form
    document.getElementById('editItemName').value = item.name;
    document.getElementById('editItemWeight').value = item.weight;
    document.getElementById('editItemType').value = item.type;
    
    // Show edit modal
    document.getElementById('editItemModal').classList.add('show');
    document.getElementById('editItemName').focus();
}

// Show edit item modal
function showEditItemModal() {
    document.getElementById('editItemModal').classList.add('show');
    document.getElementById('editItemName').focus();
}

// Close edit item modal
function closeEditItemModal() {
    document.getElementById('editItemModal').classList.remove('show');
    document.getElementById('editItemForm').reset();
    editingItemId = null;
}

// Save edited item
function saveEditedItem() {
    if (!editingItemId) return;
    
    const form = document.getElementById('editItemForm');
    const formData = new FormData(form);
    
    const newName = formData.get('itemName').trim();
    const newWeight = parseInt(formData.get('itemWeight'));
    const newType = formData.get('itemType');
    
    // Validate item name uniqueness (excluding current item)
    if (items.some(item => item.id !== editingItemId && item.name.toLowerCase() === newName.toLowerCase())) {
        alert('An item with this name already exists!');
        return;
    }
    
    // Update item
    const itemIndex = items.findIndex(item => item.id === editingItemId);
    if (itemIndex !== -1) {
        items[itemIndex].name = newName;
        items[itemIndex].weight = newWeight;
        items[itemIndex].type = newType;
        
        // Update selected item if it's the one being edited
        if (selectedItem && selectedItem.id === editingItemId) {
            selectedItem = items[itemIndex];
            localStorage.setItem('selectedItem', JSON.stringify(selectedItem));
            displaySelectedItem();
        }
        
        localStorage.setItem('analyticsItems', JSON.stringify(items));
        renderItemTable();
        closeEditItemModal();
        
        showNotification('Item updated successfully!', 'success');
    }
}

// Edit item settings (redirect to settings page)
function editItemSettings(itemId) {
    localStorage.setItem('editItemId', itemId);
    window.location.href = 'item-settings';
}

// Edit selected item settings
function editSelectedItemSettings() {
    if (selectedItem) {
        editItemSettings(selectedItem.id);
    }
}

// Delete selected item
function deleteSelectedItem() {
    if (!selectedItem) return;
    
    if (confirm(`Are you sure you want to delete "${selectedItem.name}"?`)) {
        items = items.filter(item => item.id !== selectedItem.id);
        localStorage.setItem('analyticsItems', JSON.stringify(items));
        
        selectedItem = null;
        document.getElementById('clearSelectionBtn').disabled = true;
        document.getElementById('trialRunBtn').disabled = true;
        document.getElementById('editSelectedSettingsBtn').disabled = true;
        document.getElementById('deleteSelectedBtn').disabled = true;
        
        renderItemTable();
        displaySelectedItem();
        
        showNotification('Item deleted successfully!', 'success');
    }
}

// ===========================================
// NUMERIC KEYPAD FUNCTIONS
// ===========================================

// Show numeric keypad
function showNumericKeypad() {
    const keypad = document.getElementById('numericKeypad');
    if (keypad) {
        keypad.classList.add('show');
    }
}

// Hide numeric keypad
function hideNumericKeypad() {
    const keypad = document.getElementById('numericKeypad');
    if (keypad) {
        keypad.classList.remove('show');
    }
}

// Type number on keypad
function typeNumber(number) {
    if (!activeInput) return;
    
    const currentValue = activeInput.value;
    const cursorPos = activeInput.selectionStart;
    
    activeInput.value = currentValue.slice(0, cursorPos) + number + currentValue.slice(cursorPos);
    activeInput.setSelectionRange(cursorPos + 1, cursorPos + 1);
    activeInput.focus();
    
    // Trigger input event for any listeners
    activeInput.dispatchEvent(new Event('input', { bubbles: true }));
}

// Clear input on keypad
function clearInput() {
    if (!activeInput) return;
    
    activeInput.value = '';
    activeInput.focus();
    
    // Trigger input event for any listeners
    activeInput.dispatchEvent(new Event('input', { bubbles: true }));
}

// Backspace on keypad
function backspaceKeypad() {
    if (!activeInput) return;
    
    const currentValue = activeInput.value;
    const cursorPos = activeInput.selectionStart;
    
    if (cursorPos > 0) {
        activeInput.value = currentValue.slice(0, cursorPos - 1) + currentValue.slice(cursorPos);
        activeInput.setSelectionRange(cursorPos - 1, cursorPos - 1);
        activeInput.focus();
        
        // Trigger input event for any listeners
        activeInput.dispatchEvent(new Event('input', { bubbles: true }));
    }
}

// ===========================================
// NOTIFICATION SYSTEM
// ===========================================

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" style="background: none; border: none; color: white; font-size: 1.2rem; cursor: pointer; margin-left: 1rem;">&times;</button>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: var(--accent-${type === 'success' ? 'green' : type === 'error' ? 'red' : 'blue'});
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
        max-width: 400px;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-in forwards';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Close modal when clicking outside
document.getElementById('addItemModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeAddItemModal();
    }
});

// Close edit modal when clicking outside
document.getElementById('editItemModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeEditItemModal();
    }
});

// Handle form submission
document.getElementById('addItemForm').addEventListener('submit', function(e) {
    e.preventDefault();
    handleSaveNewItem();
});

// Handle edit form submission
document.getElementById('editItemForm').addEventListener('submit', function(e) {
    e.preventDefault();
    handleSaveEditedItem();
});

// Initialize page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    loadTheme();
    initializePage();
    loadSelectedItem();
    setActiveNavTab();
});

// Set active navigation tab based on current page
function setActiveNavTab() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navTabs = document.querySelectorAll('.nav-tab');
    
    navTabs.forEach(tab => {
        tab.classList.remove('active');
        const href = tab.getAttribute('href');
        if (href && href.includes(currentPage)) {
            tab.classList.add('active');
        }
    });
}

// Load selected item from localStorage
function loadSelectedItem() {
    const savedSelectedItem = localStorage.getItem('selectedItem');
    if (savedSelectedItem) {
        selectedItem = JSON.parse(savedSelectedItem);
        displaySelectedItem();
        
        // Enable action buttons
        document.getElementById('clearSelectionBtn').disabled = false;
        document.getElementById('trialRunBtn').disabled = false;
        document.getElementById('editSelectedSettingsBtn').disabled = false;
        document.getElementById('deleteSelectedBtn').disabled = false;
    }
}

// Virtual Keyboard Functions
function toggleKeyboard() {
    const keyboard = document.getElementById('virtualKeyboard');
    keyboardVisible = !keyboardVisible;
    
    if (keyboardVisible) {
        keyboard.classList.add('show');
    } else {
        keyboard.classList.remove('show');
        activeInput = null;
    }
}

function typeKey(key) {
    if (!activeInput) return;
    
    const currentValue = activeInput.value;
    const cursorPos = activeInput.selectionStart;
    
    let keyToType = capsLock ? key.toUpperCase() : key.toLowerCase();
    
    activeInput.value = currentValue.slice(0, cursorPos) + keyToType + currentValue.slice(cursorPos);
    activeInput.setSelectionRange(cursorPos + 1, cursorPos + 1);
    activeInput.focus();
    
    // Trigger input event for any listeners
    activeInput.dispatchEvent(new Event('input', { bubbles: true }));
}

function backspace() {
    if (!activeInput) return;
    
    const currentValue = activeInput.value;
    const cursorPos = activeInput.selectionStart;
    
    if (cursorPos > 0) {
        activeInput.value = currentValue.slice(0, cursorPos - 1) + currentValue.slice(cursorPos);
        activeInput.setSelectionRange(cursorPos - 1, cursorPos - 1);
        activeInput.focus();
        
        // Trigger input event for any listeners
        activeInput.dispatchEvent(new Event('input', { bubbles: true }));
    }
}

function toggleCaps() {
    capsLock = !capsLock;
    const capsButton = document.querySelector('.key.caps');
    
    if (capsLock) {
        capsButton.classList.add('active');
    } else {
        capsButton.classList.remove('active');
    }
}

function enterKey() {
    if (activeInput) {
        activeInput.blur();
        activeInput = null;
    }
}

function setupInputFocus() {
    // Add event listeners to all input fields
    document.addEventListener('focusin', function(e) {
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
            activeInput = e.target;
        }
    });
    
    document.addEventListener('focusout', function(e) {
        if (e.target === activeInput) {
            // Small delay to allow clicking keyboard keys
            setTimeout(() => {
                if (document.activeElement !== activeInput) {
                    activeInput = null;
                }
            }, 100);
        }
    });
}