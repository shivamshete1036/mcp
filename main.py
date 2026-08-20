import os
import requests

# Personal Access Token (PAT) should be set as an environment variable for security
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# Repository details
OWNER = "shivamshete1036"
REPO = "mcp"

def greet_owner():
    """Greet the repository owner."""
    print(f"Hello, {OWNER}! Welcome to the {REPO} repository.")

greet_owner()

def create_issue(title: str, body: str):
    """Create a new issue in the specified repository using the GitHub REST API."""
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    data = {"title": title, "body": body}
    response = requests.post(url, json=data, headers=headers)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Example: create a test issue
    issue = create_issue("Test issue from script", "This issue was created via the GitHub API using a PAT.")
    print(f"Issue created: {issue['html_url']}")
