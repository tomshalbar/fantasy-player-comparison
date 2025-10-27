
import math
import numpy as np

# Recommendation heuristic based on FantasyPoints
def prototype_recommendation(player_a: str, player_b: str, a: dict, b: dict) -> str:
    """
    Recommend A or B based on season FantasyPoints.
    """
    a_pts = a.get("FantasyPoints", np.nan)
    b_pts = b.get("FantasyPoints", np.nan)
    if np.isnan(a_pts) and np.isnan(b_pts):
        return "No clear edge from current stats."
    if np.isnan(a_pts):
        return f"Start {player_b} (A missing FantasyPoints)."
    if np.isnan(b_pts):
        return f"Start {player_a} (B missing FantasyPoints)."
    if math.isclose(a_pts, b_pts, rel_tol=0.01, abs_tol=1.0):
        return f"It's close — slight lean to {player_a}."
    better = player_a if a_pts > b_pts else player_b
    return f"Start {better}: higher season FantasyPoints."
