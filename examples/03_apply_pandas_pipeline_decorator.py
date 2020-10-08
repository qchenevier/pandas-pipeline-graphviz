import logging

import networkx as nx
import numpy as np
import pandas as pd
from pandas_pipeline_graphviz import pandas_pipeline, convert_to_dot, apply_pandas_pipeline_decorator


def compute_polynomial_features(df):
    df_squared = (df ** 2).rename(columns=lambda x: x + "_squared")
    return pd.concat([df, df_squared], axis=1)

def compute_binary(df, threshold=0.5):
    return df > threshold

def compute_merge(df1, df2):
    return (
        df1
        .merge(
            df2,
            suffixes=("", "_merged"),
            left_index=True,
            right_index=True
        )
    )

#%% apply decorator
logging.basicConfig(level=logging.DEBUG)
graph = nx.DiGraph()
apply_pandas_pipeline_decorator(function_prefix="compute", graph=graph)

#%% data load
df_start = pd.DataFrame(np.random.rand(100, 3), columns=["a", "b", "c"])

#%% pipeline
df_polynomial = compute_polynomial_features(df_start)
df_binary = compute_binary(df_start)
df_end = compute_merge(df_polynomial, df_binary)

#%% draw graph
dot_graph = convert_to_dot(graph)
dot_graph.draw("03_apply_pandas_pipeline_decorator.png")
dot_graph.draw("03_apply_pandas_pipeline_decorator.svg")
