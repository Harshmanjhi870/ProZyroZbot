import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "7785667937:AAHKV2scpVH7SeyMGuyUZHaiYw-z4Rnpj9c")
API_ID = int(os.getenv("API_ID", "23255238"))
API_HASH = os.getenv("API_HASH", "009e3d8c1bdc89d5387cdd8fd182ec15")


MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://nibbanmisal3302:Gokukhan3303@cluster0.0u22b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.getenv("DB_NAME", "antakshari_bot_db")


# Bot Settings
OWNER_ID = int(os.getenv("OWNER_ID", "7073835511"))
BOT_NAME = os.getenv("BOT_NAME", "Atlas")
LOGGER = True

# Game Settings
JOIN_TIME = 60  # 60 seconds to join
TURN_TIME = 30  # 30 seconds per turn
MIN_PLAYERS = 2  # Minimum players to start game
MAX_PLAYERS = 20  # Maximum players in a game
POINTS_PER_WORD = 10  # Points for correct answer
BONUS_POINTS = 5  # Bonus for difficult words
