"""
Health check endpoint
"""

from flask import Blueprint, jsonify
import logging

logger = logging.getLogger(__name__)
health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint - verify service is running

    Returns:
        JSON with service status
    """
    return jsonify({
        'status': 'healthy',
        'service': 'presidio-browser-anonymizer',
        'version': '1.0.0'
    }), 200
