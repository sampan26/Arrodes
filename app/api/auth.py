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