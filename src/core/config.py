from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
from pydantic import ConfigDict

load_dotenv()


class Settings(BaseSettings):
    '''
    Application configuration settings loaded from environment variables.

    Attributes:
        - PROJECT_NAME: Name of the project
        - DATABASE_URL: Database connection URL
        - JWT_SECRET: Secret key for JWT token generation and verification
        - JWT_ALGORITHM: Algorithm used for JWT encoding/decoding
        - ACCESS_TOKEN_EXPIRE_MINUTES: Expiration time for access tokens in minutes
        - SERVER_HOST: Host address for the server
        - SERVER_PORT: Port number for the server
    '''
    PROJECT_NAME: str = "fastapi-blog"
    DATABASE_URL: str = os.getenv("DATABASE_URL_LOCAL")
    JWT_SECRET: str = os.getenv('JWT_SECRET_LOCAL')  
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 3000

    model_config = ConfigDict(
        env_file=".env", 
        extra="allow")

    # class Config: 
    #     env_file = ".env"

settings = Settings()

