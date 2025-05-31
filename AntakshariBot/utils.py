import logging
from AntakshariBot.database import db

logger = logging.getLogger(__name__)

async def format_leaderboard(limit: int = 10) -> str:
    """Format leaderboard for display"""
    try:
        leaderboard = await db.get_leaderboard(limit)
        
        if not leaderboard:
            return "🏆 **Global Leaderboard**\n\nNo players yet! Be the first to play!"
        
        text = "🏆 **Global Leaderboard**\n\n"
        
        for i, player in enumerate(leaderboard, 1):
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}️⃣"
            
            name = player.get("user_name", "Unknown")
            points = player.get("total_points", 0)
            games_won = player.get("games_won", 0)
            games_played = player.get("games_played", 0)
            
            win_rate = (games_won / max(games_played, 1)) * 100
            
            text += f"{emoji} **{name}**\n"
            text += f"   💯 {points} points | 🏆 {games_won} wins | 📊 {win_rate:.1f}%\n\n"
        
        return text
        
    except Exception as e:
        logger.error(f"Error formatting leaderboard: {e}")
        return "❌ Error loading leaderboard. Please try again."

async def get_user_stats(user_id: int) -> dict:
    """Get user statistics"""
    try:
        return await db.get_player_stats(user_id)
    except Exception as e:
        logger.error(f"Error getting user stats: {e}")
        return None

async def format_game_history(chat_id: int) -> str:
    """Format game history for a chat"""
    try:
        stats = await db.get_game_stats(chat_id)
        
        text = f"📊 **Game Statistics**\n\n"
        text += f"🎮 Total Games: {stats['total_games']}\n\n"
        
        if stats['recent_games']:
            text += "📈 **Recent Games:**\n"
            for game in stats['recent_games']:
                winner = max(game.get('players', []), key=lambda p: p.get('score', 0), default={'name': 'Unknown', 'score': 0})
                text += f"• Winner: {winner['name']} ({winner['score']} pts)\n"
        
        return text
        
    except Exception as e:
        logger.error(f"Error formatting game history: {e}")
        return "❌ Error loading game history."
