/**
 * Presidio Browser Anonymizer - Background Service Worker
 * Handles API communication with localhost:4222
 */

const API_BASE_URL = 'http://127.0.0.1:4222/api';

// Auto-load API token from backend
let API_TOKEN = null;

chrome.runtime.onInstalled.addListener(async () => {
  console.log('[Presidio] Extension installed');

  // Auto-fetch token from backend
  await autoLoadToken();

  // Set default settings
  await chrome.storage.local.set({
    enabled: true,
    showHighlights: true
  });
});

// Auto-load token from backend on startup
chrome.runtime.onStartup.addListener(async () => {
  console.log('[Presidio] Extension started');
  await autoLoadToken();
});

// Auto-load token function
async function autoLoadToken() {
  // First, try to load from storage (cached)
  const stored = await chrome.storage.local.get(['apiToken']);
  if (stored.apiToken) {
    API_TOKEN = stored.apiToken;
    console.log('[Presidio] Token loaded from cache ✓');
    return;
  }

  // If not cached, fetch from backend
  try {
    const response = await fetch('http://127.0.0.1:4222/api/token');
    if (response.ok) {
      const data = await response.json();
      API_TOKEN = data.token;
      await chrome.storage.local.set({ apiToken: API_TOKEN });
      console.log('[Presidio] Token auto-loaded from backend ✓');
    } else {
      console.warn('[Presidio] Could not auto-load token. Backend may not be running.');
    }
  } catch (error) {
    console.warn('[Presidio] Backend not available. Start backend to enable anonymization.');
  }
}

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'anonymize') {
    anonymizeText(message.text)
      .then(result => sendResponse({ success: true, data: result }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Keep channel open for async response
  }

  if (message.action === 'checkHealth') {
    checkHealth()
      .then(result => sendResponse({ success: true, data: result }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }

  if (message.action === 'setToken') {
    API_TOKEN = message.token;
    chrome.storage.local.set({ apiToken: message.token });
    sendResponse({ success: true });
    return true;
  }
});

/**
 * Anonymize text via API
 */
async function anonymizeText(text) {
  // Auto-load token if not available
  if (!API_TOKEN) {
    console.log('[Presidio] Token not loaded, attempting auto-load...');
    await autoLoadToken();

    // If still no token, throw error
    if (!API_TOKEN) {
      throw new Error('Backend not running. Please start backend: cd backend && source .venv/bin/activate && python app.py');
    }
  }

  const response = await fetch(`${API_BASE_URL}/anonymize`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Presidio-Token': API_TOKEN
    },
    body: JSON.stringify({ text })
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Anonymization failed');
  }

  return await response.json();
}

/**
 * Check API health
 */
async function checkHealth() {
  const response = await fetch(`${API_BASE_URL}/health`);

  if (!response.ok) {
    throw new Error('Health check failed');
  }

  return await response.json();
}

// Initialize token on service worker load
(async function init() {
  console.log('[Presidio] Service worker loaded');
  await autoLoadToken();
})();
