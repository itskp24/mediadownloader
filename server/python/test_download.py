import os
from instagram import download_instagram_content
import logging
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_instagram_download():
    # Create downloads directory
    downloads_dir = os.path.join(os.path.dirname(__file__), '../../downloads')

    # Clean up old downloads
    if os.path.exists(downloads_dir):
        shutil.rmtree(downloads_dir)
    os.makedirs(downloads_dir, exist_ok=True)

    # Test URLs
    test_urls = [
        "https://www.instagram.com/p/CueUzxluh5a/",  # photo
        "https://www.instagram.com/reel/DGH4iFzpsby/"  # reel
    ]

    for url in test_urls:
        try:
            logger.info(f"\nTesting download for URL: {url}")
            file_path, content_type = download_instagram_content(url, downloads_dir)
            logger.info(f"Successfully downloaded content to: {file_path}")
            logger.info(f"Content type: {content_type}")

            # Verify file exists and has size
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                logger.info("✓ File exists and has content")
            else:
                logger.error("✗ File is missing or empty")

        except Exception as e:
            logger.error(f"Failed to download {url}: {str(e)}")

if __name__ == "__main__":
    test_instagram_download()