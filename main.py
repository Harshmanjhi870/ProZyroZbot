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
        
        # Initialize data loader (countries and cities from JSON)
        data_loaded = await init_data_loader()
        if data_loaded:
            logger.info("Word data loaded successfully from JSON file")
        else:
            logger.warning("Failed to load word data from JSON file, using fallback data")
            logger.warning("Make sure to upload countries_cities.json to AntakshariBot/data/ folder")
        
        # Initialize and start bot
        bot = AntakshariBot()
        await bot.start()
        
    except Exception as e:
        logger.error(f"Error in main: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
