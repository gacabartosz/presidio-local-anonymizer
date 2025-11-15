// Background service worker for Presidio Browser Anonymizer
// Import config functions
importScripts('config.js');

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'anonymize') {
    anonymizeText(request.text)
      .then(result => sendResponse({ success: true, data: result }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Keep the message channel open for async response
  }

  if (request.action === 'getBackendUrl') {
    getBackendUrl()
      .then(url => sendResponse({ success: true, url }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true;
  }

  if (request.action === 'testConnection') {
    testBackendConnection(request.url)
      .then(result => sendResponse(result))
      .catch(error => sendResponse({ success: false, message: error.message }));
    return true;
  }
});

// Anonymize text using the API
async function anonymizeText(text) {
  try {
    const backendUrl = await getBackendUrl();
    console.log('[Presidio Background] Backend URL:', backendUrl);
    console.log('[Presidio Background] Sending request to:', `${backendUrl}/api/anonymize`);
    console.log('[Presidio Background] Text to anonymize:', text.substring(0, 50));

    const response = await fetch(`${backendUrl}/api/anonymize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });

    console.log('[Presidio Background] Response status:', response.status);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: Anonymization failed`);
    }

    const data = await response.json();
    console.log('[Presidio Background] Anonymization successful:', data.anonymized_text?.substring(0, 50));
    return data;
  } catch (error) {
    console.error('[Presidio Background] Anonymization error:', error);
    throw error;
  }
}

// Context menu for anonymizing selected text
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'anonymize-selection',
    title: 'Anonimizuj zaznaczony tekst',
    contexts: ['selection']
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'anonymize-selection') {
    const selectedText = info.selectionText;

    anonymizeText(selectedText)
      .then(result => {
        // Send result to content script to replace text
        chrome.tabs.sendMessage(tab.id, {
          action: 'replaceSelection',
          anonymizedText: result.anonymized_text
        });
      })
      .catch(error => {
        console.error('Failed to anonymize:', error);
      });
  }
});
