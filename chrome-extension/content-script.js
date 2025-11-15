// Content script for Presidio Browser Anonymizer

// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'replaceSelection') {
    replaceSelectedText(request.anonymizedText);
  }
});

// Replace selected text with anonymized version
function replaceSelectedText(anonymizedText) {
  const selection = window.getSelection();

  if (!selection.rangeCount) return;

  const range = selection.getRangeAt(0);
  range.deleteContents();
  range.insertNode(document.createTextNode(anonymizedText));

  // Clear selection
  selection.removeAllRanges();

  // Show notification
  showNotification('Tekst został zanonimizowany', 'success');
}

// Show notification toast
function showNotification(message, type = 'info') {
  const toast = document.createElement('div');
  toast.textContent = message;
  toast.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: ${type === 'success' ? '#10b981' : '#2563eb'};
    color: white;
    padding: 12px 20px;
    border-radius: 8px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    font-size: 14px;
    font-weight: 500;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    z-index: 999999;
    opacity: 0;
    transition: opacity 0.3s;
  `;

  document.body.appendChild(toast);

  // Fade in
  setTimeout(() => {
    toast.style.opacity = '1';
  }, 10);

  // Fade out and remove
  setTimeout(() => {
    toast.style.opacity = '0';
    setTimeout(() => {
      document.body.removeChild(toast);
    }, 300);
  }, 3000);
}

// Keyboard shortcut: Ctrl+Shift+A to anonymize selected text
document.addEventListener('keydown', async (e) => {
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'A') {
    e.preventDefault();

    const selectedText = window.getSelection().toString().trim();

    if (!selectedText) {
      showNotification('Zaznacz tekst do anonimizacji', 'info');
      return;
    }

    try {
      showNotification('Anonimizowanie...', 'info');

      const response = await chrome.runtime.sendMessage({
        action: 'anonymize',
        text: selectedText
      });

      if (response.success) {
        replaceSelectedText(response.data.anonymized_text);
      } else {
        throw new Error(response.error);
      }
    } catch (error) {
      console.error('Anonymization failed:', error);
      showNotification('Błąd anonimizacji. Sprawdź czy backend działa.', 'error');
    }
  }
});
