from flask import Flask, request, jsonify, send_file, Response
from flask_cors import CORS
import os
from instagram import download_instagram_content
import logging
import traceback

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create downloads directory
downloads_dir = os.path.join(os.path.dirname(__file__), '../../downloads')
os.makedirs(downloads_dir, exist_ok=True)

@app.route('/api/test', methods=['GET'])
def test():
    """Test endpoint to verify API is working"""
    return jsonify({
        'status': 'success',
        'message': 'API is working'
    })

@app.route('/api/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        logger.info(f"Attempting to download content from URL: {url}")

        # Ensure downloads directory exists
        os.makedirs(downloads_dir, exist_ok=True)

        try:
            file_path, content_type = download_instagram_content(url, downloads_dir)
            logger.info(f"Successfully downloaded content to: {file_path}")

            if not os.path.exists(file_path):
                raise Exception("Downloaded file not found")

            # Set response timeout to a higher value
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
    # Configure for longer timeouts
    app.run(
        host='0.0.0.0',
        port=8000,
        threaded=True,
        request_timeout=300  # 5 minutes timeout
    )