from natsort import natsorted
import os
from rad import importer
import pandas as pd
from . import sort_by_controversial


def combine_distribution_table(distObjs, config={}):
    # receives an array of distobj and returns a dataframe containing the whole distribution results.

    allrounds_df = []

    for i, dist in enumerate(distObjs):

        dist_df = pd.DataFrame(dist.distributionResults)

        for index, row in dist_df.iterrows():
            row["DIST_ROUND"] = i
            allrounds_df.append(row)

    allrounds_df = pd.DataFrame(allrounds_df)
    allrounds_df.reset_index(inplace=True)

    return allrounds_df


def combine_quantification_data(distObjs, config={}):
    # receives an array of distobj and returns a dataframe containing the whole quantification data.

    allrounds_df = []

    print(type(distObjs))

    for i, dist in enumerate(distObjs):

        quant_df = sort_by_controversial.run(dist)

        for index, row in quant_df.iterrows():
            row["DIST_ROUND"] = i
            allrounds_df.append(row)

    allrounds_df = pd.DataFrame(allrounds_df)

    allrounds_df["DATE"] = pd.to_datetime(allrounds_df["DATE"])

    allrounds_df.sort_values(by="DATE", inplace=True)

    allrounds_df.reset_index(inplace=True)

    return allrounds_df
