"""
Anonymization endpoint - core functionality
"""

from flask import Blueprint, jsonify, request
import logging
from core.analyzer import build_analyzer
from core.anonymizer import anonymize_text

logger = logging.getLogger(__name__)
anonymize_bp = Blueprint('anonymize', __name__)

# Initialize analyzer once at startup (expensive operation)
try:
    analyzer, config = build_analyzer()
    logger.info("Presidio Analyzer initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Presidio Analyzer: {e}")
    analyzer = None
    config = None

@anonymize_bp.route('/anonymize', methods=['POST'])
def anonymize():
    """
    Anonymize text endpoint

    Request JSON:
        {
            "text": "Jan Kowalski, PESEL: 92010212345",
            "entities": ["PERSON", "PL_PESEL"]  # Optional, default: all
        }

    Response JSON:
        {
            "original_text": "Jan Kowalski, PESEL: 92010212345",
            "anonymized_text": "[OSOBA], PESEL: [PESEL]",
            "entities_found": [
                {
                    "type": "PERSON",
                    "start": 0,
                    "end": 13,
                    "score": 0.95,
                    "text": "Jan Kowalski"
                },
                {
                    "type": "PL_PESEL",
                    "start": 22,
                    "end": 33,
                    "score": 0.9,
                    "text": "92010212345"
                }
            ],
            "stats": {
                "total_entities": 2,
                "processing_time_ms": 45
            }
        }
    """

    # Check if analyzer is initialized
    if analyzer is None or config is None:
        return jsonify({
            'error': 'Service not ready',
            'message': 'Presidio Analyzer failed to initialize'
        }), 503

    # Get request data
    data = request.get_json()

    if not data or 'text' not in data:
        return jsonify({
            'error': 'Invalid request',
            'message': 'Missing "text" field in request body'
        }), 400

    text = data.get('text', '')
    entities_filter = data.get('entities', None)  # Optional filter

    # Validate text
    if not text or not text.strip():
        return jsonify({
            'error': 'Invalid request',
            'message': 'Text cannot be empty'
        }), 400

    try:
        import time
        start_time = time.time()

        # Analyze text for PII
        results = analyzer.analyze(
            text=text,
            language='pl',
            entities=entities_filter  # If None, detects all entities
        )

        # Anonymize text
        anonymized_text = anonymize_text(text, results, config)

        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)  # milliseconds

        # Build response with detailed entity information
        entities_found = []
        for result in results:
            entity_info = {
                'type': result.entity_type,
                'start': result.start,
                'end': result.end,
                'score': round(result.score, 2),
                'text': text[result.start:result.end]
            }
            entities_found.append(entity_info)

        response = {
            'original_text': text,
            'anonymized_text': anonymized_text,
            'entities_found': entities_found,
            'stats': {
                'total_entities': len(results),
                'processing_time_ms': processing_time
            }
        }

        logger.info(f"Anonymized text: {len(results)} entities found, {processing_time}ms")

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error during anonymization: {e}", exc_info=True)
        return jsonify({
            'error': 'Anonymization failed',
            'message': str(e)
        }), 500
