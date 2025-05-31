import asyncio
import logging
from pyrogram import filters
from pyrogram.types import Message
from TEAMZYRO.database import db
import config

logger = logging.getLogger(__name__)

class MediaProtection:
    def __init__(self, app):
        self.app = app
    
    def register_handlers(self):
        """Register media protection handlers"""
        
        @self.app.on_message(filters.document & filters.group)
        async def handle_documents(client, message: Message):
            # Check if user is authorized
            auth_users = await db.get_auth_users()
            if message.from_user.id in auth_users:
                return
            
            # Check if document is PDF
            if message.document.mime_type == "application/pdf":
                try:
                    await message.delete()
                    logger.info(f"Deleted PDF from user {message.from_user.id}")
                except Exception as e:
                    logger.error(f"Failed to delete PDF: {e}")
        
        @self.app.on_message((filters.photo | filters.video | filters.animation) & filters.group)
        async def handle_media(client, message: Message):
            # Check if user is authorized
            auth_users = await db.get_auth_users()
            if message.from_user.id in auth_users:
                return
            
            # Schedule deletion after 60 seconds
            asyncio.create_task(self.delete_after_delay(message, config.MEDIA_DELETE_TIME))
    
    async def delete_after_delay(self, message: Message, delay: int):
        """Delete message after specified delay"""
        try:
            await asyncio.sleep(delay)
            await message.delete()
            logger.info(f"Deleted media message from user {message.from_user.id} after {delay}s")
        except Exception as e:
            logger.error(f"Failed to delete media after delay: {e}")
