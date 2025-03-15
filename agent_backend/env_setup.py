import os
from dotenv import load_dotenv
import logging
import platform

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """
    Load environment variables and set up OpenAI API key for both client and tracing.
    Also sets up WeasyPrint environment variables on macOS.
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
    
    # Set up WeasyPrint environment variables on macOS
    if platform.system() == "Darwin":  # macOS
        logger.info("Setting up WeasyPrint environment variables for macOS")
        
        # Set library paths for WeasyPrint dependencies
        os.environ["DYLD_LIBRARY_PATH"] = "/opt/homebrew/lib:" + os.environ.get("DYLD_LIBRARY_PATH", "")
        os.environ["PKG_CONFIG_PATH"] = "/opt/homebrew/lib/pkgconfig:/opt/homebrew/opt/libffi/lib/pkgconfig:/opt/homebrew/opt/libxml2/lib/pkgconfig:/opt/homebrew/opt/libxslt/lib/pkgconfig:" + os.environ.get("PKG_CONFIG_PATH", "")
        
        logger.info("WeasyPrint environment variables set")
    
    return True

# Run setup when this module is imported
setup_successful = setup_environment() 