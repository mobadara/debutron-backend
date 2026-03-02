from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from contextlib import asynccontextmanager

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from .core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Define the lifespan of the application, including startup and shutdown events.
    
    This function is responsible for initializing the MongoDB connection and Beanie ODM on startup,
    and closing the MongoDB connection on shutdown.
    
    Args:
        app (FastAPI): The FastAPI application instance.
        
    Yields:
        None: This function does not yield any value,
        but it allows for setup and teardown logic to be executed around the lifespan of the application.
    """
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.DATABASE_NAME]
    
    await init_beanie(
        database=db,  # type: ignore
        document_models=[
            # Students
        ]
    )
    logging.info('System Boot: Connected to MongoDB and initialize Beanie')
    
    yield
    
    client.close()
    logging.info('System Shutdown: MongoDB connection closed')
    
    
app = FastAPI(
    title='Debutron Lab API',
    description='Enterprise backend for the Debutron LMS, CMS, and CBT and Admin system.',
    version='1.0.0',
    lifespan=lifespan
)

origins = [
    'https://localhost:3000',
    'http://localhost:5173',
    'https://debutron.org',
    'https://www.debutron.org',
    'https://debutron.vercel.app'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True
)

@app.get('/')
async def root():
    """Root endpoint of the API.
    
    This endpoint serves as a health check and provides a welcome message to indicate that the API is running.
    
    Returns:
        dict: A JSON response containing a welcome message.
    """
    return {'status': 'online', 'message': 'Debutron Lab API is working'}
