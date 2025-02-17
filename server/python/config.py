import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Download Configuration
DOWNLOAD_PATH = os.getenv('DOWNLOAD_PATH', './downloads')
DOWNLOAD_TIMEOUT = int(os.getenv('DOWNLOAD_TIMEOUT', 600))
MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
RETRY_DELAY = int(os.getenv('RETRY_DELAY', 5))

# Instagram Configuration (optional)
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# API Configuration
API_PORT = int(os.getenv('API_PORT', 8000))

# Ensure downloads directory exists
os.makedirs(os.path.abspath(DOWNLOAD_PATH), exist_ok=True)
