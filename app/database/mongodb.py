from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        self.client = AsyncIOMotorClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB_NAME]

    async def close(self):
        if self.client:
            self.client.close()

mongodb = MongoDB()

