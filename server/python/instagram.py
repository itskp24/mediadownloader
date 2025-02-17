import requests
import json
import re
import os
import logging
import time
import instaloader
from instaloader.exceptions import InstaloaderException
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_instagram_id(url):
    """Extract the Instagram shortcode from URL."""
    patterns = [
        r'instagram.com/p/([^/?]+)',
        r'instagram.com/reel/([^/?]+)'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            shortcode = match.group(1)
            logger.info(f"Extracted shortcode: {shortcode} from URL: {url}")
            return shortcode

    logger.error(f"Failed to extract shortcode from URL: {url}")
    raise ValueError("Invalid Instagram URL format")

def download_instagram_content(url, downloads_dir):
    """Download Instagram content using instaloader."""
    try:
        logger.info(f"Starting download for URL: {url}")
        shortcode = extract_instagram_id(url)
        logger.info(f"Extracted shortcode: {shortcode}")

        # Initialize instaloader with more detailed logging
        L = instaloader.Instaloader(
            dirname_pattern=downloads_dir,
            filename_pattern=shortcode,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            post_metadata_txt_pattern='',
            max_connection_attempts=3
        )

        # Download the post
        logger.info("Initializing post download...")
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # Determine content type and download
        if post.is_video:
            logger.info("Detected video content")
            file_path = os.path.join(downloads_dir, f"{shortcode}.mp4")
            content_type = 'video/mp4'
            L.download_post(post, target=shortcode)
        else:
            logger.info("Detected image content")
            file_path = os.path.join(downloads_dir, f"{shortcode}.jpg")
            content_type = 'image/jpeg'
            L.download_post(post, target=shortcode)

        # Verify file exists and has content
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            logger.info(f"Successfully downloaded content to: {file_path}")
            return file_path, content_type
        else:
            raise Exception("Download completed but file is missing or empty")

    except InstaloaderException as e:
        logger.error(f"Instaloader error: {str(e)}")
        raise Exception(f"Failed to download content: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise Exception(f"Failed to download content: {str(e)}")