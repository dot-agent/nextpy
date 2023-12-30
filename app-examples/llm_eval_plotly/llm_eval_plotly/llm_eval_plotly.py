# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Welcome to Nextpy! This file outlines the steps to create a basic app."""
from xtconfig import config
import nextpy as xt
from io import StringIO
import pandas as pd
import plotly.graph_objects as go
from llm_eval_plotly.components import drawer_sidebar, DrawerState
from llm_eval_plotly.data.data import llm_eval_result


def grab_categories_and_values(df: pd.DataFrame, model_name: str = None):
    categories = list(df.loc[model_name].index)
    values = list(df.loc[model_name].values)
    categories.append(categories[0])
    values.append(values[0])
    return categories, values


default_llm_data = llm_eval_result

md_df = (
    pd.read_csv(
        StringIO(default_llm_data.replace(" ", "")),  # Get rid of whitespaces
        sep="|",
        index_col=1,
    )
    .dropna(axis=1, how="all")
    .iloc[1:]
)
models = list(md_df.index)
md_df = md_df.reset_index()
md_df = md_df.set_index("model_name")
md_df = md_df.astype(float)

fig = go.Figure()
for model_name in md_df.index:
    categories, values = grab_categories_and_values(md_df, model_name)
    fig.add_trace(
        go.Scatterpolar(r=values, theta=categories, fill="toself", name=model_name)
    )
fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0.0, 1.0])), showlegend=True
)


@xt.page("/", "Index")
def index() -> xt.Component:
    return xt.box(
        drawer_sidebar(),
        xt.plotly(data=fig,),
        class_name="relative text-center w-[100vw] h-[100vh] bg-white",
    )


# Add state and page to the app.
app = xt.App()

