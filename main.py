import asyncio
import logging
from pyrogram import Client
from AntakshariBot.bot import AntakshariBot
from AntakshariBot.database import init_db
from AntakshariBot.data.data_loader import init_data_loader
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
        
        # Initialize data loader (countries and cities)
        data_loaded = await init_data_loader()
        if data_loaded:
            logger.info("Word data loaded successfully")
        else:
            logger.warning("Failed to load word data, using fallback data")
        
        # Initialize and start bot
        bot = AntakshariBot()
        await bot.start()
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
