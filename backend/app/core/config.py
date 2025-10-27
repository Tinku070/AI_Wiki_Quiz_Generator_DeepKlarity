# backend/app/core/config.py (Modified)
from pydantic_settings import BaseSettings
import os

# Define the location of the .env file
# Ensure this correctly points to your .env file in the backend directory
# (Assuming your backend/.env file exists)
ENV_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", ".env")

class Settings(BaseSettings):
    # Core LLM Key
    GEMINI_API_KEY: str

    # Simplified Database Configuration
    # Use a single, comprehensive URL for the database connection
    # SQLite URL format: sqlite:///./<your_db_file_name>.db
    # You can set this default directly here for SQLite simplicity.
    DATABASE_URL: str = "sqlite:///./quiz_generator.db"

    # NOTE: You must remove or comment out the Pydantic fields that 
    # are failing: POSTGRES_USER, POSTGRES_PASSWORD, etc.

    class Config:
        env_file = ENV_FILE_PATH

# Now, initialize settings based on the updated class
settings = Settings()