import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_BOT_TOKEN_HERE")
API_ID = int(os.getenv("API_ID", "YOUR_API_ID"))
API_HASH = os.getenv("API_HASH", "YOUR_API_HASH")
SESSION = os.getenv("SESSION", "YOUR_SESSION_STRING")

# Database Configuration
MONGO_URI = os.getenv("MONGO_URI", "YOUR_MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "telegram_bot_db")

# Bot Settings
OWNER_ID = int(os.getenv("OWNER_ID", "YOUR_OWNER_ID"))
LOGGING_GROUP = int(os.getenv("LOGGING_GROUP", "YOUR_LOGGING_GROUP_ID"))
SUPPORT_ID = int(os.getenv("SUPPORT_ID", "YOUR_SUPPORT_GROUP_ID"))
BOT_NAME = os.getenv("BOT_NAME", "Protection Bot")
LOGGER = True

# Media Settings
POST_INTERVAL = 600  # 10 minutes
BATCH_SIZE = 20
MEDIA_DELETE_TIME = 60  # 60 seconds
USERBOT_CLEANUP_TIME = 240  # 240 seconds
