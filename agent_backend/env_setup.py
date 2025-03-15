import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """
    Load environment variables and set up OpenAI API key for both client and tracing.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        logger.warning("OPENAI_API_KEY not found in environment variables")
        return False
    
    # Explicitly set OPENAI_API_KEY as environment variable for tracing
    os.environ["OPENAI_API_KEY"] = openai_api_key
    logger.info("OPENAI_API_KEY set for tracing")
    
    return True

# Run setup when this module is imported
setup_successful = setup_environment() 