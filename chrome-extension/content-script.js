// Content script for Presidio Browser Anonymizer

let extensionEnabled = true;

// Load extension state on initialization
async function loadExtensionState() {
  try {
    const result = await chrome.storage.local.get(['extensionEnabled']);
    extensionEnabled = result.extensionEnabled !== false; // Default to true
    console.log('[Presidio] Extension state loaded:', extensionEnabled);
  } catch (error) {
    console.error('[Presidio] Failed to load extension state:', error);
    extensionEnabled = true;
  }
}

// Initialize - wait for state to load
(async () => {
  await loadExtensionState();
  console.log('[Presidio] Content script initialized. Auto-anonymization:', extensionEnabled ? 'ENABLED' : 'DISABLED');
})();

// Listen for storage changes
chrome.storage.onChanged.addListener((changes, namespace) => {
  if (namespace === 'local' && changes.extensionEnabled) {
    extensionEnabled = changes.extensionEnabled.newValue;
    console.log('[Presidio] Extension state changed:', extensionEnabled ? 'ENABLED' : 'DISABLED');

    if (extensionEnabled) {
      showNotification('✅ Auto-anonimizacja WŁĄCZONA', 'success');
    } else {
      showNotification('⛔ Auto-anonimizacja WYŁĄCZONA', 'info');
    }
  }
});

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
  // Skip if extension is disabled
  if (!extensionEnabled) {
    console.log('[Presidio] Paste event - extension DISABLED, skipping');
    return;
  }

  console.log('[Presidio] Paste event detected - extension ENABLED');
  console.log('[Presidio] Active element:', document.activeElement?.tagName, document.activeElement?.className);

  // Get pasted text from clipboard
  const pastedText = e.clipboardData.getData('text/plain');

  if (!pastedText || pastedText.length === 0) {
    console.log('[Presidio] No text in clipboard, skipping');
    return;
  }

  console.log('[Presidio] Clipboard text length:', pastedText.length);

  // CRITICAL: Prevent default AND stop propagation
  e.preventDefault();
  e.stopPropagation();
  e.stopImmediatePropagation();

  try {
    console.log('[Presidio] Sending anonymization request...');
    showNotification('Anonimizowanie...', 'info');

    const response = await chrome.runtime.sendMessage({
      action: 'anonymize',
      text: pastedText
    });

    console.log('[Presidio] Anonymization response:', response.success);

    if (response.success) {
      const anonymizedText = response.data.anonymized_text;
      const activeElement = document.activeElement;

      console.log('[Presidio] Inserting anonymized text into:', activeElement?.tagName);

      // METHOD 1: TEXTAREA or INPUT
      if (activeElement && (activeElement.tagName === 'TEXTAREA' || activeElement.tagName === 'INPUT')) {
        const start = activeElement.selectionStart || 0;
        const end = activeElement.selectionEnd || 0;
        const before = activeElement.value.substring(0, start);
        const after = activeElement.value.substring(end);

        // Replace content
        activeElement.value = before + anonymizedText + after;

        // Set cursor position
        const newPos = start + anonymizedText.length;
        activeElement.selectionStart = activeElement.selectionEnd = newPos;

        // Trigger events for React/Vue
        activeElement.dispatchEvent(new Event('input', { bubbles: true }));
        activeElement.dispatchEvent(new Event('change', { bubbles: true }));

        console.log('[Presidio] Text inserted into textarea/input');
      }
      // METHOD 2: ContentEditable (ChatGPT, Claude, Gmail)
      else if (activeElement && (activeElement.isContentEditable || activeElement.contentEditable === 'true')) {
        // Use execCommand for better compatibility
        const success = document.execCommand('insertText', false, anonymizedText);

        if (!success) {
          // Fallback: manual insertion
          const selection = window.getSelection();
          if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            range.deleteContents();
            const textNode = document.createTextNode(anonymizedText);
            range.insertNode(textNode);

            // Move cursor to end
            range.setStartAfter(textNode);
            range.setEndAfter(textNode);
            selection.removeAllRanges();
            selection.addRange(range);
          }
        }

        // Trigger input event
        activeElement.dispatchEvent(new InputEvent('input', {
          bubbles: true,
          cancelable: true,
          inputType: 'insertText',
          data: anonymizedText
        }));

        console.log('[Presidio] Text inserted into contentEditable');
      }
      // METHOD 3: Shadow DOM or other (Perplexity?)
      else {
        console.log('[Presidio] Unknown element type, trying selection-based insertion');

        const selection = window.getSelection();
        if (selection && selection.rangeCount > 0) {
          const range = selection.getRangeAt(0);
          range.deleteContents();
          const textNode = document.createTextNode(anonymizedText);
          range.insertNode(textNode);

          // Move cursor
          range.setStartAfter(textNode);
          range.setEndAfter(textNode);
          selection.removeAllRanges();
          selection.addRange(range);
        } else {
          console.error('[Presidio] No selection range available');
        }
      }

      showNotification('✅ Tekst zanonimizowany!', 'success');
    } else {
      throw new Error(response.error);
    }
  } catch (error) {
    console.error('[Presidio] Paste anonymization failed:', error);
    showNotification('❌ Błąd anonimizacji. Wklejam oryginalny.', 'error');

    // Fallback: paste original text
    const activeElement = document.activeElement;
    if (activeElement && (activeElement.tagName === 'TEXTAREA' || activeElement.tagName === 'INPUT')) {
      const start = activeElement.selectionStart || 0;
      const end = activeElement.selectionEnd || 0;
      const before = activeElement.value.substring(0, start);
      const after = activeElement.value.substring(end);
      activeElement.value = before + pastedText + after;
      activeElement.selectionStart = activeElement.selectionEnd = start + pastedText.length;
      activeElement.dispatchEvent(new Event('input', { bubbles: true }));
    } else if (activeElement && (activeElement.isContentEditable || activeElement.contentEditable === 'true')) {
      document.execCommand('insertText', false, pastedText);
    }
  }
}, true);

