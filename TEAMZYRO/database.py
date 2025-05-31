import logging
from motor.motor_asyncio import AsyncIOMotorClient
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
            
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    async def get_auth_users(self):
        """Get list of authorized users"""
        try:
            collection = self.db.auth_users
            users = await collection.find({}).to_list(length=None)
            return [user['user_id'] for user in users]
        except Exception as e:
            logger.error(f"Error getting auth users: {e}")
            return []
    
    async def add_auth_user(self, user_id: int, user_name: str = None):
        """Add authorized user"""
        try:
            collection = self.db.auth_users
            await collection.update_one(
                {'user_id': user_id},
                {'$set': {'user_id': user_id, 'user_name': user_name}},
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Error adding auth user: {e}")
            return False
    
    async def remove_auth_user(self, user_id: int):
        """Remove authorized user"""
        try:
            collection = self.db.auth_users
            result = await collection.delete_one({'user_id': user_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error removing auth user: {e}")
            return False

# Global database instance
db = Database()

async def init_db():
    """Initialize database connection"""
    await db.connect()
