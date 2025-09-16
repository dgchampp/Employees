import motor.motor_asyncio
from .config import MONGO_URI, DB_NAME

# MongoDB client and database
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]


async def init_db():
    """Initialize database indexes"""
    # Ensure unique indexes
    await db.employees.create_index("employee_id", unique=True)
    await db.users.create_index("username", unique=True)


async def close_db():
    """Close database connection"""
    client.close()
