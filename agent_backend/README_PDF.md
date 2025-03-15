# PDF Generation in CramPlan

This document provides instructions for setting up and using the PDF generation functionality in CramPlan.

## Prerequisites

WeasyPrint requires several system dependencies to function properly. The installation process varies depending on your operating system.

### macOS

On macOS, you need to install the required dependencies using Homebrew:

```bash
brew install pango libffi cairo pango gdk-pixbuf libxml2 libxslt
```

After installing the dependencies, you need to set up the environment variables:

```bash
source agent_backend/setup_weasyprint.sh
```

This script sets the necessary environment variables for WeasyPrint to find the required libraries.

### Linux

On Debian/Ubuntu:

```bash
apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

On Fedora:

```bash
dnf install redhat-rpm-config python-devel python-pip python-setuptools python-wheel python-cffi libffi-devel cairo pango gdk-pixbuf2
```

### Windows

On Windows, the installation is more complex. Please refer to the official WeasyPrint documentation:
[WeasyPrint Installation on Windows](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows)

## Testing the Installation

To test if WeasyPrint is working correctly, run:

```bash
python agent_backend/test_weasyprint.py
```

If the test is successful, you should see a message indicating that WeasyPrint is working correctly, and a PDF file will be generated in a temporary directory.

## API Endpoints for PDF Generation

CramPlan provides several endpoints for generating PDFs:

1. `/generate-pdf-from-content` - Generates a PDF from a ContentResponse object
2. `/generate-pdf-from-file` - Generates a PDF from an uploaded markdown file
3. `/generate-pdf-from-text` - Generates a PDF from markdown text
4. `/complete-flow-with-pdf` - Runs the complete flow and returns the result as a PDF

### Example Usage

#### Generate PDF from Content

```python
import requests
import json

url = "http://localhost:8000/generate-pdf-from-content"
data = {
    "topic": [
        {
            "topic_title": "Introduction to Python",
            "main_description": "Python is a high-level programming language...",
            "subtopics": [
                {
                    "sub_topic_title": "Python Syntax",
                    "sub_content_text": "Python syntax is designed to be readable and simple..."
                }
            ]
        }
    ]
}
headers = {"Content-Type": "application/json"}

response = requests.post(url, data=json.dumps(data), headers=headers)

# Save the PDF
with open("study_plan.pdf", "wb") as f:
    f.write(response.content)
```

#### Generate PDF from Markdown File

```python
import requests

url = "http://localhost:8000/generate-pdf-from-file"
files = {"markdown_file": ("study_notes.md", open("study_notes.md", "rb"), "text/markdown")}
params = {"title": "My Study Notes"}

response = requests.post(url, files=files, params=params)

# Save the PDF
with open("study_notes.pdf", "wb") as f:
    f.write(response.content)
```

## Troubleshooting

If you encounter issues with PDF generation, check the following:

1. Make sure all dependencies are installed correctly
2. Ensure environment variables are set properly (especially on macOS)
3. Check the application logs for specific error messages
4. Try running the test script to verify WeasyPrint functionality

For macOS users, if you see an error about missing libraries, run:

```bash
source agent_backend/setup_weasyprint.sh
```

For more detailed troubleshooting, refer to the WeasyPrint documentation:
[WeasyPrint Troubleshooting](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#troubleshooting) 