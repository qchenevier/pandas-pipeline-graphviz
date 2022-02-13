
import networkx as nx
import numpy as np
import pandas as pd
from pandas_pipeline_graphviz import pandas_pipeline, convert_to_dot
import unittest



graph = nx.DiGraph()


@pandas_pipeline(graph=graph)
def compute_square(df):
    return df ** 2


# we have to use global variables
df_start = pd.DataFrame(np.random.rand(100, 3), columns=["a", "b", "c"])
df_end = compute_square(df_start)



class TestStringMethods(unittest.TestCase):


    def test_edges(self):
        self.assertEqual(2, len(graph.edges))
        self.assertTrue(('df_start', 'df_start—compute_square—df_end') in list(graph.edges))
        self.assertTrue(('df_start—compute_square—df_end', 'df_end') in list(graph.edges))


if __name__ == '__main__':
    unittest.main()