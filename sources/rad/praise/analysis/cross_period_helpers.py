from natsort import natsorted
import os
from rad import importer
import pandas as pd
from . import sort_by_controversial


def combine_distribution_table(distObjs, config={}):
    # receives an array of distobj and returns a dataframe containing the whole istribution results.

    allrounds_df = []

    for dist in distObjs:

        dist_df = pd.DataFrame(dist.distributionResults)

        for index, row in dist_df.iterrows():
            allrounds_df.append(row)

    allrounds_df = pd.DataFrame(allrounds_df)
    allrounds_df.reset_index(inplace=True)

    return allrounds_df


def combine_quantifier_data(distObjs, config={}):
    # receives an array of distobj and returns a dataframe containing the whole istribution results.

    allrounds_df = []

    for dist in distObjs:

        quant_df = sort_by_controversial.run(dist)

        for index, row in quant_df.iterrows():
            allrounds_df.append(row)

    allrounds_df = pd.DataFrame(allrounds_df)
    allrounds_df.reset_index(inplace=True)

    return allrounds_df
