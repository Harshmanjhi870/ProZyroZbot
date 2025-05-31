import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from TEAMZYRO.Bot_modules.auth import AuthModule
from TEAMZYRO.Bot_modules.media_protection import MediaProtection
from TEAMZYRO.Bot_modules.message_protection import MessageProtection
import config

logger = logging.getLogger(__name__)

class Bot:
    def __init__(self):
        self.app = Client(
            "protection_bot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.TELEGRAM_TOKEN
        )
        
        # Initialize modules
        self.auth_module = AuthModule(self.app)
        self.media_protection = MediaProtection(self.app)
        self.message_protection = MessageProtection(self.app)
        
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup all bot handlers"""
        
        @self.app.on_message(filters.command(["start", "help"]))
        async def start_handler(client, message: Message):
            await message.reply_text(
                f"🛡️ **{config.BOT_NAME}** is now active!\n\n"
                "**Features:**\n"
                "• Auto-delete media files after 60 seconds\n"
                "• Auto-delete PDF files immediately\n"
                "• Protection against message editing/deletion\n"
                "• Auth system for trusted users\n\n"
                "**Admin Commands:**\n"
                "/auth - Authorize a user\n"
                "/unauth - Remove authorization\n"
                "/status - Check bot status"
            )
        
        # Register module handlers
        self.auth_module.register_handlers()
        self.media_protection.register_handlers()
        self.message_protection.register_handlers()
    
    async def start(self):
        """Start the bot"""
        try:
            await self.app.start()
            
            # Send startup message to logging group
            if config.LOGGING_GROUP:
                await self.app.send_message(
                    config.LOGGING_GROUP,
                    f"🤖 **Bot Started**\n\n"
                    f"Bot Name: {config.BOT_NAME}\n"
                    f"Status: ✅ Online\n"
                    f"Protection: 🛡️ Active"
                )
            
            logger.info("Bot started successfully")
            
            # Keep the bot running
            await asyncio.Event().wait()
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise
        finally:
            await self.app.stop()
