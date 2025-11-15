// Popup script for Presidio Browser Anonymizer
const API_BASE_URL = 'http://localhost:4222/api';

// Check service health on popup open
async function checkHealth() {
  const statusBadge = document.getElementById('status-badge');
  const statusDot = document.getElementById('status-dot');
  const statusText = document.getElementById('status-text');

  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    const data = await response.json();

    if (data.status === 'healthy' || data.status === 'ok') {
      statusBadge.className = 'status-badge online';
      statusDot.className = 'status-dot online';
      statusText.textContent = 'Online';
    } else {
      throw new Error('Service offline');
    }
  } catch (error) {
    statusBadge.className = 'status-badge offline';
    statusDot.className = 'status-dot offline';
    statusText.textContent = 'Offline';
  }
}

// Run health check on load
document.addEventListener('DOMContentLoaded', checkHealth);
