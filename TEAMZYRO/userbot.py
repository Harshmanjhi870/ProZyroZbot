import asyncio
import logging
from pyrogram import Client
from TEAMZYRO.Userbot_modules.cleanup import CleanupModule
import config

logger = logging.getLogger(__name__)

class UserBot:
    def __init__(self):
        self.app = Client(
            "userbot_session",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=config.SESSION
        )
        
        # Initialize modules
        self.cleanup_module = CleanupModule(self.app)
    
    async def start(self):
        """Start the userbot"""
        try:
            await self.app.start()
            
            # Send startup message to logging group
            if config.LOGGING_GROUP:
                await self.app.send_message(
                    config.LOGGING_GROUP,
                    f"👤 **UserBot Started**\n\n"
                    f"Status: ✅ Online\n"
                    f"Cleanup: 🧹 Active (240s interval)"
                )
            
            logger.info("UserBot started successfully")
            
            # Start cleanup task
            asyncio.create_task(self.cleanup_module.start_cleanup_task())
            
            # Keep the userbot running
            await asyncio.Event().wait()
            
        except Exception as e:
            logger.error(f"Error starting userbot: {e}")
            raise
        finally:
            await self.app.stop()
