from fastapi import FastAPI

from routers import discord, rmb

app = FastAPI()
app.include_router(discord.router)
app.include_router(rmb.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
