import asyncio
import logging
from pyrogram import Client
from TEAMZYRO.bot import Bot
from TEAMZYRO.userbot import UserBot
from TEAMZYRO.database import init_db
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Main function to start both bot and userbot"""
    try:
        # Initialize database
        await init_db()
        logger.info("Database initialized successfully")
        
        # Initialize bot
        bot = Bot()
        
        # Initialize userbot
        userbot = UserBot()
        
        # Start both bot and userbot concurrently
        await asyncio.gather(
            bot.start(),
            userbot.start()
        )
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
