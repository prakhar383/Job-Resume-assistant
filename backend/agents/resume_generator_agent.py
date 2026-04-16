import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class ResumeGeneratorAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile" 
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.template_path = os.path.join(current_dir, "..", "templates", "base_resume.tex")

    def _load_template(self) -> str:
        try:
            with open(self.template_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            print(f"❌ Error: Could not find template at {self.template_path}")
            return ""

    def run(self, parsed_jd: dict, selected_projects: list) -> str:
        print("📝 Generating dynamic Objective and optimized LaTeX projects...")
        
        base_latex = self._load_template()
        if not base_latex:
            return "Error: Base LaTeX template missing."
            
        # PROMPT 1: Generate the Objective
        objective_prompt = f"""
        Write a highly professional resume objective specifically tailored to this job description:
        {parsed_jd}
        
        CRITICAL RULES:
        1. Maximum of 2 sentences. It must be highly concise and action-oriented.
        2. NO CHATTER. Output ONLY the raw objective text. 
        3. Do not use quotes, bolding, markdown formatting blocks, or introductory phrases.
        """

        # PROMPT 2: Generate the Projects
        project_prompt = f"""
        You are an expert technical resume writer. Write LaTeX formatting for the following projects to maximize ATS matching for this job description.
        
        Job Requirements: {parsed_jd}
        Selected Projects Data (USE THESE EXACT URLS): {selected_projects}
        
        CRITICAL RULES for Writing Project Bullet Points:
        1. NO PARAGRAPHS. You MUST explain the project using EXACTLY TWO (2) bullet points per project. NEVER 3 or more.
        2. BE EXTREMELY SPACE EFFICIENT. Each bullet point must be a maximum of 1-2 lines long. Keep it highly concise and action-oriented.
        3. KEYWORD INJECTION: You MUST naturally integrate the specific tools, core skills, and domain knowledge from the Job Requirements exactly as they appear in the parsed JSON. This is critical for ATS selection.
        4. Do not output any more projects than the ones provided in the Selected Projects Data. Only output the provided projects (maximum 3).
        5. You MUST extract the exact GitHub URL from the provided data for each project. DO NOT use 'your-username' or placeholders.
        6. NO CHATTER. You must output ONLY raw LaTeX code. You must never output conversational text, markdown formatting blocks (like ```latex), or introductory phrases. Start immediately with \\resumeProjectHeading.
        
        Output exact structure for each project:
        \\resumeProjectHeading
          {{\\href{{[EXACT_GITHUB_URL]}}{{\\textbf{{[PROJECT_NAME]}}}} $|$ \\emph{{[TECH_STACK]}}}}{{[YEAR/MONTH]}}
          \\resumeItemListStart
            \\resumeItem{{[Highly concise, action-oriented bullet point 1 integrating ATS keywords (max 1-2 lines)]}}
            \\resumeItem{{[Highly concise, action-oriented bullet point 2 demonstrating impact/result (max 1-2 lines)]}}
          \\resumeItemListEnd
        """

        try:
            # Generate Objective
            obj_response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": objective_prompt}],
                model=self.model,
                temperature=0.2,
            )
            dynamic_objective = obj_response.choices[0].message.content.strip()

            # Generate Projects
            proj_response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": project_prompt}],
                model=self.model,
                temperature=0.2,
            )
            project_latex = proj_response.choices[0].message.content.strip()
            
            # Clean markdown if present
            if project_latex.startswith("```latex"):
                project_latex = project_latex[8:-3]
            elif project_latex.startswith("```"):
                project_latex = project_latex[3:-3]
                
            # Inject both into base template
            final_resume = base_latex.replace("{{DYNAMIC_OBJECTIVE_PLACEHOLDER}}", dynamic_objective)
            final_resume = final_resume.replace("{{DYNAMIC_PROJECTS_PLACEHOLDER}}", project_latex)
            
            print("✅ Final LaTeX Resume generated with custom objective!")
            return final_resume
            
        except Exception as e:
            print(f"❌ Error generating resume: {e}")
            return base_latex