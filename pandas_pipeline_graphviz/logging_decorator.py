from functools import wraps
import inspect
import logging
import re
import types

import networkx as nx
import pandas as pd

from pandas_pipeline_graphviz.pipeline_graph import add_edge_to_graph, style


def get_output_name(f_name, stack_position=2):
    stack = inspect.stack(context=30)
    frame = stack[stack_position]
    var_name = None
    try:
        for code_line in reversed(frame.code_context[: frame.lineno]):
            if re.search(rf"\ *=\ *{f_name}", code_line):
                var_name = code_line.split("=")[0].strip()
                break
    except Exception:  # pylint: disable=broad-except
        logging.exception("Could not get output name")
        var_name = None
    return var_name


def find_dataframe_name_in_globals(df, script_globals):
    dataframes = [
        k
        for k, v in script_globals.items()
        if isinstance(v, pd.DataFrame) and not re.match("_", k)
    ]
    all_names = [k for k in dataframes if script_globals[k].equals(df)]
    if all_names:
        return all_names[0]
    return None


def get_dataframes_global_names(*args, script_globals=None, **kwargs):
    return {
        find_dataframe_name_in_globals(arg, script_globals): arg
        for arg in [*args, *list(kwargs.values())]
        if isinstance(arg, pd.DataFrame)
    }


def pandas_pipeline(graph=None, show_columns=True, log=True, script_globals=None):
    if script_globals is None:
        script_globals = dict(inspect.getmembers(inspect.stack()[1][0]))["f_globals"]

    def pandas_pipeline_decorator(f):
        @wraps(f)
        def f_decorated(*args, **kwargs):
            output = f(*args, **kwargs)

            input_columns = set()
            dataframes = get_dataframes_global_names(
                *args, script_globals=script_globals, **kwargs
            )
            output_name = get_output_name(f.__name__, stack_position=2)
            f_dict = dict(
                name=f"""{"_".join(dataframes.keys())}—{f.__name__}—{output_name or ""}""",
                style=style.function,
                value=f.__name__,
            )

            for df_name, df in dataframes.items():
                input_columns |= set(df)
                if log:
                    logging.info("%s <— %s %s", f.__name__, df_name, df.shape)
                if isinstance(graph, nx.DiGraph):
                    add_edge_to_graph(
                        graph,
                        start=dict(
                            name=df_name,
                            style=style.dataframe,
                            value=df if show_columns else None,
                        ),
                        end=f_dict,
                    )

            if isinstance(output, pd.DataFrame):
                new_columns = list(set(output) - input_columns)
                if log:
                    logging.info("%s —> %s %s", f.__name__, output_name, output.shape)
                    logging.debug(
                        "%s —> %s: new_columns=%s", f.__name__, output_name, new_columns
                    )
                if isinstance(graph, nx.DiGraph):
                    add_edge_to_graph(
                        graph,
                        start=f_dict,
                        end=dict(
                            name=output_name,
                            style=style.dataframe,
                            value=output if show_columns else None,
                        ),
                        new_columns=new_columns,
                    )
            return output

        return f_decorated

    return pandas_pipeline_decorator


# pylint: disable=bad-continuation
def apply_pandas_pipeline_decorator(function_prefix="compute", **decorator_kwargs):
    script_globals = dict(inspect.getmembers(inspect.stack()[1][0]))["f_globals"]
    for name, obj in list(script_globals.items()):
        if isinstance(obj, types.FunctionType):
            if name.startswith(function_prefix):
                script_globals[name] = pandas_pipeline(
                    script_globals=script_globals, **decorator_kwargs
                )(obj)
