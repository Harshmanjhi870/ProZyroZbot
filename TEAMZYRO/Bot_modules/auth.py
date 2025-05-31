import logging
from pyrogram import filters
from pyrogram.types import Message
from TEAMZYRO.database import db
import config

logger = logging.getLogger(__name__)

class AuthModule:
    def __init__(self, app):
        self.app = app
    
    def register_handlers(self):
        """Register auth-related handlers"""
        
        @self.app.on_message(filters.command("auth") & filters.group)
        async def auth_user(client, message: Message):
            # Check if user is admin
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status not in ["administrator", "creator"]:
                await message.reply_text("❌ Only admins can use this command.")
                return
            
            if not message.reply_to_message:
                await message.reply_text("❌ Reply to a user's message to authorize them.")
                return
            
            user_id = message.reply_to_message.from_user.id
            user_name = message.reply_to_message.from_user.first_name
            
            if await db.add_auth_user(user_id, user_name):
                await message.reply_text(
                    f"✅ User {user_name} has been authorized.\n"
                    f"Their messages will not be deleted."
                )
                logger.info(f"User {user_id} authorized by {message.from_user.id}")
            else:
                await message.reply_text("❌ Failed to authorize user.")
        
        @self.app.on_message(filters.command("unauth") & filters.group)
        async def unauth_user(client, message: Message):
            # Check if user is admin
            member = await client.get_chat_member(message.chat.id, message.from_user.id)
            if member.status not in ["administrator", "creator"]:
                await message.reply_text("❌ Only admins can use this command.")
                return
            
            if not message.reply_to_message:
                await message.reply_text("❌ Reply to a user's message to remove their authorization.")
                return
            
            user_id = message.reply_to_message.from_user.id
            user_name = message.reply_to_message.from_user.first_name
            
            if await db.remove_auth_user(user_id):
                await message.reply_text(
                    f"✅ Authorization removed for {user_name}.\n"
                    f"Their messages will now be subject to protection."
                )
                logger.info(f"User {user_id} unauthorized by {message.from_user.id}")
            else:
                await message.reply_text("❌ User was not authorized or failed to remove authorization.")
