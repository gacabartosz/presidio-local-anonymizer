"""
Security Manager - API token authentication
"""

import secrets
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class SecurityManager:
    """Manage API authentication tokens"""

    def __init__(self):
        """Initialize security manager and load/generate token"""
        self.token_file = Path.home() / '.presidio-browser' / 'token'
        self.token = self._load_or_generate_token()

    def _load_or_generate_token(self):
        """Load existing token or generate new one"""

        # Check if token file exists
        if self.token_file.exists():
            try:
                with open(self.token_file, 'r') as f:
                    token = f.read().strip()
                logger.info(f"Loaded existing token from {self.token_file}")
                return token
            except Exception as e:
                logger.warning(f"Failed to load token: {e}")

        # Generate new token
        token = secrets.token_urlsafe(32)

        # Save token to file
        try:
            self.token_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.token_file, 'w') as f:
                f.write(token)
            # Set file permissions (only owner can read)
            self.token_file.chmod(0o600)
            logger.info(f"Generated new token and saved to {self.token_file}")
        except Exception as e:
            logger.error(f"Failed to save token: {e}")

        return token

    def get_token(self):
        """Get current API token"""
        return self.token

    def verify_token(self, provided_token):
        """Verify provided token matches stored token"""
        return secrets.compare_digest(provided_token, self.token)

    def regenerate_token(self):
        """Generate new token (invalidates old one)"""
        self.token = secrets.token_urlsafe(32)

        try:
            with open(self.token_file, 'w') as f:
                f.write(self.token)
            logger.info("Token regenerated successfully")
            return self.token
        except Exception as e:
            logger.error(f"Failed to save new token: {e}")
            return None
