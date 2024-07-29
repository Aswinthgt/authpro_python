from fastapi import FastAPI
from app.routes import auth

app = FastAPI()


@app.get('/')
def root() -> str:
    return "AuthPro Python Server"


app.include_router(auth.auth)