import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import rules, analyses

app = FastAPI(title="Blackletter API", version="0.1.0")

# CORS configuration (allow frontends to call the API)
cors_origins = os.getenv("CORS_ORIGINS", "*")
if cors_origins == "*":
    allow_origins = ["*"]
else:
    allow_origins = [o.strip() for o in cors_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(rules.router, prefix="/api")
app.include_router(analyses.router, prefix="/api")


@app.get("/")
def read_root():
    return {"status": "ok"}


@app.get("/healthz")
def healthz():
    return {"ok": True}
