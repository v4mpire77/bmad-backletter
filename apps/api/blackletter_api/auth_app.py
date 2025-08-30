"""Minimal FastAPI app exposing only the auth routes.
Useful for lightweight testing and demos."""
from fastapi import FastAPI

from .routers import auth

app = FastAPI()
app.include_router(auth.router)
