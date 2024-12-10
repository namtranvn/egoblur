from fastapi import FastAPI
from routers import blur_router

app = FastAPI(
    title="EgoBlur API",
    description="API for processing videos with EgoBlur",
    version="1.0.0"
)

# Include routers
app.include_router(blur_router.router, prefix="/v1")

@app.get("/health")
async def health_check():
    """
    Basic health check endpoint
    """
    return {"status": "healthy"}