import uvicorn
import logging
from env_setup import setup_successful

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Check if environment setup was successful
if not setup_successful:
    logger.error("Failed to set up environment variables. API may not function correctly.")

# Import the FastAPI app after environment setup
from api import app

if __name__ == "__main__":
    logger.info("Starting CramPlan API server")
    uvicorn.run(app, host="0.0.0.0", port=8000) 