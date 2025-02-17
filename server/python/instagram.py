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
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def extract_instagram_id(url):
    """Extract the Instagram shortcode from URL."""
    patterns = [
        r'instagram.com/(?:p|reel)/([^/?]+)',
        r'instagram.com/.*/reel/([^/?]+)'
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
    """Download Instagram content using instaloader with enhanced error handling."""
    try:
        logger.info(f"Starting download for URL: {url}")
        shortcode = extract_instagram_id(url)
        logger.info(f"Extracted shortcode: {shortcode}")

        # Initialize instaloader with more detailed logging and relaxed rate limits
        L = instaloader.Instaloader(
            dirname_pattern=downloads_dir,
            filename_pattern=shortcode,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            post_metadata_txt_pattern='',
            max_connection_attempts=5,
            request_timeout=60,
            rate_controller=None  # Disable rate limiting for testing
        )

        # Download with retry logic
        max_retries = 3
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                logger.info(f"Download attempt {attempt + 1} of {max_retries}")

                # Get post instance
                logger.info("Fetching post information...")
                post = instaloader.Post.from_shortcode(L.context, shortcode)

                # Determine content type and download
                if post.is_video:
                    logger.info("Detected video content")
                    file_path = os.path.join(downloads_dir, f"{shortcode}.mp4")
                    content_type = 'video/mp4'
                    logger.info("Starting video download...")
                    L.download_post(post, target=shortcode)
                else:
                    logger.info("Detected image content")
                    file_path = os.path.join(downloads_dir, f"{shortcode}.jpg")
                    content_type = 'image/jpeg'
                    logger.info("Starting image download...")
                    L.download_post(post, target=shortcode)

                # Verify file exists and has content
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    file_size = os.path.getsize(file_path)
                    logger.info(f"Successfully downloaded content to: {file_path} (Size: {file_size} bytes)")
                    return file_path, content_type
                else:
                    raise Exception("Download completed but file is missing or empty")

            except InstaloaderException as e:
                logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < max_retries - 1:
                    logger.info(f"Waiting {retry_delay} seconds before retry...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    raise

    except InstaloaderException as e:
        logger.error(f"Instaloader error: {str(e)}")
        raise Exception(f"Failed to download content: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise Exception(f"Failed to download content: {str(e)}")