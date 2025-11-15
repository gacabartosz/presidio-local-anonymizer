#!/usr/bin/env python3
"""
Presidio Browser Anonymizer - Backend API Server
Localhost service for real-time text anonymization in browser

Author: Bartosz Gaca
License: MIT
"""

import os
import sys
import logging
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add backend directory to path for imports
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from api.health import health_bp
from api.anonymize import anonymize_bp
from api.config import config_bp
from api.setup import setup_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='../web-ui', static_url_path='')
app.config['JSON_AS_ASCII'] = False  # Support for Polish characters

# CORS configuration - allow only localhost and browser extension
CORS(app, resources={
    r"/*": {
        "origins": [
            "http://localhost:*",
            "http://127.0.0.1:*",
            "chrome-extension://*",
            "moz-extension://*"
        ]
    }
})

# No authentication needed - backend runs only on localhost

# Register blueprints
app.register_blueprint(health_bp, url_prefix='/api')
app.register_blueprint(anonymize_bp, url_prefix='/api')
app.register_blueprint(config_bp, url_prefix='/api')
app.register_blueprint(setup_bp, url_prefix='/api/setup')

# Root endpoint - serve main app
@app.route('/')
@app.route('/dashboard')
@app.route('/setup')
def index():
    """Serve main application - single page app"""
    from flask import send_from_directory
    return send_from_directory('../web-ui', 'app.html')

# No token endpoint needed - no authentication required

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not found',
        'message': 'The requested endpoint does not exist'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

def main():
    """Start the Flask server"""

    # Display startup information
    logger.info("=" * 60)
    logger.info("Presidio Browser Anonymizer - Backend Service")
    logger.info("=" * 60)
    logger.info("🌐 Backend URL: http://127.0.0.1:4222")
    logger.info("🔧 Settings: http://127.0.0.1:4222")
    logger.info("📊 Dashboard: http://127.0.0.1:4222/dashboard")
    logger.info("=" * 60)

    # Start server
    app.run(
        host='127.0.0.1',  # Localhost only for security
        port=4222,
        debug=False,  # Disable in production
        threaded=True  # Handle multiple requests
    )

if __name__ == '__main__':
    main()
