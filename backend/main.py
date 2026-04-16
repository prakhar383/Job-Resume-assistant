import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import all our agents
from agents.github_agent import GitHubAgent
from agents.jd_parser_agent import JDParserAgent
from agents.project_selector_agent import ProjectSelectorAgent
from agents.score_checker_agent import ScoreCheckerAgent
from agents.resume_generator_agent import ResumeGeneratorAgent

app = FastAPI(title="AI Resume Generator API")

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # changed to accept requests from ANY origin (like a local HTML file)
    allow_credentials=False, # Must be False when allowing all origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class GenerateRequest(BaseModel):
    job_description: str

class TemplateRequest(BaseModel):
    content: str

@app.get("/")
def read_root():
    return {"status": "FastAPI Master Server is running."}

@app.post("/api/generate-resume")
def generate_resume(request: GenerateRequest):
    try:
        # 1. Parse Job Description
        jd_agent = JDParserAgent()
        parsed_jd = jd_agent.run(request.job_description)

        # 2. Fetch GitHub Projects
        github_agent = GitHubAgent()
        all_projects = github_agent.run()

        # 3. Select Top Projects
        selector_agent = ProjectSelectorAgent()
        selected_projects = selector_agent.run(parsed_jd, all_projects)

        # 4. Calculate ATS Score
        score_agent = ScoreCheckerAgent()
        ats_data = score_agent.run(parsed_jd, selected_projects)

        # 5. Generate LaTeX Code
        resume_agent = ResumeGeneratorAgent()
        final_latex = resume_agent.run(parsed_jd, selected_projects)

        print("🎉 Entire Pipeline Complete!")
        
        # We return the score data and the raw LaTeX string directly to the frontend
        return {
            "status": "success",
            "message": "Resume generated successfully",
            "ats_score": ats_data,
            "latex_code": final_latex
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Pipeline Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/update-template")
def update_template(request: TemplateRequest):
    try:
        content = request.content
        
        # 1. Verification logic
        if "{{DYNAMIC_OBJECTIVE_PLACEHOLDER}}" not in content:
            raise HTTPException(status_code=400, detail="Missing required placeholder: {{DYNAMIC_OBJECTIVE_PLACEHOLDER}}")
            
        if "{{DYNAMIC_PROJECTS_PLACEHOLDER}}" not in content:
            raise HTTPException(status_code=400, detail="Missing required placeholder: {{DYNAMIC_PROJECTS_PLACEHOLDER}}")
            
        # 2. Write logic
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(current_dir, "templates", "base_resume.tex")
        
        with open(template_path, "w", encoding="utf-8") as file:
            file.write(content)
            
        return {
            "status": "success",
            "message": "Template successfully updated."
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update template: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)