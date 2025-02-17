import requests
import json
import re
import os
from bs4 import BeautifulSoup

def extract_instagram_id(url):
    patterns = [
        r'instagram.com/p/([^/?]+)',
        r'instagram.com/reel/([^/?]+)'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError("Invalid Instagram URL")

def download_instagram_content(url, downloads_dir):
    try:
        shortcode = extract_instagram_id(url)

        # First get the page HTML
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find meta tags with content URLs
        meta_tags = soup.find_all('meta', {'property': ['og:video', 'og:image']})

        if not meta_tags:
            raise ValueError("No media content found")

        # Get the content URL from meta tag
        content_url = None
        content_type = None

        for tag in meta_tags:
            if tag.get('property') == 'og:video':
                content_url = tag.get('content')
                content_type = 'video/mp4'
                break
            elif tag.get('property') == 'og:image':
                content_url = tag.get('content')
                content_type = 'image/jpeg'
                break

        if not content_url:
            raise ValueError("Could not extract media URL")

        # Download the content
        response = requests.get(content_url, headers=headers)
        response.raise_for_status()

        # Save file
        extension = '.mp4' if content_type == 'video/mp4' else '.jpg'
        file_path = os.path.join(downloads_dir, f'{shortcode}{extension}')

        with open(file_path, 'wb') as f:
            f.write(response.content)

        return file_path, content_type

    except Exception as e:
        raise Exception(f"Failed to download content: {str(e)}")