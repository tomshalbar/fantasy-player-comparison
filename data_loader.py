
import os
import pandas as pd

DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "player_stats.csv")

# Normalize column labels
def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a copy of df with trimmed column names.
    """
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]
    return df

# Main loader
def load_players_df() -> pd.DataFrame:
    """
    Load the player's CSV produced by the scraper drop junk columns
    map snake_case to the UI's expected names and coerce numeric columns.
    """
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Missing CSV at {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)
    df = _normalize_columns(df)

    # Drop known junk columns if present
    for junk in ("Unnamed: 0", "..."):
        if junk in df.columns:
            df = df.drop(columns=[junk])

    # Map the scraper's snake_case to UI's columns
    rename_map = {
        "player": "Name",
        "fantpos": "Position",
        "tm": "Team",
        "games": "Games",
        "passing_yds": "PassingYds",
        "passing_td": "PassingTD",
        "passes_intercepted": "INT",
        "rushing_yds": "RushingYds",
        "rushing_td": "RushingTD",
        "receiving_yds": "ReceivingYds",
        "receiving_td": "ReceivingTD",
        "fantasy_points": "FantasyPoints",
        "fantasy_points_ppr_": "FantasyPointsPPR",
    }
    for src, dst in rename_map.items():
        if src in df.columns:
            df[dst] = df[src]

    # Ensure minimal text columns exist
    for need in ("Name", "Position", "Team"):
        if need not in df.columns:
            df[need] = ""

    # Coerce stats to numeric
    numeric_like = [
        "Games","PassingYds","PassingTD","INT","RushingYds","RushingTD",
        "ReceivingYds","ReceivingTD","FantasyPoints","FantasyPointsPPR"
    ]
    for c in numeric_like:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    return df
