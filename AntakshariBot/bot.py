import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from AntakshariBot.game_manager import GameManager
from AntakshariBot.database import db
from AntakshariBot.utils import format_leaderboard, get_user_stats
import config

logger = logging.getLogger(__name__)

class AntakshariBot:
    def __init__(self):
        self.app = Client(
            "antakshari_bot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.TELEGRAM_TOKEN
        )
        
        self.game_manager = GameManager()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup all bot handlers"""
        
        @self.app.on_message(filters.command("start") & filters.private)
        async def start_private(client, message: Message):
            await message.reply_text(
                f"🎮 **Welcome to {config.BOT_NAME}!**\n\n"
                "🌍 **Country Antakshari Game**\n"
                "Play the classic word game with country and city names!\n\n"
                "**How to Play:**\n"
                "• Add me to a group\n"
                "• Use /antakshari to start a game\n"
                "• Players join with /join\n"
                "• Say country/city names in sequence\n\n"
                "**Commands:**\n"
                "/help - Show help\n"
                "/stats - Your game statistics\n"
                "/leaderboard - Top players\n\n"
                "Add me to a group to start playing! 🎯",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📖 Help", callback_data="help")],
                    [InlineKeyboardButton("📊 Global Stats", callback_data="global_stats")]
                ])
            )
        
        @self.app.on_message(filters.command("help"))
        async def help_command(client, message: Message):
            help_text = (
                "🎮 **Antakshari Game Help**\n\n"
                "**Game Commands:**\n"
                "🎯 `/antakshari` - Start new game\n"
                "🚪 `/join` - Join current game\n"
                "🚫 `/leave` - Leave current game\n"
                "⏹️ `/endgame` - End current game (admin only)\n"
                "📊 `/gamestats` - Current game status\n\n"
                "**Player Commands:**\n"
                "📈 `/stats` - Your statistics\n"
                "🏆 `/leaderboard` - Top 10 players\n"
                "🌍 `/countries` - List of valid countries\n"
                "🏙️ `/cities` - List of valid cities\n\n"
                "**Game Rules:**\n"
                "• Say country or city names\n"
                "• Next word must start with last letter of previous word\n"
                "• No repetition of words\n"
                "• 30 seconds per turn\n"
                "• Earn points for correct answers\n\n"
                "**Scoring:**\n"
                f"• Correct answer: {config.POINTS_PER_WORD} points\n"
                f"• Bonus for rare words: {config.BONUS_POINTS} points\n"
                "• Streak bonus: +1 point per consecutive turn"
            )
            await message.reply_text(help_text)
        
        @self.app.on_message(filters.command("antakshari") & filters.group)
        async def start_game(client, message: Message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            user_name = message.from_user.first_name
            
            # First try to end any existing game in the database
            await self.game_manager.end_game(chat_id)
            
            result = await self.game_manager.start_game(chat_id, user_id, user_name)
            
            if result["success"]:
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🚪 Join Game", callback_data=f"join_{chat_id}")],
                    [InlineKeyboardButton("📊 Game Rules", callback_data="game_rules")]
                ])
                
                await message.reply_text(
                    f"🎮 **Antakshari Game Started!**\n\n"
                    f"🌍 **Theme:** Countries & Cities\n"
                    f"👤 **Started by:** {user_name}\n"
                    f"⏰ **Join Time:** {config.JOIN_TIME} seconds\n"
                    f"👥 **Players:** 1/{config.MAX_PLAYERS}\n\n"
                    f"🚪 Use /join or click button to join!\n"
                    f"⏱️ Game starts automatically in {config.JOIN_TIME} seconds",
                    reply_markup=keyboard
                )
                
                # Start join timer
                asyncio.create_task(self.game_manager.start_join_timer(chat_id, client))
            else:
                await message.reply_text(f"❌ {result['message']}")
        
        @self.app.on_message(filters.command("join") & filters.group)
        async def join_game(client, message: Message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            user_name = message.from_user.first_name
            
            result = await self.game_manager.join_game(chat_id, user_id, user_name)
            
            if result["success"]:
                game = result["game"]
                await message.reply_text(
                    f"✅ {user_name} joined the game!\n"
                    f"👥 Players: {len(game['players'])}/{config.MAX_PLAYERS}\n"
                    f"⏰ Time left: {result.get('time_left', 'Unknown')} seconds"
                )
            else:
                await message.reply_text(f"❌ {result['message']}")
        
        @self.app.on_message(filters.command("leave") & filters.group)
        async def leave_game(client, message: Message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            user_name = message.from_user.first_name
            
            result = await self.game_manager.leave_game(chat_id, user_id)
            
            if result["success"]:
                await message.reply_text(f"👋 {user_name} left the game!")
            else:
                await message.reply_text(f"❌ {result['message']}")
        
        @self.app.on_message(filters.command("endgame") & filters.group)
        async def end_game(client, message: Message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            
            # Check if user is admin
            member = await client.get_chat_member(chat_id, user_id)
            if member.status not in ["administrator", "creator"]:
                await message.reply_text("❌ Only admins can end the game.")
                return
            
            result = await self.game_manager.end_game(chat_id)
            
            if result["success"]:
                await message.reply_text("🛑 Game ended by admin!")
            else:
                await message.reply_text(f"❌ {result['message']}")
        
        @self.app.on_message(filters.text & filters.group & ~filters.command(["antakshari", "join", "leave", "endgame", "help", "stats", "leaderboard", "gamestats", "countries", "cities"]))
        async def handle_game_message(client, message: Message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            user_name = message.from_user.first_name
            word = message.text.strip().lower()
            
            result = await self.game_manager.process_word(chat_id, user_id, user_name, word)
            
            # Only respond if it's the current player's turn
            if result.get("is_current_player", True):
                if result["success"]:
                    if result["type"] == "correct":
                        points = result.get("points", config.POINTS_PER_WORD)
                        streak = result.get("streak", 0)
                        next_letter = result.get("next_letter", "")
                        
                        response = f"✅ **Correct!** +{points} points\n"
                        if streak > 1:
                            response += f"🔥 Streak: {streak}\n"
                        response += f"📝 Next word should start with: **{next_letter.upper()}**\n"
                        response += f"👤 Next player: {result.get('next_player', 'Unknown')}"
                        
                        await message.reply_text(response)
                        
                    elif result["type"] == "game_won":
                        winner = result.get("winner")
                        reason = result.get("reason", "points")
                        
                        if reason == "last_player":
                            response = f"🎉 **Game Over!**\n\n"
                            response += f"🏆 **Winner:** {winner['name']} (Last player standing!)\n"
                            response += f"💯 **Final Score:** {winner['score']} points"
                        else:
                            final_scores = result.get("scores", {})
                            response = f"🎉 **Game Over!**\n\n"
                            response += f"🏆 **Winner:** {winner['name']} ({winner['score']} points)\n\n"
                            response += "📊 **Final Scores:**\n"
                            
                            for player_id, score in sorted(final_scores.items(), key=lambda x: x[1], reverse=True):
                                player_name = result.get("player_names", {}).get(str(player_id), "Unknown")
                                response += f"• {player_name}: {score} points\n"
                        
                        await message.reply_text(response)

                elif result.get("error"):
                    if result.get("eliminated"):
                        await message.reply_text(f"❌ {result['message']}\n🚫 **You have been eliminated!**")
                    else:
                        await message.reply_text(f"❌ {result['message']}")
        
        @self.app.on_message(filters.command("stats"))
        async def user_stats(client, message: Message):
            user_id = message.from_user.id
            user_name = message.from_user.first_name
            
            stats = await get_user_stats(user_id)
            
            if stats:
                response = f"📊 **Stats for {user_name}**\n\n"
                response += f"🎮 Games Played: {stats.get('games_played', 0)}\n"
                response += f"🏆 Games Won: {stats.get('games_won', 0)}\n"
                response += f"📈 Total Points: {stats.get('total_points', 0)}\n"
                response += f"💯 Best Score: {stats.get('best_score', 0)}\n"
                response += f"🔥 Best Streak: {stats.get('best_streak', 0)}\n"
                response += f"✅ Correct Words: {stats.get('correct_words', 0)}\n"
                response += f"❌ Wrong Words: {stats.get('wrong_words', 0)}\n"
                
                if stats.get('correct_words', 0) > 0:
                    accuracy = (stats.get('correct_words', 0) / (stats.get('correct_words', 0) + stats.get('wrong_words', 0))) * 100
                    response += f"🎯 Accuracy: {accuracy:.1f}%\n"
                
                win_rate = (stats.get('games_won', 0) / max(stats.get('games_played', 1), 1)) * 100
                response += f"📊 Win Rate: {win_rate:.1f}%"
            else:
                response = f"📊 **Stats for {user_name}**\n\nNo games played yet! Use /antakshari to start playing."
            
            await message.reply_text(response)
        
        @self.app.on_message(filters.command("leaderboard"))
        async def leaderboard(client, message: Message):
            leaderboard_text = await format_leaderboard()
            await message.reply_text(leaderboard_text)
        
        @self.app.on_message(filters.command("gamestats") & filters.group)
        async def game_stats(client, message: Message):
            chat_id = message.chat.id
            game_info = await self.game_manager.get_game_info(chat_id)
            
            if game_info:
                response = f"🎮 **Current Game Status**\n\n"
                response += f"📊 Status: {game_info['status'].title()}\n"
                response += f"👥 Players: {len(game_info['players'])}\n"
                
                if game_info['status'] == 'active':
                    response += f"🎯 Current Turn: {game_info.get('current_player_name', 'Unknown')}\n"
                    response += f"📝 Last Word: {game_info.get('last_word', 'None')}\n"
                    response += f"🔤 Next Letter: {game_info.get('next_letter', 'Any').upper()}\n"
                    response += f"📈 Round: {game_info.get('round', 1)}\n\n"
                    
                    response += "📊 **Current Scores:**\n"
                    for player in game_info['players']:
                        response += f"• {player['name']}: {player['score']} points\n"
                
                await message.reply_text(response)
            else:
                await message.reply_text("❌ No active game in this group.")
        
        @self.app.on_callback_query()
        async def handle_callbacks(client, callback_query):
            data = callback_query.data
            user_id = callback_query.from_user.id
            user_name = callback_query.from_user.first_name
            
            if data.startswith("join_"):
                chat_id = int(data.split("_")[1])
                result = await self.game_manager.join_game(chat_id, user_id, user_name)
                
                if result["success"]:
                    await callback_query.answer(f"✅ Joined the game!", show_alert=True)
                else:
                    await callback_query.answer(f"❌ {result['message']}", show_alert=True)
            
            elif data == "help":
                help_text = (
                    "🎮 How to Play:\n"
                    "1️⃣ /antakshari to start\n"
                    "2️⃣ /join to join game\n"
                    "3️⃣ Say country/city names\n"
                    "4️⃣ Next word starts with last letter\n"
                    "5️⃣ No repetition allowed"
                )
                await callback_query.answer(help_text, show_alert=True)
            
            elif data == "game_rules":
                rules_text = (
                    "📋 Rules:\n"
                    "• Country/city names only\n"
                    "• 30 seconds per turn\n"
                    "• No repetition\n"
                    "• Get eliminated if timeout\n"
                    "• Last player wins"
                )
                await callback_query.answer(rules_text, show_alert=True)
    
    async def start(self):
        """Start the bot"""
        try:
            await self.app.start()
            logger.info(f"{config.BOT_NAME} started successfully")
            
            # Keep the bot running
            await asyncio.Event().wait()
            
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            raise
        finally:
            await self.app.stop()
