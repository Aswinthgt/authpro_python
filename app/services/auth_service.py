from app.db.database import auth_db
import random

collection = auth_db.get_collection("user")


async def is_old_user(user_data):
    result = await collection.find_one({"user_name": user_data["user_name"]})
    if result:
        return result
    else:
        return None


def random_six_digit():
    return random.randint(100000, 999999)


async def create_user(user_data):
    result = await collection.insert_one(user_data)
    if result.inserted_id:
        return result
    else:
        return None
