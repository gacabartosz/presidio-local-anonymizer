// Popup script for Presidio Browser Anonymizer

let currentBackendUrl = '';

// Initialize popup
document.addEventListener('DOMContentLoaded', async () => {
  await loadBackendUrl();
  await checkBackendStatus();

  // Add event listeners for buttons
  document.getElementById('settings-btn')?.addEventListener('click', openSettings);
  document.getElementById('dashboard-btn')?.addEventListener('click', openDashboard);
  document.getElementById('options-btn')?.addEventListener('click', openOptions);
});

// Load backend URL from storage
async function loadBackendUrl() {
  try {
    const response = await chrome.runtime.sendMessage({ action: 'getBackendUrl' });
    if (response.success) {
      currentBackendUrl = response.url;
      // Update button links
      updateButtonLinks();
    }
  } catch (error) {
    console.error('Failed to load backend URL:', error);
    currentBackendUrl = 'http://localhost:4222';
    updateButtonLinks();
  }
}

// Update button links with current backend URL
function updateButtonLinks() {
  const settingsBtn = document.getElementById('settings-btn');
  const dashboardBtn = document.getElementById('dashboard-btn');

  if (settingsBtn) {
    settingsBtn.href = currentBackendUrl + '/';
  }
  if (dashboardBtn) {
    dashboardBtn.href = currentBackendUrl + '/dashboard';
  }
}

// Check backend status
async function checkBackendStatus() {
  const statusBadge = document.getElementById('status-badge');
  const statusDot = document.getElementById('status-dot');
  const statusText = document.getElementById('status-text');

  try {
    const response = await chrome.runtime.sendMessage({
      action: 'testConnection',
      url: currentBackendUrl
    });

    if (response.success) {
      statusBadge.className = 'status-badge online';
      statusDot.className = 'status-dot online';
      statusText.textContent = 'Online';
    } else {
      throw new Error(response.message);
    }
  } catch (error) {
    statusBadge.className = 'status-badge offline';
    statusDot.className = 'status-dot offline';
    statusText.textContent = 'Offline';
    console.error('Backend check failed:', error);
  }
}

// Open settings in new tab
function openSettings(e) {
  e.preventDefault();
  chrome.tabs.create({ url: currentBackendUrl + '/' });
}

// Open dashboard in new tab
function openDashboard(e) {
  e.preventDefault();
  chrome.tabs.create({ url: currentBackendUrl + '/dashboard' });
}

// Open extension options
function openOptions(e) {
  if (e) e.preventDefault();
  chrome.runtime.openOptionsPage();
}
