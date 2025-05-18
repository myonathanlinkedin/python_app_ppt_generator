import os
import logging
from flask import Flask, render_template, jsonify, request
from src.controllers.presentation_controller import PresentationController
from werkzeug.exceptions import HTTPException
import traceback

# Configure logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'app.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize and register controllers
presentation_controller = PresentationController()
app.register_blueprint(presentation_controller.blueprint, url_prefix='/api')

@app.before_request
def log_request_info():
    """Log request details for debugging."""
    if request.path != '/favicon.ico':  # Skip favicon requests
        logger.debug('Headers: %s', dict(request.headers))
        if request.is_json:
            logger.debug('Body: %s', request.get_data())

@app.after_request
def after_request(response):
    """Log response details."""
    if request.path != '/favicon.ico':  # Skip favicon requests
        logger.info(f'{request.method} {request.path} {response.status_code}')
    return response

@app.errorhandler(Exception)
def handle_exception(e):
    """Global exception handler."""
    # Log the full stack trace
    logger.error('Unhandled Exception: %s', str(e), exc_info=True)
    logger.error('Stack Trace: %s', traceback.format_exc())
    
    # Pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # Return JSON instead of HTML for other errors
    return jsonify(error=str(e)), 500

@app.route('/')
def index():
    """Render the main application page."""
    logger.info('Serving index page')
    return render_template('index.html')

if __name__ == '__main__':
    logger.info('Starting Flask application...')
    # Ensure the presentations directory exists
    if not os.path.exists('presentations'):
        os.makedirs('presentations')
        logger.info('Created presentations directory')
    app.run(host='0.0.0.0', debug=True) 