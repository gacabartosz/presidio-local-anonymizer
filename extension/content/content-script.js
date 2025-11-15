/**
 * Presidio Browser Anonymizer - Content Script
 * Injected into ChatGPT, Claude AI, Perplexity
 */

console.log('[Presidio] Content script loaded on', window.location.hostname);

let isEnabled = true;
let currentTextarea = null;

// Initialize
(async function init() {
  // Load settings
  const settings = await chrome.storage.local.get(['enabled', 'showHighlights']);
  isEnabled = settings.enabled !== false;

  // Find textarea and attach listeners
  observeTextareas();
})();

/**
 * Observe for textareas (handle dynamic content)
 */
function observeTextareas() {
  const observer = new MutationObserver(() => {
    findAndAttachToTextarea();
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true
  });

  // Initial check
  findAndAttachToTextarea();
}

/**
 * Find main textarea and attach event listeners
 */
function findAndAttachToTextarea() {
  // Selectors for different sites (ordered by specificity)
  const selectors = [
    // ChatGPT (current interface - late 2024)
    '#prompt-textarea',
    'textarea[placeholder*="Message"]',
    'textarea[placeholder*="Send a message"]',

    // ChatGPT (older versions)
    'textarea[data-id="root"]',

    // Claude AI
    'div[contenteditable="true"][data-value]',
    'div[contenteditable="true"]',

    // Perplexity
    'textarea.search-box-input',
    'textarea[placeholder*="Ask anything"]',

    // Generic fallback (main content textarea)
    'main textarea',
    'textarea[role="textbox"]',
    'textarea',
  ];

  for (const selector of selectors) {
    const textarea = document.querySelector(selector);
    if (textarea && textarea !== currentTextarea) {
      console.log('[Presidio] Found textarea:', selector);
      attachToTextarea(textarea);
      currentTextarea = textarea;
      return; // Found and attached
    }
  }

  // If no textarea found, try again later
  if (!currentTextarea) {
    console.log('[Presidio] No textarea found yet, will retry...');
  }
}

/**
 * Attach to textarea
 */
function attachToTextarea(textarea) {
  // Listen for input events
  textarea.addEventListener('input', handleInput);
  textarea.addEventListener('paste', handlePaste);

  console.log('[Presidio] Attached to textarea');
}

/**
 * Handle input event
 */
async function handleInput(event) {
  if (!isEnabled) return;

  const text = event.target.value || event.target.textContent;
  if (!text || text.length < 3) return;

  // Debounce (wait 500ms after user stops typing)
  clearTimeout(window.presidioDebounce);
  window.presidioDebounce = setTimeout(async () => {
    await anonymizeAndReplace(event.target, text);
  }, 500);
}

/**
 * Handle paste event
 */
async function handlePaste(event) {
  if (!isEnabled) return;

  setTimeout(async () => {
    const text = event.target.value || event.target.textContent;
    await anonymizeAndReplace(event.target, text);
  }, 100);
}

/**
 * Anonymize text and replace
 */
async function anonymizeAndReplace(target, text) {
  try {
    // Send to background script
    const response = await chrome.runtime.sendMessage({
      action: 'anonymize',
      text: text
    });

    if (response.success) {
      const { anonymized_text, entities_found } = response.data;

      // Only replace if entities were found
      if (entities_found.length > 0) {
        console.log(`[Presidio] Found ${entities_found.length} entities`);

        // Replace text
        if (target.value !== undefined) {
          target.value = anonymized_text;
        } else {
          target.textContent = anonymized_text;
        }

        // Show notification
        showNotification(`${entities_found.length} dane zanonimizowane`);

        // Highlight (optional)
        highlightEntities(target, entities_found);
      }
    } else {
      console.error('[Presidio] Error:', response.error);
    }
  } catch (error) {
    console.error('[Presidio] Failed to anonymize:', error);
  }
}

/**
 * Show notification
 */
function showNotification(message) {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = 'presidio-notification';
  notification.textContent = message;
  document.body.appendChild(notification);

  // Remove after 3 seconds
  setTimeout(() => {
    notification.remove();
  }, 3000);
}

/**
 * Highlight entities (visual indicator)
 */
function highlightEntities(target, entities) {
  // Add visual indicator class
  target.classList.add('presidio-anonymized');

  // Remove after 2 seconds
  setTimeout(() => {
    target.classList.remove('presidio-anonymized');
  }, 2000);
}

// Listen for settings changes
chrome.storage.onChanged.addListener((changes) => {
  if (changes.enabled) {
    isEnabled = changes.enabled.newValue;
    console.log('[Presidio] Enabled:', isEnabled);
  }
});
