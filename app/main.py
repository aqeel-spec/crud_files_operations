# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import create_db_and_tables
# temp
from app.routers import media
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# The first part of the function, before the yield, will
# be executed before the application starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    print("Tables created")
    yield

# Correctly create the FastAPI app with the lifespan and other settings
app = FastAPI(
    lifespan=lifespan,
    title="Media Upload API",
    version="0.0.1",
    # servers=[
    #     {
    #         "url": "http://localhost:8000",  # ADD NGROK URL Here Before Creating GPT Action
    #         "description": "Development Server",
    #     }
    # ],
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)



app.include_router(media.router, prefix="/api/v1", tags=["Upload files"])

# Mount the 'media' directory to serve static files
app.mount("/media", StaticFiles(directory="media"), name="media")

@app.get("/")
def root() -> dict:
    return {"Message": "Welcome to CDN App"}