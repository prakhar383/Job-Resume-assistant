import os
import json
from dotenv import load_dotenv
from github import Github
from groq import Groq

load_dotenv()

class GitHubAgent:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.username = "prakhar383" # Using your username
        self.github = Github(self.token)

    def fetch_repositories(self):
        user = self.github.get_user(self.username)
        repos = user.get_repos()
        project_list = []

        for repo in repos:
            try:
                readme = repo.get_readme()
                readme_content = readme.decoded_content.decode("utf-8")
            except:
                readme_content = ""

            project = {
                "name": repo.name,
                "description": repo.description or "",
                "url": repo.html_url,
                "topics": repo.get_topics(),
                "language": repo.language or "",
                "readme": readme_content[:2000]  # limit size to save tokens
            }
            project_list.append(project)
        return project_list

    def run(self):
        print("📦 Fetching GitHub projects...")
        projects = self.fetch_repositories()
        print(f"✅ Found {len(projects)} repositories")
        return projects


class JDParserAgent:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        # LLaMA 3 8B is incredibly fast and cheap for data extraction
        self.model = "llama3-8b-8192" 

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
                temperature=0.1, # Low temperature forces consistent JSON
            )
            
            raw_content = response.choices[0].message.content.strip()
            
            # Clean up potential markdown blocks added by the LLM
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