// =============================================================================
// AUTO-ANONYMIZE BEFORE SEND (ChatGPT, Gmail, Forms)
// =============================================================================

// Track which textareas we're monitoring
const monitoredTextareas = new WeakSet();

// Function to anonymize textarea content before submission
async function anonymizeBeforeSend(textarea) {
  const text = textarea.value || textarea.textContent || textarea.innerText;

  console.log('[Presidio] anonymizeBeforeSend() called - text length:', text?.length || 0);

  if (!text || text.trim().length === 0) {
    console.log('[Presidio] No text to anonymize, skipping');
    return;
  }

  try {
    console.log('[Presidio] Starting anonymization for text:', text.substring(0, 50) + '...');
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
  // Skip if extension is disabled
  if (!extensionEnabled) {
    return;
  }

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
  // Skip if extension is disabled
  if (!extensionEnabled) {
    return;
  }

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
  // Skip if extension is disabled
  if (!extensionEnabled) {
    return;
  }

  // Enter without Shift (send message in most chat apps)
  // NOTE: This is disabled because it's unreliable for ChatGPT/Claude/Perplexity
  // Use PASTE (Ctrl+V) or BUTTON CLICK instead - they work much better!
  //
  // if (e.key === 'Enter' && !e.shiftKey) {
  //   console.log('[Presidio] Enter key pressed (no Shift)');
  //   const target = e.target;
  //
  //   // Only process if it's a textarea or contenteditable
  //   if (target.tagName === 'TEXTAREA' || target.isContentEditable || target.contentEditable === 'true') {
  //     console.log('[Presidio] Enter pressed in input field, anonymizing before send...');
  //
  //     // Prevent default send
  //     e.preventDefault();
  //     e.stopPropagation();
  //
  //     // Anonymize content
  //     await anonymizeBeforeSend(target);
  //
  //     // Trigger Enter again after anonymization
  //     setTimeout(() => {
  //       const enterEvent = new KeyboardEvent('keydown', {
  //         key: 'Enter',
  //         code: 'Enter',
  //         keyCode: 13,
  //         which: 13,
  //         bubbles: true,
  //         cancelable: true
  //       });
  //       target.dispatchEvent(enterEvent);
  //     }, 100);
  //   }
  // }
}, true);
