from flask import jsonify, request, send_file
import logging
import os
from typing import Tuple, Union
from ..services.llm_service import LLMService
from ..services.presentation_generator import PresentationGenerator
from ..models.presentation import Presentation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PresentationController:
    def __init__(self):
        self.llm_service = LLMService()
        self.presentation_generator = PresentationGenerator()

    def generate_presentation(self) -> Tuple[dict, int]:
        """Handle presentation generation request."""
        try:
            # Validate request
            data = request.json
            if not data or 'topic' not in data:
                return jsonify({'error': 'Topic is required'}), 400

            topic = data['topic']
            logger.info(f"Generating presentation for topic: {topic}")

            # Generate content using LLM
            content_data = self.llm_service.generate_presentation_content(topic)
            if not content_data:
                return jsonify({
                    'error': 'Failed to generate presentation content. Please check if LMStudio is running at http://127.0.0.1:1234/v1'
                }), 500

            # Create presentation model
            try:
                presentation = Presentation.from_dict(content_data)
            except ValueError as e:
                logger.error(f"Invalid presentation data: {e}")
                return jsonify({'error': f'Invalid presentation structure: {str(e)}'}), 500

            # Generate PowerPoint file
            filename = self.presentation_generator.generate(presentation)
            if not filename:
                return jsonify({'error': 'Failed to generate PowerPoint file'}), 500

            # Return preview data
            return jsonify({
                'title': presentation.title,
                'subtitle': presentation.subtitle,
                'slides': [vars(slide) for slide in presentation.slides],
                'filename': filename
            }), 200

        except Exception as e:
            logger.error(f"Error in generate_presentation: {e}")
            return jsonify({'error': f'Internal server error: {str(e)}'}), 500

    def download_presentation(self, filename: str) -> Union[Tuple[dict, int], object]:
        """Handle presentation download request."""
        try:
            filepath = os.path.join(os.getcwd(), 'presentations', filename)
            if not os.path.exists(filepath):
                logger.error(f"Presentation file not found: {filepath}")
                return jsonify({'error': 'File not found'}), 404
            return send_file(filepath, as_attachment=True)
        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            return jsonify({'error': 'File not found'}), 404 