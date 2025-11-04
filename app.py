import numpy as np
import pandas as pd
import streamlit as st
import os
import src.data_scraper as scrape
from data_loader import load_players_df
from tree_adapter import TREE_AVAILABLE, build_tree_from_df, find_by_name
from frontend_utils import (
   clean_name, stat_tiles_single, build_single_table, build_compare_table, KEY_STATS
)
from compare_utils import prototype_recommendation
import src.data_scraper as scraper


if not os.path.isfile('data/player_stats.csv'):
   try:
       os.mkdir('data')
   except:
       pass
   scrape.download_data_file("data/",2025)
   scrape.html_to_csv("data/player_stats.html")


# Streamlit page setup
st.set_page_config(page_title="Fantasy Football Player Comparison", layout="wide")
st.title("Fantasy Football Player Comparison")
    
# Load data (from data/player_stats.csv)
try:
    df = load_players_df()
except Exception as e:
    st.error("Could not load player data.")
    st.exception(e)
    st.stop()

# Build team tree once
if TREE_AVAILABLE:
    build_tree_from_df(df)

# Sidebar filters + BFS/DFS toggle for tree search
st.sidebar.header("Filters & Search")
positions = sorted([p for p in df["Position"].dropna().unique().tolist() if str(p).strip()])
picked_positions = st.sidebar.multiselect(
    "Filter by Position",
    options=positions,
    default=positions if positions else [],
)
search_strategy = st.sidebar.radio(
    "Tree Search Strategy",
    options=["BFS","DFS"],
    index=0,
    help="Controls how the single-player search traverses the tree.",
)
# all_years = [2025 - i for i in range(50)]
search_year = st.sidebar.selectbox(
    "Year to search",
    options= [2025 - i for i in range(56)],
    index=0,
    help="Controls what year to search data",
)
if "last_year_option" not in st.session_state:
    st.session_state.last_year_option = search_year
    scraper.download_data_file("data/",search_year)
    scraper.html_to_csv("data/player_stats.html")
    df = load_players_df()
    build_tree_from_df(df)

# --- Only run expensive operation if radio changed ---
if search_year != st.session_state.last_year_option:
    scraper.download_data_file("data/",search_year)
    scraper.html_to_csv("data/player_stats.html")
    st.session_state.last_year_option = search_year
    df = load_players_df()
    build_tree_from_df(df)


# Filtered subset for UI pickers
filt = df if not picked_positions else df[df["Position"].isin(picked_positions)]
all_names = sorted(filt["Name"].dropna().unique().tolist())

# Single Player Lookup
st.subheader("Single Player Lookup")
picked_single = st.selectbox(
    "Search by name:",
    options=["— Select —"] + all_names,
    index=0,
    placeholder="Start typing a name...",
)

if picked_single and picked_single != "— Select —":
    data_single = None

    # Try tree (BFS/DFS) then fallback to DF exact match
    if TREE_AVAILABLE:
        data_single = find_by_name(picked_single, method=search_strategy)
    if data_single is None:
        row = df[df["Name"].str.lower() == picked_single.lower()]
        if not row.empty:
            data_single = row.iloc[0].to_dict()

    if data_single:
        st.markdown(
            f"**{clean_name(data_single.get('Name'))}** — {clean_name(data_single.get('Position'))} "
            f"({clean_name(data_single.get('Team'))})"
        )
        st.divider()
        stat_tiles_single(data_single)
        st.divider()
        st.subheader("All Stats")
        st.dataframe(build_single_table(data_single), width="stretch")
    else:
        st.warning("No data found for that player.")

st.divider()

# Compare Two Players
st.subheader("Compare Two Players")
c1, c2 = st.columns(2)
with c1:
    player_a = st.selectbox("Player A", options=["— Select —"] + all_names, index=0)
with c2:
    player_b = st.selectbox("Player B", options=["— Select —"] + all_names, index=0)

# Streamlit deprecation button
compare_clicked = st.button("Compare", type="primary", use_container_width=True)


# Full player table (filtered subset)
st.divider()
st.subheader("All Players")
cols_to_show = [c for c in [
    "Name","Position","Team","Games","FantasyPoints",
    "PassingYds","PassingTD","INT","RushingYds","RushingTD",
    "ReceivingYds","ReceivingTD","FantasyPointsPPR"
] if c in filt.columns]
st.dataframe(filt[cols_to_show], width="stretch")

if compare_clicked:
    issues = []
    if player_a == "— Select —": issues.append("Pick **Player A**.")
    if player_b == "— Select —": issues.append("Pick **Player B**.")
    if player_a == player_b and player_a != "— Select —": issues.append("Pick two *different* players.")
    if issues:
        st.error(" ".join(issues))
        st.stop()

    row_a = df[df["Name"].str.lower() == player_a.lower()]
    row_b = df[df["Name"].str.lower() == player_b.lower()]
    if row_a.empty or row_b.empty:
        st.error("Could not find one or both players.")
        st.stop()

    data_a = row_a.iloc[0].to_dict()
    data_b = row_b.iloc[0].to_dict()

    st.divider()
    st.subheader("Player Overview")
    oc1, _, oc3 = st.columns([1.2, 0.2, 1.2])
    with oc1:
        st.write(f"**{clean_name(data_a.get('Name'))}** — {clean_name(data_a.get('Position'))} ({clean_name(data_a.get('Team'))})")
        st.caption("Player A")
    with oc3:
        st.write(f"**{clean_name(data_b.get('Name'))}** — {clean_name(data_b.get('Position'))} ({clean_name(data_b.get('Team'))})")
        st.caption("Player B")

    st.divider()
    st.subheader("Key Stats")
    grid = st.columns(5)
    for i, (key, label) in enumerate(KEY_STATS):
        a_val = data_a.get(key, np.nan)
        b_val = data_b.get(key, np.nan)
        with grid[i % 5]:
            st.write(f"**{label}**")
            left, right = st.columns(2)
            left.metric("A", value="—" if pd.isna(a_val) else a_val)
            right.metric("B", value="—" if pd.isna(b_val) else b_val)

    st.divider()
    st.subheader("Detailed Comparison")
    comp = build_compare_table(data_a, data_b)
    st.dataframe(comp, width="stretch")

    st.divider()
    st.subheader("Recommendation: ")
    st.success(prototype_recommendation(player_a, player_b, data_a, data_b))
