# AI-Automated Resume Maker

A powerful full-stack application that leverages Large Language Models (LLMs) to automatically construct ATS-optimized resumes in LaTeX format. By intelligently analyzing a candidate's GitHub projects and a target Job Description, it dynamically matches required skills and outputs concise, high-impact bullet points to maximize selection rates.

## Features
- **Smart JD Parsing:** Extracts core skills, tools, and domain knowledge required from the Job Description.
- **GitHub Integration:** Scrapes and selects the top 3 most relevant projects from a candidate's GitHub profile.
- **ATS Match Analysis:** Provides a score out of 100 with actionable feedback on missing keywords.
- **LaTeX Generation:** Generates raw, customizable LaTeX code with highly space-efficient, precisely targeted bullet points.
- **Modern UI:** Built with Vite and React, styled gracefully with Tailwind CSS.

## Tech Stack
- **Backend:** Python, FastAPI, Groq API (LLaMa Models)
- **Frontend:** React, Vite, Tailwind CSS, Lucide React

## Getting Started

### Prerequisites
- Node.js installed
- Python 3.9+ installed
- A valid Groq API Key

### Backend Setup
1. Navigate to the `backend` directory: `cd backend`
2. Create and activate a virtual environment: `python -m venv venv` and `.\venv\Scripts\activate`
3. Install dependencies (requires fastapi, uvicorn, groq, pydantic, python-dotenv).
4. Create a `.env` file and add your target API key: `GROQ_API_KEY=your_key_here`
5. Run the server: `python main.py`

### Frontend Setup
1. Navigate to the `frontend` directory: `cd frontend`
2. Install dependencies: `npm install`
3. Run the development server: `npm run dev`
4. Visit `http://localhost:5173` in your browser.
