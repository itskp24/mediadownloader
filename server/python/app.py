from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from instagram import download_instagram_content

app = Flask(__name__)
CORS(app)

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
        
    try:
        file_path, content_type = download_instagram_content(url)
        return send_file(
            file_path,
            as_attachment=True,
            download_name=os.path.basename(file_path),
            mimetype=content_type
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
