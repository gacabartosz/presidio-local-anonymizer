// Presidio Anonymizer - Popup Script

const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const enabledToggle = document.getElementById('enabledToggle');
const openDashboardBtn = document.getElementById('openDashboard');

// Load settings
async function loadSettings() {
  const settings = await chrome.storage.local.get(['enabled']);
  enabledToggle.checked = settings.enabled !== false;

  // Check health
  checkHealth();
}

// Check API health
async function checkHealth() {
  try {
    const response = await chrome.runtime.sendMessage({ action: 'checkHealth' });

    if (response.success) {
      statusDot.className = 'dot online';
      statusText.textContent = 'Connected';
    } else {
      statusDot.className = 'dot offline';
      statusText.textContent = 'Offline';
    }
  } catch (error) {
    statusDot.className = 'dot offline';
    statusText.textContent = 'Backend not running';
  }
}

// Save enabled state
enabledToggle.addEventListener('change', async () => {
  await chrome.storage.local.set({ enabled: enabledToggle.checked });
  console.log('Anonymization:', enabledToggle.checked ? 'enabled' : 'disabled');
});

// Open dashboard
openDashboardBtn.addEventListener('click', () => {
  chrome.tabs.create({ url: 'http://127.0.0.1:4222/dashboard' });
});

// Initialize
loadSettings();
