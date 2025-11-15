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
from storage.security import SecurityManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Support for Polish characters

# CORS configuration - allow only localhost and browser extension
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:*",
            "chrome-extension://*",
            "moz-extension://*"
        ]
    }
})

# Initialize security manager
security_manager = SecurityManager()

# Security middleware - check API token
@app.before_request
def verify_token():
    """Verify API token for all requests except /health"""

    # Skip token verification for health check
    if request.path == '/api/health':
        return None

    # Get token from header
    token = request.headers.get('X-Presidio-Token')

    if not token:
        logger.warning(f"Missing token in request to {request.path}")
        return jsonify({
            'error': 'Missing authentication token',
            'message': 'Include X-Presidio-Token header'
        }), 401

    if not security_manager.verify_token(token):
        logger.warning(f"Invalid token attempt for {request.path}")
        return jsonify({
            'error': 'Invalid authentication token',
            'message': 'Token is not valid'
        }), 403

    return None

# Register blueprints
app.register_blueprint(health_bp, url_prefix='/api')
app.register_blueprint(anonymize_bp, url_prefix='/api')
app.register_blueprint(config_bp, url_prefix='/api')

# Root endpoint
@app.route('/')
def index():
    """Root endpoint - service information"""
    return jsonify({
        'service': 'Presidio Browser Anonymizer',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'health': '/api/health',
            'anonymize': '/api/anonymize',
            'config': '/api/config'
        },
        'documentation': '/api/docs'
    })

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
    logger.info(f"Security token: {security_manager.get_token()}")
    logger.info("Copy this token to browser extension settings")
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
