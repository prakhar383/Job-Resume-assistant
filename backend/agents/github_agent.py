import os
from dotenv import load_dotenv
from github import Github

load_dotenv()

class GitHubAgent:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.username = "prakhar383" 
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
                "readme": readme_content[:2000]  
            }
            project_list.append(project)
        return project_list

    def run(self):
        print("📦 Fetching GitHub projects...")
        projects = self.fetch_repositories()
        print(f"✅ Found {len(projects)} repositories")
        return projects