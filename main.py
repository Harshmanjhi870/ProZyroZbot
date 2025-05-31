import asyncio
import logging
from pyrogram import Client
from AntakshariBot.bot import AntakshariBot
from AntakshariBot.database import init_db
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('antakshari_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

async def main():
    """Main function to start the Antakshari bot"""
    try:
        # Initialize database
        await init_db()
        logger.info("Database initialized successfully")
        
        # Initialize and start bot
        bot = AntakshariBot()
        await bot.start()
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
