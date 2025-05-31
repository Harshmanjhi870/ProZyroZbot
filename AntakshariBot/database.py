import logging
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import config

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client = None
        self.db = None
    
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(config.MONGO_URI)
            self.db = self.client[config.DB_NAME]
            
            # Test connection
            await self.client.admin.command('ping')
            logger.info("Database connected successfully")
            
            # Create indexes
            await self.create_indexes()
            
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    async def create_indexes(self):
        """Create database indexes for better performance"""
        try:
            # Games collection indexes
            await self.db.games.create_index("chat_id", unique=True)
            await self.db.games.create_index("status")
            
            # Player stats indexes
            await self.db.player_stats.create_index("user_id", unique=True)
            await self.db.player_stats.create_index("total_points")
            await self.db.player_stats.create_index("games_won")
            
            # Game history indexes
            await self.db.game_history.create_index("chat_id")
            await self.db.game_history.create_index("date")
            
            logger.info("Database indexes created successfully")
            
        except Exception as e:
            logger.error(f"Error creating indexes: {e}")
    
    async def create_game(self, game_data: dict):
        """Create a new game record"""
        try:
            # First check if a game already exists for this chat
            existing_game = await self.db.games.find_one({"chat_id": game_data["chat_id"]})
            
            if existing_game:
                # Update the existing game instead of creating a new one
                await self.update_game(game_data["chat_id"], game_data)
                logger.info(f"Updated existing game for chat {game_data['chat_id']}")
                return
            
            # Create new game record if none exists
            game_record = {
                "chat_id": game_data["chat_id"],
                "status": game_data["status"],
                "players": game_data["players"],
                "creator": game_data["creator"],
                "start_time": datetime.utcnow(),
                "current_player": game_data["current_player"],
                "last_word": game_data["last_word"],
                "next_letter": game_data["next_letter"],
                "round": game_data["round"],
                "used_words": list(game_data["used_words"])
            }
            
            await self.db.games.insert_one(game_record)
            logger.info(f"Game created for chat {game_data['chat_id']}")
            
        except Exception as e:
            logger.error(f"Error creating game: {e}")
    
    async def update_game(self, chat_id: int, game_data: dict):
        """Update existing game record"""
        try:
            update_data = {
                "status": game_data["status"],
                "players": game_data["players"],
                "current_player": game_data["current_player"],
                "last_word": game_data["last_word"],
                "next_letter": game_data["next_letter"],
                "round": game_data["round"],
                "used_words": list(game_data["used_words"]),
                "updated_time": datetime.utcnow()
            }
            
            await self.db.games.update_one(
                {"chat_id": chat_id},
                {"$set": update_data}
            )
            
        except Exception as e:
            logger.error(f"Error updating game: {e}")
    
    async def end_game(self, chat_id: int):
        """End a game and move to history"""
        try:
            # Get game data
            game = await self.db.games.find_one({"chat_id": chat_id})
            
            if game:
                # Move to history
                game["end_time"] = datetime.utcnow()
                game["status"] = "completed"
                await self.db.game_history.insert_one(game)
                
                # Remove from active games
                await self.db.games.delete_one({"chat_id": chat_id})
                
                logger.info(f"Game ended for chat {chat_id}")
            
        except Exception as e:
            logger.error(f"Error ending game: {e}")
    
    async def update_player_stats(self, user_id: int, user_name: str, action: str, points: int = 0, won: bool = False):
        """Update player statistics"""
        try:
            # Get current stats
            stats = await self.db.player_stats.find_one({"user_id": user_id})
            
            if not stats:
                stats = {
                    "user_id": user_id,
                    "user_name": user_name,
                    "games_played": 0,
                    "games_won": 0,
                    "total_points": 0,
                    "best_score": 0,
                    "best_streak": 0,
                    "correct_words": 0,
                    "wrong_words": 0,
                    "first_played": datetime.utcnow(),
                    "last_played": datetime.utcnow()
                }
            
            # Update based on action
            if action == "correct_word":
                stats["correct_words"] += 1
                stats["total_points"] += points
                stats["best_score"] = max(stats["best_score"], points)
            
            elif action == "wrong_word":
                stats["wrong_words"] += 1
            
            elif action == "game_finished":
                stats["games_played"] += 1
                if won:
                    stats["games_won"] += 1
                stats["best_score"] = max(stats["best_score"], points)
            
            stats["user_name"] = user_name  # Update name in case it changed
            stats["last_played"] = datetime.utcnow()
            
            # Upsert the document
            await self.db.player_stats.update_one(
                {"user_id": user_id},
                {"$set": stats},
                upsert=True
            )
            
        except Exception as e:
            logger.error(f"Error updating player stats: {e}")
    
    async def get_player_stats(self, user_id: int):
        """Get player statistics"""
        try:
            return await self.db.player_stats.find_one({"user_id": user_id})
        except Exception as e:
            logger.error(f"Error getting player stats: {e}")
            return None
    
    async def get_leaderboard(self, limit: int = 10):
        """Get top players leaderboard"""
        try:
            cursor = self.db.player_stats.find().sort("total_points", -1).limit(limit)
            return await cursor.to_list(length=limit)
        except Exception as e:
            logger.error(f"Error getting leaderboard: {e}")
            return []
    
    async def get_game_stats(self, chat_id: int):
        """Get game statistics for a chat"""
        try:
            # Count total games in this chat
            total_games = await self.db.game_history.count_documents({"chat_id": chat_id})
            
            # Get recent games
            recent_games = await self.db.game_history.find(
                {"chat_id": chat_id}
            ).sort("end_time", -1).limit(5).to_list(length=5)
            
            return {
                "total_games": total_games,
                "recent_games": recent_games
            }
            
        except Exception as e:
            logger.error(f"Error getting game stats: {e}")
            return {"total_games": 0, "recent_games": []}

# Global database instance
db = Database()

async def init_db():
    """Initialize database connection"""
    await db.connect()
