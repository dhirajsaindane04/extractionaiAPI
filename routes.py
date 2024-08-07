from flask import Blueprint, request, jsonify
import logging
from gemini_client import get_gemini_response
from image_processor import input_image_setup

logger = logging.getLogger(__name__)
bp = Blueprint('main', __name__)

@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        image_data = input_image_setup(file)
        response = get_gemini_response("Extract invoice data", image_data)
        return jsonify(response)
    except FileNotFoundError as e:
        logger.error(f"File Error: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"Unexpected Error: {e}")
        return jsonify({'error': 'Internal Server Error'}), 500
