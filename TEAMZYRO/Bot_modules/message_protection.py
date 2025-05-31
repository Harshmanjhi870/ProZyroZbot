import logging
from pyrogram import filters
from pyrogram.types import Message
from TEAMZYRO.database import db
import config

logger = logging.getLogger(__name__)

class MessageProtection:
    def __init__(self, app):
        self.app = app
        self.original_messages = {}  # Store original messages
    
    def register_handlers(self):
        """Register message protection handlers"""
        
        @self.app.on_message(filters.group)
        async def store_message(client, message: Message):
            # Store original message content for edit detection
            self.original_messages[message.id] = {
                'text': message.text,
                'user_id': message.from_user.id,
                'chat_id': message.chat.id
            }
        
        @self.app.on_edited_message(filters.group)
        async def handle_edited_message(client, message: Message):
            # Check if user is authorized
            auth_users = await db.get_auth_users()
            if message.from_user.id in auth_users:
                return
            
            try:
                await message.delete()
                logger.info(f"Deleted edited message from user {message.from_user.id}")
            except Exception as e:
                logger.error(f"Failed to delete edited message: {e}")
