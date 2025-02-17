from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
import os
import sys
from instagram import download_instagram_content
import logging
import traceback

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('instagram_downloader.log')
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Create downloads directory
downloads_dir = os.path.join(os.path.dirname(__file__), '../../downloads')
os.makedirs(downloads_dir, exist_ok=True)

@app.route('/api/test', methods=['GET'])
def test():
    """Test endpoint to verify API is working"""
    logger.info("Test endpoint called")
    return jsonify({
        'status': 'success',
        'message': 'API is working'
    })

@app.route('/api/download', methods=['POST'])
def download():
    try:
        logger.info("Download endpoint called")
        data = request.get_json()

        if not data:
            logger.error("No JSON data received")
            return jsonify({'error': 'No data provided'}), 400

        url = data.get('url')
        logger.info(f"Received URL: {url}")

        if not url:
            logger.error("No URL provided")
            return jsonify({'error': 'URL is required'}), 400

        try:
            file_path, content_type = download_instagram_content(url, downloads_dir)
            logger.info(f"Content downloaded to: {file_path}")

            if not os.path.exists(file_path):
                logger.error("Downloaded file not found")
                raise Exception("Downloaded file not found")

            return send_file(
                file_path,
                as_attachment=True,
                download_name=os.path.basename(file_path),
                mimetype=content_type
            )

        except Exception as e:
            logger.error(f"Download failed: {str(e)}\n{traceback.format_exc()}")
            return jsonify({
                'error': str(e),
                'details': traceback.format_exc()
            }), 500

    except Exception as e:
        logger.error(f"Server error: {str(e)}\n{traceback.format_exc()}")
        return jsonify({
            'error': 'Internal server error',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    try:
        logger.info("Starting Flask server...")
        app.run(
            host='0.0.0.0',
            port=8000,
            threaded=True,
            debug=True  # Enable debug mode for detailed error messages
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}\n{traceback.format_exc()}")
        sys.exit(1)