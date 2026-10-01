"""AI evidence detection engine"""
from typing import List, Dict, Any
import re

AI_KEYWORDS = [
    'copilot', 'github copilot', 'ai', 'artificial intelligence',
    'gpt', 'openai', 'claude', 'llm', 'machine learning',
    'generated', 'auto-generated', 'ai-generated',
    'ai assisted', 'ai-powered', 'llm assisted'
]

def analyze_repository(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Analyze repository data for AI evidence
    
    Args:
        data: Repository data from get_repo_data()
    
    Returns:
        List of evidence items found
    """
    evidence = []
    
    # Analyze commits
    for commit in data.get('commits', []):
        message = commit.get('commit', {}).get('message', '').lower()
        if any(keyword in message for keyword in AI_KEYWORDS):
            evidence.append({
                'type': 'Commit',
                'title': commit.get('commit', {}).get('message', 'Unknown commit').split('\n')[0],
                'confidence': 'High',
                'source': 'Commit message'
            })
    
    # Analyze pull requests
    for pr in data.get('pull_requests', []):
        title = pr.get('title', '').lower()
        body = pr.get('body', '').lower()
        
        combined_text = title + ' ' + body
        
        if any(keyword in combined_text for keyword in AI_KEYWORDS):
            evidence.append({
                'type': 'Pull Request',
                'title': pr.get('title', 'Unknown PR'),
                'confidence': 'High',
                'source': f"PR #{pr.get('number', 'N/A')}"
            })
    
    return evidence
