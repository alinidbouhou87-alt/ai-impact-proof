"""GitHub data collection module"""
import requests
from typing import Dict, Any, Optional

def get_repo_data(repo_url: str, github_token: Optional[str] = None) -> Dict[str, Any]:
    """
    Fetch repository data from GitHub API
    
    Args:
        repo_url: GitHub repository URL (https://github.com/owner/repo)
        github_token: Optional GitHub personal access token
    
    Returns:
        Dictionary containing repository data, commits, and pull requests
    """
    # Parse repo URL
    parts = repo_url.strip('/').split('/')
    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL")
    
    owner = parts[-2]
    repo = parts[-1]
    
    headers = {}
    if github_token:
        headers['Authorization'] = f'token {github_token}'
    
    try:
        # Get repository info
        repo_response = requests.get(
            f'https://api.github.com/repos/{owner}/{repo}',
            headers=headers,
            timeout=10
        )
        repo_response.raise_for_status()
        repository = repo_response.json()
        
        # Get commits
        commits_response = requests.get(
            f'https://api.github.com/repos/{owner}/{repo}/commits',
            headers=headers,
            params={'per_page': 100},
            timeout=10
        )
        commits_response.raise_for_status()
        commits = commits_response.json()
        
        # Get pull requests
        prs_response = requests.get(
            f'https://api.github.com/repos/{owner}/{repo}/pulls',
            headers=headers,
            params={'state': 'all', 'per_page': 100},
            timeout=10
        )
        prs_response.raise_for_status()
        pull_requests = prs_response.json()
        
        return {
            'repository': repository,
            'commits': commits,
            'pull_requests': pull_requests
        }
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch GitHub data: {str(e)}")
