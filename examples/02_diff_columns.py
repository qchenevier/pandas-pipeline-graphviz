import logging

import networkx as nx
import numpy as np
import pandas as pd
from pandas_pipeline_graphviz import pandas_pipeline, convert_to_dot

logging.basicConfig(level=logging.DEBUG)
graph = nx.DiGraph()

@pandas_pipeline(graph=graph)
def compute_polynomial_features(df):
    df_squared = (df ** 2).rename(columns=lambda x: x + "_squared")
    return pd.concat([df, df_squared], axis=1)

#%% data load
df_start = pd.DataFrame(np.random.rand(100, 3), columns=["a", "b", "c"])

#%% pipeline
df_end = compute_polynomial_features(df_start)

#%% draw graph
dot_graph = convert_to_dot(graph)
dot_graph.draw("02_diff_columns.png")
dot_graph.draw("02_diff_columns.svg")
