import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# Neuron360 Configuration
NEURON360_API_KEY = os.getenv("NEURON360_API_KEY")
NEURON360_BASE_URL = os.getenv("NEURON360_BASE_URL", "https://api.neuron360.io/v1")

# LLM Configuration
LLM_VENDOR = os.getenv("LLM_VENDOR", "gemini").lower() # "gemini" or "deepseek"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash-latest")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_MODEL_NAME = os.getenv("DEEPSEEK_MODEL_NAME", "deepseek-chat")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")

# Concurrency and Rate Limiting Configuration
try:
    MAX_CONCURRENT_LLM_REQUESTS = int(os.getenv("MAX_CONCURRENT_LLM_REQUESTS", "5"))
except ValueError:
    MAX_CONCURRENT_LLM_REQUESTS = 5
    print("Warning: MAX_CONCURRENT_LLM_REQUESTS in .env is not a valid integer. Defaulting to 5.")

try:
    LLM_REQUEST_DELAY_SECONDS = float(os.getenv("LLM_REQUEST_DELAY_SECONDS", "0.1"))
except ValueError:
    LLM_REQUEST_DELAY_SECONDS = 0.1
    print("Warning: LLM_REQUEST_DELAY_SECONDS in .env is not a valid float. Defaulting to 0.1.")

# Validate essential configurations
if not NEURON360_API_KEY:
    raise ValueError("NEURON360_API_KEY not found in .env file or environment variables.")

if LLM_VENDOR == "gemini" and not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found for the selected 'gemini' LLM vendor.")
elif LLM_VENDOR == "deepseek" and not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY not found for the selected 'deepseek' LLM vendor.") 