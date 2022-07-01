from importlib.metadata import distribution
from ..straightDistribution import StraightDistribution
import plotly.express as px
import pandas as pd
import json


# [TODO]change to markdown and find a way to insert some variables into the text so f.ex we can mention which dataset we are using
header = "# Histogram"
description = "This is a histogram of the straight distribution object. It's stored in /reward_systems/straight_distribution as a regular python module. Apart from perfoming the analysis, it can also output a visual representation with a specific header (above) and description text. "
author = "Nuggan"
Last_updated = "2022."
version = ""


def run(straight_distribution_data):
    # print(type(straight_distribution_data))
    distribution = StraightDistribution.generate_from_dict(straight_distribution_data)
    res = distribution.distribution_results

    return res


def printGraph(straight_distribution_data):

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
