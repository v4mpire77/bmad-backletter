from fastapi import FastAPI

from .routers import jobs, uploads

app = FastAPI()

app.include_router(uploads.router, prefix="/v1")
app.include_router(jobs.router, prefix="/v1")


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Hello, world!"}
