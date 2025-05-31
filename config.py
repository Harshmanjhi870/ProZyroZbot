import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN_HERE")
API_ID = int(os.getenv("API_ID", "YOUR_API_ID"))
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")

# Database Configuration
MONGO_URI = os.getenv("MONGO_URI", "YOUR_MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "antakshari_bot_db")

# Bot Settings
OWNER_ID = int(os.getenv("OWNER_ID", "YOUR_OWNER_ID"))
BOT_NAME = os.getenv("BOT_NAME", "Antakshari Game Bot")
LOGGER = True

# Game Settings
JOIN_TIME = 60  # 60 seconds to join
TURN_TIME = 30  # 30 seconds per turn
MIN_PLAYERS = 2  # Minimum players to start game
MAX_PLAYERS = 20  # Maximum players in a game
POINTS_PER_WORD = 10  # Points for correct answer
BONUS_POINTS = 5  # Bonus for difficult words
