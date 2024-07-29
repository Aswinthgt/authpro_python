from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from aiocache import Cache
from aiocache.serializers import JsonSerializer
from app.models.auth import authData

from app.config.secret import hash_password, verify_password, create_token
from app.services.common.mail_service import send_mail, EmailSchema
from app.services.auth_service import (
    is_old_user,
    create_user,
    random_six_digit,
)

cache = Cache(Cache.MEMORY, serializer=JsonSerializer())


async def loginController(user_data: authData):
    user = await is_old_user(user_data)
    if not user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No user Found. Create one")
    if not verify_password(user_data['password'], user['password']):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")
    token = create_token({'user_id': str(user['_id'])})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"token": token})

async def sign_up_controller(user_data):
    old_user = await is_old_user(user_data)
    if old_user and old_user['_id']:
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "The user already exist"},
        )

    randomDigit = random_six_digit()
    user_data.update({"otp": randomDigit})
    await cache.set(user_data["email"], user_data, ttl=120)
    email = EmailSchema(
        subject="Otp Verfication",
        email=user_data["email"],
        message=f"Your OTP is {randomDigit}",
    )

    if send_mail(email):
        return "OTP sent to your mail successfully"

    return "Account Creation failed"


async def verify_and_Create(data):
    user_data = await cache.get(data["email"])
    if not user_data or not user_data["otp"]:
        return HTTPException(
            status_code=status.HTTP_408_REQUEST_TIMEOUT, detail="OTP time out"
        )

    if user_data["otp"] != data["otp"]:
        return HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="OTP verification Failed"
        )
    del user_data["otp"]
    user_data["password"] = hash_password(user_data["password"])
    saved_user = await create_user(user_data)
    if saved_user:
        token = create_token({'user_id': str(saved_user.inserted_id)})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={"token": token})
    else:
        return HTTPException(status_code=500, detail="Failed to create User")
