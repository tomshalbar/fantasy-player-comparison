import math
import numpy as np

def calculate_trade_value(stats: dict) -> float:
    """
    Calculate a player's trade value based on multiple factors.
    Returns np.nan if essential stats are missing.
    """
    points = stats.get("FantasyPoints", np.nan)
    games = stats.get("Games", np.nan)
    position = stats.get("Position", "")
    
    if np.isnan(points) or np.isnan(games) or not position:
        return np.nan
        
    # Calculate points per game
    if games > 0:
        ppg = points / games
    else:
        ppg = 0
    
    # Position scarcity multiplier
    pos_multiplier = {
        # QBs are usually easier to replace
        "QB": 1.0,  
        # RBs are scarce and valuable
        "RB": 1.3,  
        # WRs are valuable but more abundant than RBs
        "WR": 1.2,  
        # TEs are very scarce at top tier
        "TE": 1.4   
    }.get(position, 1.0)
    
    # Calculate trade value
    # Games played factor helps value reliability
    trade_value = ppg * pos_multiplier * math.sqrt(games)  
    
    return trade_value

def prototype_recommendation(player_a: str, player_b: str, a: dict, b: dict) -> str:
    """
    Recommend which player has better trade value based on multiple factors.
    """
    a_value = calculate_trade_value(a)
    b_value = calculate_trade_value(b)
    
    if np.isnan(a_value) and np.isnan(b_value):
        return "No clear edge - insufficient stats for both players."
    if np.isnan(a_value):
        return f"{player_b} has better trade value (insufficient stats for {player_a})."
    if np.isnan(b_value):
        return f"{player_a} has better trade value (insufficient stats for {player_b})."
        
    # Calculate the percentage difference
    pct_diff = abs(a_value - b_value) / max(a_value, b_value) * 100
    
    # If values are within 5% of each other
    if pct_diff < 5:
        if a_value > b_value:
            player_with_edge = player_a
        else:
            player_with_edge = player_b
        return f"Trade values are very close: slight edge to {player_with_edge}."
    
    if a_value > b_value:
        better = player_a
    else:
        better = player_b

    if a_value > b_value:
        worse = player_b
    else:
        worse = player_a

    value_diff = round(pct_diff, 1)
    
    return f"{better} has {value_diff}% better trade value than {worse}."
