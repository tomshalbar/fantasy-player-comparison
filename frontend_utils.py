
# UI helpers for building tiles and tables in Streamlit.

import numpy as np
import pandas as pd
import streamlit as st

#  List of key stats
KEY_STATS = [
    ("FantasyPoints", "Fantasy Pts"),
    ("Games", "Games"),
    ("PassingYds", "Pass Yds"),
    ("PassingTD", "Pass TD"),
    ("INT", "INT"),
    ("RushingYds", "Rush Yds"),
    ("RushingTD", "Rush TD"),
    ("ReceivingYds", "Recv Yds"),
    ("ReceivingTD", "Recv TD"),
    ("FantasyPointsPPR", "Fantasy Pts (PPR)")
]

# Safe display name helper
def clean_name(x):

    return x if pd.notna(x) and str(x).strip() else "—"

# Render metric tiles for a single player
def stat_tiles_single(a: dict):
    """
    Show key stat tiles for one player's dict
    """
    st.subheader("Key Stats")
    cols = st.columns(5)
    for i, (key, label) in enumerate(KEY_STATS):
        val = a.get(key, "—")
        with cols[i % 5]:
            st.write(f"**{label}**")
            st.metric("Value", value="—" if pd.isna(val) else val)

# Build a comparison DataFrame
def build_compare_table(a: dict, b: dict) -> pd.DataFrame:
    """
    Return a A-vs-B comparison table for numeric fields.
    """
    cols = sorted(set(a.keys()).union(b.keys()))
    rows = []

    def is_numeric_like(col_name: str) -> bool:
        c = col_name.lower()
        return any(k in c for k in [
            "yd","td","int","point","ppr","game","att","target","reception","rush","pass","recv"
        ])

    for c in cols:
        if c in ("Name","Position","Team"):
            continue
        if not is_numeric_like(c):
            continue
        av = a.get(c, np.nan)
        bv = b.get(c, np.nan)
        av = np.nan if av is None else av
        bv = np.nan if bv is None else bv
        diff = av - bv if (pd.notna(av) and pd.notna(bv)) else np.nan
        rows.append((c, av, bv, diff))

    df = pd.DataFrame(rows, columns=["Stat","Player A","Player B","Δ (A - B)"])

    priority = {"FantasyPoints": -2, "Games": -1}
    df["__order"] = df["Stat"].map(priority).fillna(0)
    df = df.sort_values(["__order","Stat"]).drop(columns="__order")
    return df

# Build a single-player table
def build_single_table(a: dict) -> pd.DataFrame:
    """
    Return a transposed sorted view of a single player's stats (Stat/Value).
    """
    hide = {"Name","Position","Team"}
    items = {k:v for k,v in a.items() if k not in hide}
    s = pd.Series(items, name=f"{a.get('Name','Player')}")
    df = s.to_frame()
    df.index.name = "Stat"
    df.columns = ["Value"]
    return df.sort_index()
