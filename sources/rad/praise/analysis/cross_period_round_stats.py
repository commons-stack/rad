import pandas as pd
import numpy as np
import plotly.express as px


def run(allrounds_df, _config={}):

    try:
        NUMBER_OF_PERIODS = _config["NUMBER_OF_PERIODS"]
        STEP_SIZE = _config["STEP_SIZE"]
    except:
        NUMBER_OF_PERIODS = 8
        STEP_SIZE = "W"

    end_date = allrounds_df["DATE"].max().ceil("D")

    dates = pd.date_range(end=end_date, periods=NUMBER_OF_PERIODS, freq=STEP_SIZE)

    all_stats = []
    for i, period_start in enumerate(dates):
        if i == (len(dates) - 1):
            continue

        round_row = pd.Series()
        # basic information
        round_row["period_name"] = "period-" + str(i + 1)
        round_row["period_start_time"] = dates[i]
        round_row["period_end_time"] = dates[i + 1]

        current_praise = allrounds_df[
            (allrounds_df["DATE"] > round_row["period_start_time"])
            & (allrounds_df["DATE"] <= round_row["period_end_time"])
        ].copy()

        #
        round_row["total_praise"] = len(current_praise)
        round_row["total_praise_receiver"] = len(
            np.unique(current_praise["TO USER ACCOUNT"])
        )
        round_row["total_praise_giver"] = len(
            np.unique(current_praise["FROM USER ACCOUNT"])
        )

        all_stats.append(round_row)

    return pd.DataFrame(all_stats)


def printDescription(praise_distribution_data, _config={}):
    pass


def printGraph(praise_distribution_data, _config={}):
    all_stats = run(praise_distribution_data, _config)

    if _config == {}:
        _x = "period_start_time"
        _y = "total_praise"
    else:
        _x = _config["x"]
        _y = _config["y"]

    fig = px.line(all_stats, x=_x, y=_y, markers=True)

    fig.show()
