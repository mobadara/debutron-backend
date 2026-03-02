from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Configuration settings for the application, including MongoDB connection details.
    
    This class uses Pydantic's BaseSettings to manage configuration values, which can be
    loaded from environment variables or a .env file. The settings include the MongoDB URI
    and the database name.
    
    Attributes:
        MONGODB_URI (str): The URI for connecting to the MongoDB instance.
        DATABASE_NAME (str): The name of the MongoDB database to use.
    """
    MONGODB_URI: str
    DATABASE_NAME: str
    
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    
settings = Settings()