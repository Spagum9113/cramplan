import weasyprint
import tempfile
import os
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_weasyprint():
    """
    Test WeasyPrint functionality by generating a simple PDF.
    """
    try:
        logger.info("Testing WeasyPrint functionality...")
        
        # Simple HTML content
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>WeasyPrint Test</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 2cm;
                }
                h1 {
                    color: #2563eb;
                }
            </style>
        </head>
        <body>
            <h1>WeasyPrint Test</h1>
            <p>This is a test document to verify that WeasyPrint is working correctly.</p>
        </body>
        </html>
        """
        
        # Create a temporary HTML file
        with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as temp_html:
            temp_html.write(html_content.encode('utf-8'))
            temp_html_path = temp_html.name
        
        try:
            # Convert HTML to PDF
            logger.info(f"Converting HTML to PDF using WeasyPrint...")
            pdf_path = temp_html_path.replace('.html', '.pdf')
            
            # Get WeasyPrint version
            logger.info(f"WeasyPrint version: {weasyprint.__version__}")
            
            # Generate PDF
            pdf = weasyprint.HTML(filename=temp_html_path).write_pdf(pdf_path)
            
            logger.info(f"PDF successfully generated at: {pdf_path}")
            logger.info("WeasyPrint is working correctly!")
            
            return True
        finally:
            # Clean up the temporary HTML file
            if os.path.exists(temp_html_path):
                os.remove(temp_html_path)
    except Exception as e:
        logger.error(f"Error testing WeasyPrint: {str(e)}")
        return False

if __name__ == "__main__":
    # Source the environment variables if on macOS
    if sys.platform == "darwin":
        logger.info("Running on macOS, setting environment variables...")
        os.environ["DYLD_LIBRARY_PATH"] = "/opt/homebrew/lib:" + os.environ.get("DYLD_LIBRARY_PATH", "")
        os.environ["PKG_CONFIG_PATH"] = "/opt/homebrew/lib/pkgconfig:/opt/homebrew/opt/libffi/lib/pkgconfig:/opt/homebrew/opt/libxml2/lib/pkgconfig:/opt/homebrew/opt/libxslt/lib/pkgconfig:" + os.environ.get("PKG_CONFIG_PATH", "")
    
    success = test_weasyprint()
    
    if success:
        logger.info("Test completed successfully!")
        sys.exit(0)
    else:
        logger.error("Test failed!")
        logger.info("If you're on macOS, try running: source agent_backend/setup_weasyprint.sh")
        sys.exit(1) 