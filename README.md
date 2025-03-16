# CramPlan

UNIHACK Hackathon Project - A personalized study assistant that generates customized study plans based on your understanding.

## Repository Structure

This repository is organized as a monorepo with Git submodules:

- **agent_backend**: Core backend services for the CramPlan platform
- **cramplan_frontend**: Frontend application (submodule)
- **cramplan_voice**: Voice interaction component (submodule)

To clone the repository with all submodules:

```bash
git clone --recurse-submodules https://github.com/yourusername/cramplan.git
# or if already cloned:
git submodule update --init --recursive
```

## Features

- **Topic Generation**: Generate study topics based on a subject
- **Quiz Generation**: Create quizzes to test your understanding
- **Understanding Evaluation**: Evaluate your understanding based on quiz responses
- **Content Generation**: Generate detailed study content based on your understanding
- **PDF Generation**: Export your study materials as beautifully formatted PDFs
- **Voice Interaction**: Interact with the platform using voice commands (in development)

## Project Structure

The project is divided into three main components:

### Backend (agent_backend)

The backend is built with FastAPI and provides the core functionality of the application:

- Topic generation using AI
- Quiz creation and evaluation
- Content generation based on understanding
- PDF generation and export

Key files:

- `api.py`: Main API endpoints
- `llm_main.py`: AI agents for different tasks
- `pdf_generator.py`: PDF generation utilities
- `env_setup.py`: Environment setup utilities

### Frontend (cramplan_frontend)

The frontend is built with Next.js and provides a user-friendly interface for interacting with the application:

- Home page for subject input
- Assessment page for quiz taking
- Study plan page for viewing generated content
- Upload page for importing existing materials

Key directories:

- `app/`: Main application pages
- `components/`: Reusable UI components
- `styles/`: CSS and styling
- `lib/`: Utility functions and API clients

### Voice Component (cramplan_voice)

The voice component is a separate module that enables voice interaction with the platform (currently in development):

- Voice command recognition
- Voice response generation
- Integration with the main application

## API Endpoints

The backend provides the following API endpoints:

- `/generate-topics`: Generate study topics based on a subject
- `/generate-quiz`: Generate a quiz based on topics
- `/evaluate-quiz`: Evaluate understanding based on quiz responses
- `/curate-topics`: Curate topics based on understanding
- `/generate-content`: Generate detailed study content
- `/complete-flow`: Run the complete flow from topic generation to content generation
- `/generate-pdf-from-content`: Generate a PDF from content
- `/generate-pdf-from-file`: Generate a PDF from a markdown file
- `/generate-pdf-from-text`: Generate a PDF from markdown text
- `/complete-flow-with-pdf`: Run the complete flow and return the result as a PDF
- `/health`: Health check endpoint

## PDF Generation

CramPlan supports exporting your study materials as PDF documents. This feature allows you to:

- Generate PDFs from content generated by the application
- Convert markdown files to PDFs
- Convert markdown text to PDFs
- Run a complete flow and get the result as a PDF

For detailed instructions on setting up and using the PDF generation functionality, see [PDF Generation Documentation](agent_backend/README_PDF.md).

## Getting Started

### Backend Setup

1. Clone the repository with submodules:
   ```bash
   git clone --recurse-submodules https://github.com/yourusername/cramplan.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```
4. Set up WeasyPrint for PDF generation (macOS):
   ```bash
   brew install pango libffi cairo pango gdk-pixbuf libxml2 libxslt
   source agent_backend/setup_weasyprint.sh
   ```
5. Run the backend:
   ```bash
   cd agent_backend
   uvicorn api:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd cramplan_frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   # or
   pnpm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   # or
   pnpm dev
   ```
4. Open [http://localhost:3000](http://localhost:3000) in your browser

### Voice Component Setup

The voice component is currently in development. More details will be provided in future updates.

## Dependencies

### Backend

- FastAPI
- OpenAI
- WeasyPrint (for PDF generation)
- Markdown
- Python-dotenv
- Uvicorn

### Frontend

- Next.js
- React
- Tailwind CSS
- Shadcn UI
- TypeScript

## License

MIT
