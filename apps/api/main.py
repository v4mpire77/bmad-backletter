from fastapi import FastAPI

from .routers import auth

app = FastAPI()

app.include_router(auth.router)


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Hello, world!"}
