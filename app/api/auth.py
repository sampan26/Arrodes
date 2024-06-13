from fastapi import APIRouter, HTTPException, status  

from app.lib.auth.prisma import (
    encrpytedPassword,
    signJWT,
    validatePassword
)
from app.lib.prisma import prisma
from app.lib.models.auth import SignIn, SignInOut, SignUp


router = APIRouter()

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
        token = signJWT(user.id)
        return {"success": True, "data": SignInOut(token=token, user=user)}
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid credentials"
    )

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

    if user:
        return {"success": True, "data": user}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid credentials"
    )