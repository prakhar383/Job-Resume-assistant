# AI-Automated Resume Builder

An enterprise-grade, full-stack application designed to autonomously generate perfectly formatted, ATS-optimized LaTeX resumes. By leveraging highly capable Large Language Models alongside a scalable Fast API backend and a dynamic React frontend, the platform algorithmically aligns a candidate's GitHub portfolio with targeted job descriptions to maximize application success rates.

## System Architecture & Workflow

The orchestration pipeline consists of several specialized AI Agents working in concert:

1. **Job Description Extraction (`JDParserAgent`)**: Consumes the raw target job description, semantically analyzing it to extract absolute prerequisite skills, core domain knowledge, and exact tooling requirements into a structured JSON payload.
2. **Repository Aggregation (`GitHubAgent`)**: Interfaces with candidate public repositories, dynamically fetching tech stacks and project summarizations.
3. **Data Pruning (`ProjectSelectorAgent`)**: Algorithmically selects the top 3 optimal, highly-correlated projects from the candidate's repository dataset based upon the parsed JD parameters.
4. **ATS Pre-Calculation (`ScoreCheckerAgent`)**: Evaluates the overlap between the selected candidate data and the JD to provide a hard ATS projection score natively highlighting critical missing skills.
5. **LaTeX Compilation (`ResumeGeneratorAgent`)**: Instantiates a precise prompting matrix to generate hyper-compressed, highly-impactful 3-point formatting utilizing injected keywords ensuring optimal space utilization and ATS parsing success natively inside `.tex` formatted templates.

## Tech Stack Overview

### Backend Framework
- **Python / FastAPI**: Core routing and ultra-fast asynchronous data handling.
- **Groq API**: Lightning fast inferencing using state-of-the-art LLaMa models.
- **Pydantic**: Strict data validation and settings management.

### Frontend Framework
- **React / Vite**: Bleeding-edge local server handling and HMR.
- **Tailwind CSS (v4)**: Modern, highly responsive atomic styling system. 
- **Axios**: Promised-based HTTP client for API transactions.
- **Lucide-React**: Clean, unified iconography.

---

## Getting Started: Complete Installation Guide

Follow these comprehensive steps to download, install dependencies, and run the project locally on your machine.

### Prerequisites
Before beginning, ensure you have the following installed on your system:
- **[Git](https://git-scm.com/downloads)**: To clone the repository.
- **[Node.js (v18+)](https://nodejs.org/)**: To run the Vite React server.
- **[Python (v3.9+)](https://www.python.org/downloads/)**: To run the backend logic.
- **Groq API Key**: Obtain a free API key from the [Groq Cloud Console](https://console.groq.com/keys).

### 1. Clone the Repository
Open your preferred terminal configuration and clone the codebase:
```bash
git clone https://github.com/prakhar383/Job-Resume-assistant.git
cd Job-Resume-assistant
```

### 2. Configure the Backend (FastAPI + AI Pipeline)
Open a terminal and navigate into the `backend` directory to establish the isolated Python environment.

#### For Windows:
```cmd
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

#### For macOS / Linux:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

Next, create an environment variables file to safely house your API credentials.
1. Create a new file named `.env` inside the `backend` directory.
2. Add your Groq API key to the file exactly as follows:
   ```env
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

Start the backend server on port 8000. *(Note for Windows cmd users: If you run into UI emoji rendering errors, prepend the startup with the appropriate UTF-8 flag as seen below)*:
```cmd
# Windows CMD
set PYTHONIOENCODING=utf-8
python main.py

# PowerShell
$env:PYTHONIOENCODING="utf-8"
python main.py

# Mac / Linux
python main.py
```

### 3. Configure the Frontend (React + Vite)
Leave the backend terminal running. Open a **new** terminal window and navigate into the `frontend` directory to install the UI interface.

```bash
cd frontend
npm install
npm run dev
```

### 4. Application Usage
Once both servers are running successfully, your terminal will provide a localhost link (typically `http://localhost:5173/`).
1. Open your web browser and navigate precisely to **[http://localhost:5173/](http://localhost:5173/)**.
2. Input a target **GitHub Username**.
3. Paste the complete text of your desired **Job Description** into the designated text area.
4. *(Optional)* Use the **Template Configuration** box to paste your own custom LaTeX template. Ensuring it contains `{{DYNAMIC_OBJECTIVE_PLACEHOLDER}}` and `{{DYNAMIC_PROJECTS_PLACEHOLDER}}`, click **Update Template** to securely overwrite the backend configuration on the fly.
5. Click **Generate LaTeX Resume** to instantly trigger the multi-agent AI pipeline. It natively enforces strict 1-page constraints (e.g., max 2 lines per bullet, zero chat text) and returns your custom-tailored ATS resume code.

---
*Created dynamically to streamline rigorous technical job application workflows.*
