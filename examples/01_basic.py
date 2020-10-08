import logging

import networkx as nx
import numpy as np
import pandas as pd
from pandas_pipeline_graphviz import pandas_pipeline, convert_to_dot

logging.basicConfig(level=logging.DEBUG)
graph = nx.DiGraph()

@pandas_pipeline(graph=graph)
def compute_square(df):
    return df ** 2

#%% data load
df_start = pd.DataFrame(np.random.rand(100, 3), columns=["a", "b", "c"])

#%% pipeline
df_end = compute_square(df_start)

#%% draw graph
dot_graph = convert_to_dot(graph)
dot_graph.draw("01_basic.png")
dot_graph.draw("01_basic.svg")
