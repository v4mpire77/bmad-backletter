from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.routers import contracts, compliance, research

app = FastAPI(
    title="Blackletter Systems API",
    description="API for legal document analysis and compliance checking",
    version="0.1.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(contracts.router, prefix="/contracts", tags=["contracts"])
app.include_router(compliance.router, prefix="/compliance", tags=["compliance"])
app.include_router(research.router, prefix="/research", tags=["research"])

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)