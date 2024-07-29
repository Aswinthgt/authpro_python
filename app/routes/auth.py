from fastapi import APIRouter

from app.models.auth import authData, authVerify
from app.controllers.auth import loginController, sign_up_controller, verify_and_Create


auth = APIRouter(tags=["Auth"], prefix="/auth")


@auth.post("/login")
async def login(user_data: authData) -> str:
    return await loginController(user_data.model_dump())


@auth.post("/signup")
async def sign_up(user_data: authData):
    return await sign_up_controller(user_data.model_dump())


@auth.post("/signup/verify")
async def verify(data: authVerify):
    return await verify_and_Create(data.model_dump())
