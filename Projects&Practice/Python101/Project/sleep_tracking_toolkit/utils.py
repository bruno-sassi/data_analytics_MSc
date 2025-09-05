# utils.py
# Implement the following functions:

# quality_label(score): converts a numeric score to a string label based on the following:
# 85 or more → 'Excellent'
# 70 to 84 → 'Good'
# 50 to 69 → 'Fair'
# below 50 → 'Poor'
# normalize_quality(score, current_max=100): normalizes a given score to a 0 - 100 scale using the formula:
# score / current_max * 100, rounded to two decimal places
# compute_sleep_score(duration, quality_score): computes a combined sleep score (0 - 100 scale) using the formula:
# score = min(duration / 8.0, 1.0) * 60 + quality_score * 0.4, capped at 100, rounded to two decimal places

def quality_label(score):
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Fair"
    else:
        return "Poor"

def normalize_quality(score):
    if not score:
        return []
    max_score = max(score)
    return [round(score / max_score * 100, 2) for score in score]

def compute_sleep_score(duration, quality_score):
    score = min(duration / 8.0, 1.0) * 60 + quality_score * 0.4
    return round(min(score, 100), 2)
