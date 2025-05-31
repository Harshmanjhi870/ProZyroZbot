import asyncio
import logging
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, MessageDeleteForbidden
import config

logger = logging.getLogger(__name__)

class CleanupModule:
    def __init__(self, app):
        self.app = app
    
    async def start_cleanup_task(self):
        """Start periodic cleanup task"""
        while True:
            try:
                await asyncio.sleep(config.USERBOT_CLEANUP_TIME)
                await self.cleanup_group_media()
            except Exception as e:
                logger.error(f"Error in cleanup task: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def cleanup_group_media(self):
        """Clean up media files in the logging group"""
        try:
            if not config.LOGGING_GROUP:
                return
            
            deleted_count = 0
            async for message in self.app.get_chat_history(config.LOGGING_GROUP, limit=100):
                try:
                    # Check if message contains media
                    if (message.photo or message.video or message.animation or 
                        message.document or message.sticker):
                        
                        await message.delete()
                        deleted_count += 1
                        
                        # Small delay to avoid flood limits
                        await asyncio.sleep(0.5)
                        
                except MessageDeleteForbidden:
                    logger.warning(f"Cannot delete message {message.id} - insufficient permissions")
                except FloodWait as e:
                    logger.warning(f"Flood wait: {e.value} seconds")
                    await asyncio.sleep(e.value)
                except Exception as e:
                    logger.error(f"Error deleting message {message.id}: {e}")
            
            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} media files from group")
                
        except Exception as e:
            logger.error(f"Error in group media cleanup: {e}")
