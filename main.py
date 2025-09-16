from fastapi import FastAPI
from .config import API_TITLE
from .database import init_db, close_db
from .auth.routes import router as auth_router
from .employees.routes import router as employees_router

# Create FastAPI app
app = FastAPI(title=API_TITLE)

# Include routers
app.include_router(auth_router)
app.include_router(employees_router)


@app.get("/")
def root_path():
    """Root endpoint"""
    return {"hello": "world"}


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.on_event("shutdown")
async def shutdown_event():
    await close_db()
