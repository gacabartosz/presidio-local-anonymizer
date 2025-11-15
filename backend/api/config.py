"""
Configuration endpoint - manage anonymization settings
"""

from flask import Blueprint, jsonify, request
import logging
import yaml
from pathlib import Path

logger = logging.getLogger(__name__)
config_bp = Blueprint('config', __name__)

# Path to config file
CONFIG_PATH = Path(__file__).parent.parent / 'config' / 'entities.yaml'

@config_bp.route('/config', methods=['GET'])
def get_config():
    """
    Get current configuration

    Response JSON:
        {
            "language": "pl",
            "threshold": 0.35,
            "entities": {...}
        }
    """
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        return jsonify(config), 200

    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return jsonify({
            'error': 'Failed to load configuration',
            'message': str(e)
        }), 500

@config_bp.route('/config', methods=['POST'])
def update_config():
    """
    Update configuration

    Request JSON:
        {
            "threshold": 0.5,
            "entities": {...}
        }

    Response JSON:
        {
            "status": "success",
            "message": "Configuration updated"
        }
    """
    try:
        # Get new config from request
        new_config = request.get_json()

        if not new_config:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Missing configuration data'
            }), 400

        # Load current config
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            current_config = yaml.safe_load(f)

        # Update config (merge)
        if 'threshold' in new_config:
            current_config['threshold'] = new_config['threshold']

        if 'entities' in new_config:
            current_config['entities'].update(new_config['entities'])

        # Save updated config
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            yaml.dump(current_config, f, allow_unicode=True, default_flow_style=False)

        logger.info("Configuration updated successfully")

        return jsonify({
            'status': 'success',
            'message': 'Configuration updated',
            'config': current_config
        }), 200

    except Exception as e:
        logger.error(f"Error updating config: {e}")
        return jsonify({
            'error': 'Failed to update configuration',
            'message': str(e)
        }), 500
