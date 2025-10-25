import tree
import pandas as pd
import numpy
import csv

# data = pd.read_csv("data/player_stats.csv")
# print(data.iloc[0].to_numpy())

player_tree = tree.Tree()

try:
    with open("data/player_stats.csv", 'r') as f:
        for line in f:
            player_tree.insert(player_tree.root, line.strip())
except FileNotFoundError:
    print("data file not found")
    raise


