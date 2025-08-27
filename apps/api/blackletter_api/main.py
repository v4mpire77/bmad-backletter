from fastapi import FastAPI
from .routers import uploads, jobs, analyses, reports

app = FastAPI(title="Blackletter API", version="0.1.0")
app.include_router(uploads.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")
app.include_router(analyses.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
