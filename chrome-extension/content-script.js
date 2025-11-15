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

// Auto-anonymize on paste (Ctrl+V)
document.addEventListener('paste', async (e) => {
  // Get pasted text from clipboard
  const pastedText = e.clipboardData.getData('text/plain');

  if (!pastedText || pastedText.length === 0) {
    return;
  }

  // Prevent default paste behavior
  e.preventDefault();

  try {
    showNotification('Anonimizowanie wklejonego tekstu...', 'info');

    const response = await chrome.runtime.sendMessage({
      action: 'anonymize',
      text: pastedText
    });

    if (response.success) {
      // Insert anonymized text at cursor position
      const activeElement = document.activeElement;

      if (activeElement && (activeElement.tagName === 'TEXTAREA' || activeElement.tagName === 'INPUT')) {
        // For input/textarea elements
        const start = activeElement.selectionStart;
        const end = activeElement.selectionEnd;
        const before = activeElement.value.substring(0, start);
        const after = activeElement.value.substring(end);

        activeElement.value = before + response.data.anonymized_text + after;
        activeElement.selectionStart = activeElement.selectionEnd = start + response.data.anonymized_text.length;

        // Trigger input event for frameworks like React
        activeElement.dispatchEvent(new Event('input', { bubbles: true }));
      } else if (activeElement && activeElement.isContentEditable) {
        // For contenteditable elements (like ChatGPT)
        document.execCommand('insertText', false, response.data.anonymized_text);
      } else {
        // Fallback: just insert at selection
        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
          const range = selection.getRangeAt(0);
          range.deleteContents();
          range.insertNode(document.createTextNode(response.data.anonymized_text));
        }
      }

      showNotification('Tekst zanonimizowany przy wklejaniu!', 'success');
    } else {
      throw new Error(response.error);
    }
  } catch (error) {
    console.error('Paste anonymization failed:', error);
    showNotification('Błąd anonimizacji. Wklejam oryginalny tekst.', 'error');

    // Fallback: paste original text
    const activeElement = document.activeElement;
    if (activeElement && (activeElement.tagName === 'TEXTAREA' || activeElement.tagName === 'INPUT')) {
      const start = activeElement.selectionStart;
      const end = activeElement.selectionEnd;
      const before = activeElement.value.substring(0, start);
      const after = activeElement.value.substring(end);
      activeElement.value = before + pastedText + after;
      activeElement.selectionStart = activeElement.selectionEnd = start + pastedText.length;
    } else if (activeElement && activeElement.isContentEditable) {
      document.execCommand('insertText', false, pastedText);
    }
  }
});

// =============================================================================
// AUTO-ANONYMIZE BEFORE SEND (ChatGPT, Gmail, Forms)
// =============================================================================

// Track which textareas we're monitoring
const monitoredTextareas = new WeakSet();

// Function to anonymize textarea content before submission
async function anonymizeBeforeSend(textarea) {
  const text = textarea.value || textarea.textContent || textarea.innerText;

  if (!text || text.trim().length === 0) {
    return;
  }

  try {
    console.log('[Presidio] Anonymizing before send...');
    showNotification('Anonimizowanie przed wysłaniem...', 'info');

    const response = await chrome.runtime.sendMessage({
      action: 'anonymize',
      text: text
    });

    if (response.success) {
      // Replace textarea content with anonymized version
      if (textarea.tagName === 'TEXTAREA' || textarea.tagName === 'INPUT') {
        textarea.value = response.data.anonymized_text;
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
      } else if (textarea.isContentEditable || textarea.contentEditable === 'true') {
        textarea.textContent = response.data.anonymized_text;
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
      }

      console.log('[Presidio] Text anonymized before send!');
      showNotification('✅ Tekst zanonimizowany przed wysłaniem!', 'success');

      // Flash green border
      textarea.style.transition = 'border-color 0.3s';
      textarea.style.borderColor = '#10b981';
      setTimeout(() => {
        textarea.style.borderColor = '';
      }, 1000);
    } else {
      throw new Error(response.error);
    }
  } catch (error) {
    console.error('[Presidio] Anonymization before send failed:', error);
    showNotification('⚠️ Błąd anonimizacji - wysyłam oryginalny tekst', 'error');
  }
}

// Monitor form submissions
document.addEventListener('submit', async (e) => {
  console.log('[Presidio] Form submit detected');

  // Find textarea/input in the form
  const form = e.target;
  const textareas = form.querySelectorAll('textarea, input[type="text"], [contenteditable="true"]');

  if (textareas.length > 0) {
    // Prevent form submission temporarily
    e.preventDefault();
    e.stopPropagation();

    // Anonymize all textareas
    for (const textarea of textareas) {
      await anonymizeBeforeSend(textarea);
    }

    // Submit form after anonymization
    setTimeout(() => {
      form.submit();
    }, 100);
  }
}, true);

// Monitor button clicks (ChatGPT, Claude, etc.)
document.addEventListener('click', async (e) => {
  const button = e.target.closest('button');

  if (!button) return;

  // Check if this is a "Send" button (ChatGPT, Claude, etc.)
  const buttonText = button.textContent.toLowerCase();
  const isSendButton =
    buttonText.includes('send') ||
    buttonText.includes('wyślij') ||
    buttonText.includes('submit') ||
    button.type === 'submit' ||
    button.getAttribute('data-testid')?.includes('send') ||
    button.className.includes('send');

  if (!isSendButton) return;

  console.log('[Presidio] Send button clicked, searching for textarea...');

  // Find nearby textarea or contenteditable
  const parent = button.closest('form') || button.closest('div');
  if (!parent) return;

  const textarea =
    parent.querySelector('textarea') ||
    parent.querySelector('[contenteditable="true"]') ||
    parent.querySelector('input[type="text"]') ||
    document.querySelector('textarea:focus') ||
    document.querySelector('[contenteditable="true"]:focus');

  if (textarea) {
    console.log('[Presidio] Found textarea, anonymizing...');

    // Prevent button click temporarily
    e.preventDefault();
    e.stopPropagation();

    // Anonymize content
    await anonymizeBeforeSend(textarea);

    // Click button after anonymization
    setTimeout(() => {
      button.click();
    }, 100);
  }
}, true);

// Monitor Enter key press (common way to send messages)
document.addEventListener('keydown', async (e) => {
  // Enter without Shift (send message in most chat apps)
  if (e.key === 'Enter' && !e.shiftKey) {
    const target = e.target;

    // Only process if it's a textarea or contenteditable
    if (target.tagName === 'TEXTAREA' || target.isContentEditable || target.contentEditable === 'true') {
      // Check if Enter sends (no Shift) - common in ChatGPT, Claude
      const parent = target.closest('form');

      if (parent) {
        console.log('[Presidio] Enter pressed, anonymizing before send...');

        // Prevent default send
        e.preventDefault();
        e.stopPropagation();

        // Anonymize content
        await anonymizeBeforeSend(target);

        // Trigger Enter again after anonymization
        setTimeout(() => {
          const enterEvent = new KeyboardEvent('keydown', {
            key: 'Enter',
            code: 'Enter',
            keyCode: 13,
            which: 13,
            bubbles: true,
            cancelable: true
          });
          target.dispatchEvent(enterEvent);
        }, 100);
      }
    }
  }
}, true);
