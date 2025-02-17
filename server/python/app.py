from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from instagram import download_instagram_content
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create downloads directory
downloads_dir = os.path.join(os.path.dirname(__file__), '../../downloads')
os.makedirs(downloads_dir, exist_ok=True)

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        logger.info(f"Attempting to download content from URL: {url}")
        file_path, content_type = download_instagram_content(url, downloads_dir)
        logger.info(f"Successfully downloaded content to: {file_path}")

        return send_file(
            file_path,
            as_attachment=True,
            download_name=os.path.basename(file_path),
            mimetype=content_type
        )
    except Exception as e:
        logger.error(f"Download failed: {str(e)}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)