
import pandas as pd

# Attempt to import classes
try:
    from src.tree import Tree, Tree_node
    TREE_AVAILABLE = True
except Exception:
    # Tree, Tree_node = None, None
    # TREE_AVAILABLE = False
    raise("could not find tree decleration")

# Global tree instance
_tree = None

# Build a CSV line
def _line_for_node(row: dict) -> str:
    """
    Return a CSV string matching Tree_node.labels order.
    """
    alias = {
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
    vals = []
    for lab in Tree_node.labels:
        if lab in row:
            v = row.get(lab, "")
        else:
            v = row.get(alias.get(lab, ""), "")
        vals.append("" if pd.isna(v) else str(v))
    return ",".join(vals)

# Insert into BST comparing by the 'player' field only
def _safe_insert_by_player(t : Tree, root: Tree_node, data_str: str):
    """
    Insert a node into tree comparing on 'player'
    """
    p_idx = Tree_node.labels.index("player")
    new_player = data_str.split(",")[p_idx]
    if t.root is None:
        t.root = Tree_node(data_str)
        return
    cur = t.root
    while True:
        cur_player = cur.player
        if new_player < cur_player:
            if cur.left is None:
                cur.left = Tree_node(data_str)
                return
            cur = cur.left
        else:
            if cur.right is None:
                cur.right = Tree_node(data_str)
                return
            cur = cur.right

# Build tree once from a DataFrame
def build_tree_from_df(df: pd.DataFrame):
    """
    Build and cache Tree using safe insert that compares player names.
    """
    global _tree
    if not TREE_AVAILABLE:
        return None
    t = Tree()
    for _, r in df.iterrows():
        line = _line_for_node(r.to_dict())
        if t.root is None:
            t.root = Tree_node(line)
        else:
            _safe_insert_by_player(t, t.root, line)
    _tree = t
    return t

# Convert a Tree_node to a dict with UI-friendly keys
def _node_to_ui_dict(node: "Tree_node") -> dict:
    """
    Return a dict of all original labels plus UI keys (Name, Position,...)
    with numeric fields coerced to numbers.
    """
    out = {}
    for lab in Tree_node.labels:
        out[lab] = getattr(node, lab, "")

    # Friendly keys used by the UI
    def num(x): return pd.to_numeric(x, errors="coerce")
    out["Name"] = out.get("player", "")
    out["Position"] = out.get("fantpos", "")
    out["Team"] = out.get("tm", "")
    out["Games"] = num(out.get("games", ""))
    out["PassingYds"] = num(out.get("passing_yds", ""))
    out["PassingTD"] = num(out.get("passing_td", ""))
    out["INT"] = num(out.get("passes_intercepted", ""))
    out["RushingYds"] = num(out.get("rushing_yds", ""))
    out["RushingTD"] = num(out.get("rushing_td", ""))
    out["ReceivingYds"] = num(out.get("receiving_yds", ""))
    out["ReceivingTD"] = num(out.get("receiving_td", ""))
    out["FantasyPoints"] = num(out.get("fantasy_points", ""))
    out["FantasyPointsPPR"] = num(out.get("fantasy_points_ppr_", ""))
    return out

# Public search: BFS or DFS traversal
def find_by_name(name: str, method: str = "BFS"):
    """
    Traverse via BFS (default) or DFS('preorder') and return a UI dict for
    the first node whose .player == name returns None if not found.
    """
    if not _tree or not _tree.root:
        return None
    try:
        nodes = _tree.DFS('preorder') if method == "DFS" else _tree.BFS()
    except Exception:
        nodes = _tree.BFS()
    for n in nodes:
        if getattr(n, "player", "") == name:
            return _node_to_ui_dict(n)
    return None
