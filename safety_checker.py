"""Safety and security checker for sensitive information"""
from typing import Dict, Any, List
import re

# Patterns for potentially sensitive information
SENSITIVE_PATTERNS = {
    'api_key': r'(?i)(api[_-]?key|apikey)\s*[=:]\s*[\'\"]?[a-zA-Z0-9]{20,}',
    'password': r'(?i)(password|passwd|pwd)\s*[=:]\s*[^\s]+',
    'token': r'(?i)(token|auth[_-]?token)\s*[=:]\s*[a-zA-Z0-9_\-]{20,}',
    'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
    'aws_key': r'AKIA[0-9A-Z]{16}',
    'private_key': r'-----BEGIN (RSA|PRIVATE|EC).*?KEY-----'
}

def safety_report(text: str) -> Dict[str, Any]:
    """
    Analyze text for potentially sensitive information
    
    Args:
        text: Text content to analyze (commits, PRs, etc.)
    
    Returns:
        Dictionary with safety score and findings
    """
    findings: List[str] = []
    
    for pattern_name, pattern in SENSITIVE_PATTERNS.items():
        matches = re.findall(pattern, text, re.MULTILINE | re.DOTALL)
        if matches:
            findings.append(
                f"Potential {pattern_name.replace('_', ' ').title()} detected"
            )
    
    # Calculate safety score (100 = no issues, 0 = many issues)
    safety_score = max(0, 100 - (len(findings) * 15))
    
    return {
        'score': safety_score,
        'findings': findings
    }
