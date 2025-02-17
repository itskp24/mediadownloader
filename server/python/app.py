from flask import Flask, request, jsonify, send_file, Response, stream_with_context
from flask_cors import CORS
import os
import sys
from instagram import download_instagram_content
import logging
import traceback
import time
import shutil
from config import DOWNLOAD_PATH, API_PORT, DOWNLOAD_TIMEOUT

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

# Use configured downloads directory
DOWNLOADS_DIR = os.path.abspath(DOWNLOAD_PATH)
os.makedirs(DOWNLOADS_DIR, exist_ok=True)
logger.info(f"Downloads directory set to: {DOWNLOADS_DIR}")

@app.route('/api/test', methods=['GET'])
def test():
    """Test endpoint to verify API is working"""
    logger.info("Test endpoint called")
    return jsonify({
        'status': 'success',
        'message': 'API is working',
        'config': {
            'downloads_dir': DOWNLOADS_DIR,
            'timeout': DOWNLOAD_TIMEOUT
        }
    })

def send_file_partial(path, mimetype):
    """Stream file in chunks to prevent timeout"""
    file_size = os.path.getsize(path)
    logger.info(f"Preparing to stream file: {path} (size: {file_size} bytes)")

    def generate():
        with open(path, 'rb') as f:
            while True:
                chunk = f.read(8192)  # 8KB chunks
                if not chunk:
                    break
                yield chunk

    headers = {
        'Content-Type': mimetype,
        'Content-Length': file_size,
        'Content-Disposition': f'attachment; filename="{os.path.basename(path)}"'
    }

    return Response(
        stream_with_context(generate()),
        headers=headers
    )

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
            # Clean up old files in downloads directory
            for filename in os.listdir(DOWNLOADS_DIR):
                filepath = os.path.join(DOWNLOADS_DIR, filename)
                try:
                    if os.path.isfile(filepath):
                        os.unlink(filepath)
                except Exception as e:
                    logger.warning(f"Error deleting old file {filepath}: {e}")

            # Download new content
            file_path, content_type = download_instagram_content(url, DOWNLOADS_DIR)
            logger.info(f"Content downloaded to: {file_path}")

            if not os.path.exists(file_path):
                logger.error("Downloaded file not found")
                raise Exception("Downloaded file not found")

            # Log file details
            file_size = os.path.getsize(file_path)
            logger.info(f"File ready for streaming: {file_path} ({file_size} bytes)")

            # Stream the file in chunks
            return send_file_partial(file_path, content_type)

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
        # Set high timeout values
        app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        app.run(
            host='0.0.0.0',
            port=API_PORT,
            threaded=True,
            debug=True
        )
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}\n{traceback.format_exc()}")
        sys.exit(1)