// Presidio Anonymizer - Popup Script

const statusDot = document.getElementById('statusDot');
const statusText = document.getElementById('statusText');
const enabledToggle = document.getElementById('enabledToggle');
const tokenInput = document.getElementById('tokenInput');
const saveTokenBtn = document.getElementById('saveToken');
const openDashboardBtn = document.getElementById('openDashboard');

// Load settings
async function loadSettings() {
  const settings = await chrome.storage.local.get(['enabled', 'apiToken']);

  enabledToggle.checked = settings.enabled !== false;
  if (settings.apiToken) {
    tokenInput.value = settings.apiToken;
  }

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

// Save token
saveTokenBtn.addEventListener('click', async () => {
  const token = tokenInput.value.trim();
  if (token) {
    await chrome.runtime.sendMessage({ action: 'setToken', token });
    await chrome.storage.local.set({ apiToken: token });
    alert('Token saved!');
    checkHealth();
  }
});

// Open dashboard
openDashboardBtn.addEventListener('click', () => {
  chrome.tabs.create({ url: 'http://127.0.0.1:4222/dashboard' });
});

// Initialize
loadSettings();
