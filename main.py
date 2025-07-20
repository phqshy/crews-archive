from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import discord, rmb

app = FastAPI()
app.include_router(discord.router)
app.include_router(rmb.router)

"""app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)"""


@app.get("/")
async def root():
    return {"message": "Hello World"}
