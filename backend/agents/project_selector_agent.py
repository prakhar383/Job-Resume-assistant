import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class ProjectSelectorAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-8b-instant"

    def run(self, parsed_jd: dict, github_projects: list) -> list:
        print("⚖️ Selecting the best projects for the JD...")
        
        prompt = f"""
        You are an expert technical recruiter. Your job is to select the top 3 most relevant projects from the candidate's portfolio that match the Job Description.
        
        Job Requirements:
        {json.dumps(parsed_jd, indent=2)}
        
        Candidate's GitHub Projects:
        {json.dumps(github_projects, indent=2)}
        
        Select exactly 3 projects. Respond ONLY with a valid JSON array of objects in this exact format, with no markdown formatting or extra text:
        [
            {{
                "name": "project_name",
                "reason": "Brief reason why it matches the JD",
                "readme_summary": "A 2-sentence summary of what the project does based on the readme"
            }}
        ]
        """

        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                temperature=0.1,
            )
            
            raw_content = response.choices[0].message.content.strip()
            
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:-3]
            elif raw_content.startswith("```"):
                raw_content = raw_content[3:-3]
                
            selected_projects = json.loads(raw_content)
            print("✅ Projects successfully selected!")
            return selected_projects
            
        except Exception as e:
            print(f"❌ Error selecting projects: {e}")
            return []