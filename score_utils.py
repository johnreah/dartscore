"""
Score Utils Module

This module provides utility functions for working with dart scores.
"""

def is_valid_score(score: int) -> bool:
    match score:
        case _ if score < 0: return False
        case _ if score > 180: return False
        case 163 | 166 | 169 | 172 | 173 | 175 | 176 | 178 | 179: return False
    return True
