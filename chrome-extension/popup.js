// Popup script for Presidio Browser Anonymizer

let currentBackendUrl = '';

// Initialize popup
document.addEventListener('DOMContentLoaded', async () => {
  await loadBackendUrl();
  await checkBackendStatus();

  // Add event listeners for buttons
  document.getElementById('settings-btn')?.addEventListener('click', openSettings);
  document.getElementById('dashboard-btn')?.addEventListener('click', openDashboard);
  document.getElementById('setup-btn')?.addEventListener('click', openSetup);
  document.getElementById('options-btn')?.addEventListener('click', openOptions);

  // Auto-refresh status every 5 seconds
  setInterval(checkBackendStatus, 5000);
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
  const offlineWarning = document.getElementById('offline-warning');
  const setupBtn = document.getElementById('setup-btn');
  const settingsBtn = document.getElementById('settings-btn');
  const dashboardBtn = document.getElementById('dashboard-btn');

  try {
    const response = await chrome.runtime.sendMessage({
      action: 'testConnection',
      url: currentBackendUrl
    });

    if (response.success) {
      // Backend is online
      statusBadge.className = 'status-badge online';
      statusDot.className = 'status-dot online';
      statusText.textContent = 'Online';

      // Hide offline warning and setup button
      offlineWarning?.classList.add('hidden');
      setupBtn?.classList.add('hidden');

      // Show normal buttons
      settingsBtn?.classList.remove('hidden');
      dashboardBtn?.classList.remove('hidden');
    } else {
      throw new Error(response.message);
    }
  } catch (error) {
    // Backend is offline
    statusBadge.className = 'status-badge offline';
    statusDot.className = 'status-dot offline';
    statusText.textContent = 'Offline';

    // Show offline warning and setup button
    offlineWarning?.classList.remove('hidden');
    setupBtn?.classList.remove('hidden');

    // Keep normal buttons visible
    // (user might want to manually start backend)

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

// Open setup wizard in new tab
function openSetup(e) {
  e.preventDefault();
  chrome.tabs.create({ url: currentBackendUrl + '/setup' });
}

// Open extension options
function openOptions(e) {
  if (e) e.preventDefault();
  chrome.runtime.openOptionsPage();
}
