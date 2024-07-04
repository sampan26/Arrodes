import json

from fastapi import APIRouter, HTTPException, status  

from app.lib.auth.prisma import (
    encryptPassword,
    signJWT,
    validatePassword
)
from app.lib.prisma import prisma
from app.lib.models.auth import SignIn, SignInOut, SignUp


router = APIRouter()

@router.post("/auth/sign-in")
async def sign_in(signIn: SignIn):
    user = prisma.user.find_first(
        where={
            "email": signIn.email,
        },
        include={"profile": True}
    )
    if user:
        validated = validatePassword(signIn.password, user.password)
        del user.password

        if validated:
            token = signJWT(user.id)
            return {"success": True, "data": SignInOut(token=token, user=user)}
    
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid credentials"
        )

@router.post("/auth/sign-up")
async def sign_up(body: SignUp):
    encryptPassword(body.password)
    body = prisma.user.create(
        {
            "email": body.email,
            "password": encryptPassword(body.password),
            "name": body.name,
        }
    )
    prisma.profile.create(
        {"userId": body.id, "metadata": json.dump(body.metadata)}
    )

    if body:
        return {"success": True, "data": body}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid credentials"
    )