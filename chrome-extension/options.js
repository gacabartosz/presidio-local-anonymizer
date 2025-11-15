// Options page script

const backendUrlInput = document.getElementById('backend-url');
const testBtn = document.getElementById('test-btn');
const saveBtn = document.getElementById('save-btn');
const resetBtn = document.getElementById('reset-btn');
const statusMessage = document.getElementById('status-message');

// Load saved configuration
document.addEventListener('DOMContentLoaded', async () => {
  await loadConfig();

  testBtn.addEventListener('click', testConnection);
  saveBtn.addEventListener('click', saveConfig);
  resetBtn.addEventListener('click', resetConfig);
});

// Load config from storage
async function loadConfig() {
  try {
    const result = await chrome.storage.sync.get(['backendUrl']);
    if (result.backendUrl) {
      backendUrlInput.value = result.backendUrl;
    }
  } catch (error) {
    showStatus('Błąd wczytywania konfiguracji: ' + error.message, 'error');
  }
}

// Test backend connection
async function testConnection() {
  const url = backendUrlInput.value.trim();

  if (!url) {
    showStatus('Wprowadź URL backendu', 'error');
    return;
  }

  testBtn.disabled = true;
  testBtn.textContent = '⏳ Testowanie...';

  try {
    const response = await chrome.runtime.sendMessage({
      action: 'testConnection',
      url: url
    });

    if (response.success) {
      showStatus(`✅ Połączenie udane! Status: ${response.status}`, 'success');
    } else {
      showStatus(`❌ Połączenie nieudane: ${response.message}`, 'error');
    }
  } catch (error) {
    showStatus('❌ Błąd testowania: ' + error.message, 'error');
  } finally {
    testBtn.disabled = false;
    testBtn.textContent = '🔍 Testuj Połączenie';
  }
}

// Save configuration
async function saveConfig() {
  const url = backendUrlInput.value.trim();

  if (!url) {
    showStatus('Wprowadź URL backendu', 'error');
    return;
  }

  // Validate URL format
  try {
    new URL(url);
  } catch (error) {
    showStatus('Nieprawidłowy format URL', 'error');
    return;
  }

  saveBtn.disabled = true;
  saveBtn.textContent = '⏳ Zapisywanie...';

  try {
    await chrome.storage.sync.set({ backendUrl: url });
    showStatus('✅ Konfiguracja zapisana pomyślnie!', 'success');
  } catch (error) {
    showStatus('❌ Błąd zapisu: ' + error.message, 'error');
  } finally {
    saveBtn.disabled = false;
    saveBtn.textContent = '💾 Zapisz';
  }
}

// Reset to defaults
async function resetConfig() {
  backendUrlInput.value = 'http://localhost:4222';
  
  try {
    await chrome.storage.sync.set({ backendUrl: 'http://localhost:4222' });
    showStatus('✅ Przywrócono ustawienia domyślne', 'success');
  } catch (error) {
    showStatus('❌ Błąd resetowania: ' + error.message, 'error');
  }
}

// Show status message
function showStatus(message, type) {
  statusMessage.textContent = message;
  statusMessage.className = `status-box ${type}`;
  statusMessage.classList.remove('hidden');

  if (type === 'success') {
    setTimeout(() => {
      statusMessage.classList.add('hidden');
    }, 5000);
  }
}
