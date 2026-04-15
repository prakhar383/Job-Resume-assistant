import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class ScoreCheckerAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-8b-instant"

    def run(self, parsed_jd: dict, selected_projects: list) -> dict:
        print("📊 Calculating ATS Match Score...")
        
        prompt = f"""
        Act as an ATS (Applicant Tracking System). Evaluate how well the candidate's selected projects match the job requirements.
        
        Job Requirements:
        {json.dumps(parsed_jd, indent=2)}
        
        Candidate's Selected Projects:
        {json.dumps(selected_projects, indent=2)}
        
        Provide a match score out of 100 and brief feedback. Respond ONLY with a valid JSON object in this exact format:
        {{
            "score": 85,
            "feedback": "Strong match in Python and FastAPI, but missing explicit mentions of Docker.",
            "missing_keywords": ["Docker", "Kubernetes"]
        }}
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
                
            score_data = json.loads(raw_content)
            print(f"✅ ATS Score calculated: {score_data.get('score')}/100")
            return score_data
            
        except Exception as e:
            print(f"❌ Error calculating score: {e}")
            return {"score": 0, "feedback": "Error calculating score.", "missing_keywords": []}