import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Binance Testnet Configuration
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', '')
BINANCE_API_SECRET = os.getenv('BINANCE_API_SECRET', '')
TESTNET_BASE_URL = 'https://testnet.binancefuture.com'

# Logging Configuration
LOG_FILE = 'logs/trading_bot.log'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'
