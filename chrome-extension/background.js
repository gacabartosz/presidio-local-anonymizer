// Background service worker for Presidio Browser Anonymizer

const API_BASE_URL = 'http://localhost:4222/api';

// Listen for messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'anonymize') {
    anonymizeText(request.text)
      .then(result => sendResponse({ success: true, data: result }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Keep the message channel open for async response
  }
});

// Anonymize text using the API
async function anonymizeText(text) {
  try {
    const response = await fetch(`${API_BASE_URL}/anonymize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });

    if (!response.ok) {
      throw new Error('Anonymization failed');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Anonymization error:', error);
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
