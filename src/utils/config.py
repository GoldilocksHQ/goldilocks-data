import os
from dotenv import load_dotenv
from src.config.path_config import LOG_FILE_PATH

# Load environment variables from .env file
load_dotenv()


class Config:
    """
    Manages configuration settings for the application.

    Loads environment variables from a .env file and provides them as
    attributes. It also validates the presence of essential variables.
    """

    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
    SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")

    # Neuron360
    NEURON360_API_KEY = os.getenv("NEURON360_API_KEY")
    NEURON360_API_URL = os.getenv("NEURON360_API_URL")

    # LLM Providers
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # LLM Config
    MAX_CONCURRENT_LLM_REQUESTS = int(os.getenv("MAX_CONCURRENT_LLM_REQUESTS", 25))
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.2))
    LLM_REQUEST_DELAY_SECONDS = float(os.getenv("LLM_REQUEST_DELAY_SECONDS", 0.1))

    # Application
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", LOG_FILE_PATH)
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "t")

    def __init__(self):
        """
        Initializes the configuration by loading and validating variables.
        """
        load_dotenv()

        # General
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.environment = os.getenv("ENVIRONMENT", "development")

        # Neuron360 API
        self.neuron360_api_key = os.getenv("NEURON360_API_KEY")
        self.neuron360_api_url = os.getenv("NEURON360_API_URL")

        # Validate that essential variables are set
        if not self.neuron360_api_key:
            raise ValueError(
                "NEURON360_API_KEY is not set in the environment variables."
            )
        if not self.neuron360_api_url:
            raise ValueError(
                "NEURON360_API_URL is not set in the environment variables."
            )


# Create a singleton instance for easy access across the application
config = Config()
