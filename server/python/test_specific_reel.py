import logging
from instagram import download_instagram_content
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_specific_reel():
    # Test URL
    url = "https://www.instagram.com/kiran.mazumder/reel/DCllrXiBO3u/"
    
    # Create downloads directory
    downloads_dir = os.path.join(os.path.dirname(__file__), '../../downloads')
    os.makedirs(downloads_dir, exist_ok=True)
    
    try:
        logger.info(f"Testing download for URL: {url}")
        file_path, content_type = download_instagram_content(url, downloads_dir)
        
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            logger.info(f"Successfully downloaded to: {file_path}")
            logger.info(f"File size: {size} bytes")
            logger.info(f"Content type: {content_type}")
        else:
            logger.error("File was not downloaded successfully")
            
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        raise

if __name__ == "__main__":
    test_specific_reel()
