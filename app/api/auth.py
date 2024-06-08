from typing import Optional
from fastapi import FastAPI
from prisma.models import User
from pydantic import BaseModel
from app.lib.prisma import prisma
from app.lib.auth.prisma import (
    encrpytedPassword,
    signJWT,
    validatePassword
)

router = FastAPI()

class SignIn(BaseModel):
    email: str
    password: str

class SignUp(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class SignInOut(BaseModel):
    token: str
    user: User

@router.post("/auth/sign-in", tags=["auth"])
async def sign_in(signIn: SignIn):
    user = await prisma.user.find_first(
        where={
            "email": signIn.email,
        }
    )

    validated = validatePassword(signIn.password)
    del user.password

    if validated:
        print(user.id)
        token = signJWT(user.id)
        print(token)
        return SignInOut(token=token, user=user)
    return {"success": False, "error": "Invalid credentials"}

@router.post("/auth/sign-up", tags=["auth"])
async def sign_up(user: SignUp):
    encrpytedPassword(user.password)
    user = await prisma.user.create(
        {
            "email": user.email,
            "password": encrpytedPassword(user.password),
            "name": user.name,
        }
    )
    await prisma.profile.create({"userId": user.id})

    return {"success": True, "data": user}
 