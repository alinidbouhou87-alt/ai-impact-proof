"""AI impact calculation engine"""
from typing import Dict, Any

def calculate_impact(
    time_saved: float,
    quality_score: int,
    rework_hours: float,
    ai_cost: float,
    hourly_rate: float,
    confidence_score: float
) -> Dict[str, Any]:
    """
    Calculate AI impact metrics
    
    Args:
        time_saved: Hours saved by AI assistance
        quality_score: Quality score (0-100)
        rework_hours: Hours spent on rework
        ai_cost: Cost of AI tools ($)
        hourly_rate: Developer hourly rate ($)
        confidence_score: Confidence in measurements (0-100)
    
    Returns:
        Dictionary with impact metrics
    """
    # Calculate net time
    net_time = time_saved - rework_hours
    
    # Calculate monetary value
    saved_value = net_time * hourly_rate
    
    # Calculate net value
    net_value = saved_value - ai_cost
    
    # Calculate impact score
    # Based on time saved, quality, and confidence
    time_factor = min(time_saved / 10, 30)  # Max 30 points
    quality_factor = (quality_score / 100) * 40  # Max 40 points
    confidence_factor = (confidence_score / 100) * 30  # Max 30 points
    
    impact_score = time_factor + quality_factor + confidence_factor
    impact_score = min(max(impact_score, 0), 100)
    
    return {
        'time_saved': round(net_time, 2),
        'saved_value': round(saved_value, 2),
        'net_value': round(net_value, 2),
        'impact_score': round(impact_score, 1),
        'quality_score': quality_score,
        'roi': round((saved_value / ai_cost * 100) if ai_cost > 0 else 0, 1)
    }
