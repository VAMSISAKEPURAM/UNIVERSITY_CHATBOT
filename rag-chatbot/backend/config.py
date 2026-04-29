import os
from pathlib import Path
from dotenv import load_dotenv

# Define the root directory (where .env is located)
BASE_DIR = Path(__file__).resolve().parent.parent
DOTENV_PATH = BASE_DIR / ".env"

# Check if .env file exists and issue a warning if not
if not DOTENV_PATH.exists():
    print(f"Warning: .env file not found at {DOTENV_PATH}")

# Load environment variables from .env
load_dotenv(dotenv_path=DOTENV_PATH)

# Read the API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Validate existence of essential keys
if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not found. Please set it in .env file")

if not GROQ_API_KEY:
    raise EnvironmentError("GROQ_API_KEY not found. Please set it in .env file")

# Success indicator
print("API Keys (OpenAI & Groq) Loaded Successfully")

# You can export any configuration variables here for use in other files
class Config:
    OPENAI_API_KEY = OPENAI_API_KEY
    GROQ_API_KEY = GROQ_API_KEY
    BASE_PATH = BASE_DIR
