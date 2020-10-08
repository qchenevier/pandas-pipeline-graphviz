import logging

from addict import Dict
import networkx as nx
import pandas as pd

def clean_columns(series):
    return (
        series.astype(str)
        .str.replace(r"\n\ *", " ")
        .str.replace(r"#", "-")
        .str.replace(r"<", "-")
        .str.replace(r"&", "-")
        .str.strip()
        .tolist()
    )


def dict_to_html(dictionary):
    return " ".join(f'{k}="{v}"' for k, v in dictionary.items())


def compute_record_label(df, df_name, new_columns=None):
    columns = clean_columns(df.columns)
    new_columns = clean_columns(pd.Series(new_columns))
    header = f"""<tr><td><b>{df_name}</b></td></tr>"""
    shape = f"""<tr><td><b>↓ {df.shape[0]}  → {df.shape[1]}</b></td></tr>"""
    columns_table = "".join(
        [
            f'<tr><td {dict_to_html(style.new)} align="left">{col}</td></tr>'
            if col in new_columns
            else f'<tr><td align="left">{col}</td></tr>'
            for col in columns
        ]
    )
    table_html = (
        f"""<<table {dict_to_html(style.table)}>"""
        f"""<tr><td><table {dict_to_html(style.header)}>"""
        f"{header}"
        f"{shape}"
        "</table></td></tr>"
        f"""<tr><td><table {dict_to_html(style.columns)}>"""
        f"{columns_table}"
        "</table></td></tr>"
        "</table>>"
    )
    return {
        "shape": "record",
        "label": table_html,
    }


# pylint: disable=bad-continuation
def update_node_style(graph, node, new_columns=None):
    style = node.get("style")
    name = node.get("name")
    value = node.get("value")
    if style:
        graph.nodes[name].update(style)
    is_node_writable = "label" not in graph.nodes[name] or new_columns
    is_dataframe_node = isinstance(value, pd.DataFrame)
    if is_node_writable and is_dataframe_node:
        graph.nodes[name].update(
            compute_record_label(value, name, new_columns=new_columns)
        )
    elif is_node_writable and value:
        graph.nodes[name]["label"] = value


def add_edge_to_graph(graph, start, end, new_columns=None):
    if "name" not in start or "name" not in end:
        msg = "node dictionary need to have at least a 'name' property"
        logging.error(msg)
        raise ValueError(msg)
    graph.add_edge(start["name"], end["name"])
    update_node_style(graph, start)
    update_node_style(graph, end, new_columns)


def convert_to_dot(graph):
    dot_graph = nx.nx_agraph.to_agraph(graph)
    dot_graph.graph_attr.update(
        {"dpi": 100, "bgcolor": None, "layout": "dot", "rankdir": "LR"}
    )
    dot_graph.node_attr.update({"fontname": "Arial"})
    dot_graph.edge_attr.update({"color": "grey"})
    dot_graph.layout(prog="dot")
    return dot_graph


style = Dict(
    {
        "function": {"style": "filled", "color": "deepskyblue"},
        "dataframe": {"style": "filled", "color": "grey97", "shape": "rectangle"},
        "table": {"border": 0, "cellborder": 0, "cellspacing": 0},
        "header": {
            "border": 1,
            "color": "darkgrey",
            "cellborder": 0,
            "cellspacing": 0,
        },
        "columns": {"border": 0, "cellborder": 0, "cellspacing": 0},
        "new": {"bgcolor": "cyan"},
    }
)
