/**
 * Presidio Browser Anonymizer - Background Service Worker
 * Handles API communication with localhost:4222
 */

const API_BASE_URL = 'http://127.0.0.1:4222/api';

chrome.runtime.onInstalled.addListener(async () => {
  console.log('[Presidio] Extension installed');

  // Set default settings
  await chrome.storage.local.set({
    enabled: true,
    showHighlights: true
  });
});

chrome.runtime.onStartup.addListener(() => {
  console.log('[Presidio] Extension started');
});

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

});

/**
 * Anonymize text via API
 */
async function anonymizeText(text) {
  const response = await fetch(`${API_BASE_URL}/anonymize`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
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

// Initialize service worker
console.log('[Presidio] Service worker loaded');
