import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class JDParserAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.1-8b-instant" 

    def run(self, job_description: str) -> dict:
        print("🔍 Parsing Job Description via Groq...")
        
        prompt = f"""
        You are an expert technical recruiter. Analyze the following job description and extract the core required skills, technologies, and concepts.
        
        Job Description:
        {job_description}
        
        Respond ONLY with a valid JSON object in this exact format, with no markdown formatting or extra text:
        {{
            "core_skills": ["skill1", "skill2"],
            "tools_and_frameworks": ["tool1", "tool2"],
            "domain_knowledge": ["concept1", "concept2"]
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
            
            parsed_jd = json.loads(raw_content)
            print("✅ JD successfully parsed!")
            return parsed_jd
            
        except Exception as e:
            print(f"❌ Error parsing JD: {e}")
            return {"core_skills": [], "tools_and_frameworks": [], "domain_knowledge": []}