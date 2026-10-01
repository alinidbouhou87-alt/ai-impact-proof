"""Confidence score calculation engine"""
from typing import Dict, Any

def calculate_confidence(
    evidence_count: int,
    has_pr_reviews: bool,
    has_test_data: bool,
    has_baseline: bool
) -> Dict[str, Any]:
    """
    Calculate confidence level for AI impact assessment
    
    Args:
        evidence_count: Number of AI evidence items found
        has_pr_reviews: Whether repository has PR reviews
        has_test_data: Whether test data is available
        has_baseline: Whether baseline metrics exist
    
    Returns:
        Dictionary with confidence level and score
    """
    score = 0
    
    # Base score from evidence
    score += min(evidence_count * 10, 30)
    
    # Bonus for PR reviews
    if has_pr_reviews:
        score += 20
    
    # Bonus for test data
    if has_test_data:
        score += 20
    
    # Bonus for baseline
    if has_baseline:
        score += 30
    
    # Ensure score is within 0-100
    score = min(max(score, 0), 100)
    
    # Determine confidence level
    if score >= 80:
        level = "Very High"
    elif score >= 60:
        level = "High"
    elif score >= 40:
        level = "Medium"
    elif score >= 20:
        level = "Low"
    else:
        level = "Very Low"
    
    return {
        'score': score,
        'level': level
    }
