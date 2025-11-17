// Options page script

const backendUrlInput = document.getElementById('backend-url');
const testBtn = document.getElementById('test-btn');
const saveBtn = document.getElementById('save-btn');
const resetBtn = document.getElementById('reset-btn');
const statusMessage = document.getElementById('status-message');

// Load saved configuration
document.addEventListener('DOMContentLoaded', async () => {
  await loadConfig();
  initializeTabs();
  initializeOSSelector();
  initializeInstallTestButtons();

  testBtn.addEventListener('click', testConnection);
  saveBtn.addEventListener('click', saveConfig);
  resetBtn.addEventListener('click', resetConfig);
});

// Initialize tab switching
function initializeTabs() {
  const tabButtons = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  tabButtons.forEach(button => {
    button.addEventListener('click', () => {
      const targetTab = button.dataset.tab;

      // Remove active class from all tabs
      tabButtons.forEach(btn => btn.classList.remove('active'));
      tabContents.forEach(content => content.classList.remove('active'));

      // Add active class to clicked tab
      button.classList.add('active');
      document.getElementById(`tab-${targetTab}`).classList.add('active');
    });
  });
}

// Initialize OS selector
function initializeOSSelector() {
  const osButtons = document.querySelectorAll('.os-btn');
  const osInstructions = document.querySelectorAll('.os-instructions');

  osButtons.forEach(button => {
    button.addEventListener('click', () => {
      const selectedOS = button.dataset.os;

      // Remove active class from all OS buttons
      osButtons.forEach(btn => btn.classList.remove('active'));

      // Hide all instructions
      osInstructions.forEach(instructions => {
        instructions.classList.add('hidden');
      });

      // Show selected OS instructions
      button.classList.add('active');
      document.getElementById(`install-${selectedOS}`).classList.remove('hidden');
    });
  });

  // Auto-detect OS and select appropriate button
  detectAndSelectOS(osButtons);
}

// Detect user's OS and auto-select
function detectAndSelectOS(osButtons) {
  const userAgent = navigator.userAgent.toLowerCase();
  let detectedOS = 'windows'; // default

  if (userAgent.indexOf('mac') !== -1) {
    detectedOS = 'mac';
  } else if (userAgent.indexOf('linux') !== -1) {
    detectedOS = 'linux';
  } else if (userAgent.indexOf('win') !== -1) {
    detectedOS = 'windows';
  }

  // Auto-click the detected OS button
  osButtons.forEach(button => {
    if (button.dataset.os === detectedOS) {
      button.click();
    }
  });
}

// Initialize test connection buttons in installation wizard
function initializeInstallTestButtons() {
  const testButtons = [
    document.getElementById('test-connection-windows'),
    document.getElementById('test-connection-mac'),
    document.getElementById('test-connection-linux')
  ];

  testButtons.forEach(button => {
    if (button) {
      button.addEventListener('click', testConnection);
    }
  });
}

// Load config from storage
async function loadConfig() {
  try {
    const result = await chrome.storage.sync.get(['backendUrl']);
    if (result.backendUrl) {
      backendUrlInput.value = result.backendUrl;
    }
  } catch (error) {
    showStatus('Błąd wczytywania konfiguracji: ' + error.message, 'error');
  }
}

// Test backend connection
async function testConnection() {
  const url = backendUrlInput.value.trim();

  if (!url) {
    showStatus('Wprowadź URL backendu', 'error');
    return;
  }

  testBtn.disabled = true;
  testBtn.textContent = '⏳ Testowanie...';

  try {
    const response = await chrome.runtime.sendMessage({
      action: 'testConnection',
      url: url
    });

    if (response.success) {
      showStatus(`✅ Połączenie udane! Status: ${response.status}`, 'success');
    } else {
      showStatus(`❌ Połączenie nieudane: ${response.message}`, 'error');
    }
  } catch (error) {
    showStatus('❌ Błąd testowania: ' + error.message, 'error');
  } finally {
    testBtn.disabled = false;
    testBtn.textContent = '🔍 Testuj Połączenie';
  }
}

// Save configuration
async function saveConfig() {
  const url = backendUrlInput.value.trim();

  if (!url) {
    showStatus('Wprowadź URL backendu', 'error');
    return;
  }

  // Validate URL format
  try {
    new URL(url);
  } catch (error) {
    showStatus('Nieprawidłowy format URL', 'error');
    return;
  }

  saveBtn.disabled = true;
  saveBtn.textContent = '⏳ Zapisywanie...';

  try {
    await chrome.storage.sync.set({ backendUrl: url });
    showStatus('✅ Konfiguracja zapisana pomyślnie!', 'success');
  } catch (error) {
    showStatus('❌ Błąd zapisu: ' + error.message, 'error');
  } finally {
    saveBtn.disabled = false;
    saveBtn.textContent = '💾 Zapisz';
  }
}

// Reset to defaults
async function resetConfig() {
  backendUrlInput.value = 'http://localhost:4222';
  
  try {
    await chrome.storage.sync.set({ backendUrl: 'http://localhost:4222' });
    showStatus('✅ Przywrócono ustawienia domyślne', 'success');
  } catch (error) {
    showStatus('❌ Błąd resetowania: ' + error.message, 'error');
  }
}

// Show status message
function showStatus(message, type) {
  statusMessage.textContent = message;
  statusMessage.className = `status-box ${type}`;
  statusMessage.classList.remove('hidden');

  if (type === 'success') {
    setTimeout(() => {
      statusMessage.classList.add('hidden');
    }, 5000);
  }
}
