from motor.motor_asyncio import AsyncIOMotorClient
import os


MONGO_URI = os.getenv('MONGODB_URI')

client = AsyncIOMotorClient(MONGO_URI)

auth_db = client['authDB']  # create DB using manually