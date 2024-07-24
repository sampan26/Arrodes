import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routers import router
from app.lib.prisma import prisma


app = FastAPI(
    title="Arrodes",
    description="Bring a brain to your product",
    version="0.0.1",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Total request time: {process_time} secs")
    return response

@app.on_event("startup")
async def startup():
    # print("=====================================================================================================================")
    # print("=====================================================================================================================")
    # print("=====================================================================================================================")
    # import os
    # print("Database URL:", os.getenv("DATABASE_URL"))
    prisma.connect()
    # try:
    #     # Attempt to query the database
    #     result = await prisma.user.count()
    #     print(f"Database connection successful. User count: {result}")
    # except Exception as e:
    #     print(f"Database connection failed: {str(e)}")
    #     # Optionally, you might want to exit the application here
    #     # import sys
    #     # sys.exit(1)


@app.on_event("shutdown")
async def shutdown():
    prisma.disconnect()

app.include_router(router)