from pathlib import Path
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Database configurations
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./supply_chain.db")

# Blockchain configurations
BLOCKCHAIN_NETWORK = os.getenv("BLOCKCHAIN_NETWORK", "http://localhost:8545")
SMART_CONTRACT_ADDRESS = os.getenv("SMART_CONTRACT_ADDRESS", "")
CHAIN_ID = int(os.getenv("CHAIN_ID", "1"))

# AI Model configurations
MODEL_PATH = os.path.join(BASE_DIR, "models")
PREDICTION_THRESHOLD = 0.8
TRAINING_DATA_PATH = os.path.join(BASE_DIR, "data", "training")

# API configurations
API_V1_PREFIX = "/api/v1"
PROJECT_NAME = "AI-Blockchain Supply Chain Management"
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
API_PORT = int(os.getenv("API_PORT", "8000"))

# Security configurations
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Logging configurations
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
