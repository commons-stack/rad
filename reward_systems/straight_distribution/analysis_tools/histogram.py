from importlib.metadata import distribution
from ..straightDistribution import StraightDistribution
import plotly.express as px
import pandas as pd
from IPython.display import Markdown, display
import json


# [TODO]change to markdown and find a way to insert some variables into the text so f.ex we can mention which dataset we are using
# header = "# Histogram"
# description = f"This is a histogram of the { self.objectName} object. It's stored in /reward_systems/straight_distribution as a regular python module. Apart from perfoming the analysis, it can also output a visual representation with a specific header (above) and description text. "
author = "Nuggan"
Last_updated = "2022."
version = ""


def run(straight_distribution_data):
    """
    Runs the main module function: a histogram of the reward distribution among users of the reward system

    Args:
        straight_distribution_data: The object with the reward distribuiton system
    Raises:
        [TODO]: Check for errors and raise them
    Returns:
        res: a DataFrame with the requested results. Contains two columns, "ID" and "AMOUNT TO RECEIVE"

    """
    # print(straight_distribution_data)
    distribution = StraightDistribution.generate_from_dict(straight_distribution_data)
    res = distribution.distribution_results

    return res


def printDescription(straight_distribution_data):
    """
    Prints the description of the analysis module to be displayed above the graph

    Args:
        straight_distribution_data: The object with the reward distribuiton system
    Raises:
        [TODO]: Check for errors and raise them
    Returns:
        nothing, it prints the texts

    """
    name = straight_distribution_data["name"]
    header = f'# "{name}" Histogram'
    description = f"This is a histogram of the **{ name }** object. It's stored in /reward_systems/straight_distribution as a regular python module. Apart from perfoming the analysis, it can also output a visual representation with a specific header (above) and description text. "

    display(Markdown(header))
    display(Markdown(description))


def printGraph(straight_distribution_data):
    """
    Prints a visualization of the histogram generated by run(). This function is itended to be called from inside the jupyter notebook

    Args:
        straight_distribution_data: The object with the reward distribuiton system
    Raises:
        [TODO]: Check for errors and raise them
    Returns:
        nothing, it prints the figure

    """

    distribution = pd.DataFrame(run(straight_distribution_data))

    fig_freq = px.bar(
        distribution,
        x="ID",
        y="AMOUNT TO RECEIVE",
        labels={"AMOUNT TO RECEIVE": "Received", "ID": "Beneficiary"},
        title="Rating Distribution",
        width=800,
        height=300,
    )
    fig_freq.show()
