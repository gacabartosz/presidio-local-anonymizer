// Configuration management for Presidio Browser Anonymizer

const DEFAULT_CONFIG = {
  backendUrl: 'http://localhost:4222',
  autoRetry: true,
  retryAttempts: 3,
  timeout: 30000
};

// Get backend URL from storage or use default
async function getBackendUrl() {
  try {
    const result = await chrome.storage.sync.get(['backendUrl']);
    return result.backendUrl || DEFAULT_CONFIG.backendUrl;
  } catch (error) {
    console.error('Failed to get backend URL:', error);
    return DEFAULT_CONFIG.backendUrl;
  }
}

// Get full config from storage or use defaults
async function getConfig() {
  try {
    const result = await chrome.storage.sync.get(Object.keys(DEFAULT_CONFIG));
    return { ...DEFAULT_CONFIG, ...result };
  } catch (error) {
    console.error('Failed to get config:', error);
    return DEFAULT_CONFIG;
  }
}

// Save config to storage
async function saveConfig(config) {
  try {
    await chrome.storage.sync.set(config);
    return true;
  } catch (error) {
    console.error('Failed to save config:', error);
    return false;
  }
}

// Test backend connection
async function testBackendConnection(url) {
  try {
    const response = await fetch(`${url}/api/health`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' }
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    return {
      success: true,
      status: data.status || 'unknown',
      message: 'Backend połączony'
    };
  } catch (error) {
    return {
      success: false,
      status: 'offline',
      message: error.message
    };
  }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { getBackendUrl, getConfig, saveConfig, testBackendConnection, DEFAULT_CONFIG };
}
