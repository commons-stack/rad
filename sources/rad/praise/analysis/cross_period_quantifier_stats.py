# TODO!!!!!


import pandas as pd
import numpy as np
import plotly.express as px


def run(allrounds_df, _config={}):

    base_df = allrounds_df
    quantifiertable = data_by_quantifier(allrounds_df.copy())

    quantratingdf = quantifiertable
    quantlist = _get_valid_quantifier(base_df, quantratingdf)
    metrics_df = _get_participant_metrics(base_df, quantratingdf, quantlist)
    return metrics_df

    pass


def printDescription(allrounds_df, _config={}):
    # TODO

    pass


def printGraph(allrounds_df, _config={}):
    quant_stats = run(allrounds_df, _config)

    if _config == {}:
        _y = "pearson_coef"
    else:
        _y = _config["y"]

    if _y == "pearson_coef":
        fig = px.scatter(
            quant_stats.sort_values(by="pearson_coef"),
            y="pearson_coef",
            title="How similiar is one's score with the other quantifiers?",
        )

    elif _y == "av_score_displacement":
        fig = px.bar(
            quant_stats.sort_values(by="av_score_displacement"),
            y="av_score_displacement",
            title="Do one tends to give higher or lower scores than the other quantifiers?",
        )

    fig.show()


def _get_valid_quantifier(base_df, quantratingdf):
    df = base_df
    quantifier_rating_table = quantratingdf
    quant_cols = df.filter(like="USERNAME", axis=1)
    quantlist = np.unique(quant_cols.values)
    valid_qt = np.ones_like(quantlist, dtype=bool) * True
    for kq, quantid in enumerate(quantlist):
        quantdf = quantifier_rating_table.loc[
            quantifier_rating_table["QUANT_ID"] == quantid
        ]
        # exclude invalid IDs
        if len(quantdf) == 0:
            valid_qt[kq] = False
        if set(quantdf["QUANT_VALUE"].values) == {0}:
            valid_qt[kq] = False
        if quantid == "None":
            valid_qt[kq] = False
    quantlist = quantlist[valid_qt]
    return quantlist


def get_outlier(self, keywords, maxscore=5):
    from re import search  # for searching sub strings

    """
    keywords is a string in regex pattern. 
    For example, to single out all the praise about attending meetings:
    keywords = 'attend|showing up|join'
    """
    quantifier_rating_table = self.quantratingdf
    df = self.df
    for QUANT_ID in self.quantlist:
        quantdf = quantifier_rating_table.loc[
            quantifier_rating_table["QUANT_ID"] == QUANT_ID
        ]
        av_scores = []
        for kr, row in quantdf.iterrows():
            praise_id = row["PRAISE_ID"]
            praise_reason = df.loc[df["ID"] == praise_id]["REASON"].values[0]
            # if multiple things are mentioned in this praise, let's skip it.
            if search(keywords, praise_reason) and ("and" not in praise_reason):
                prase_avscore = df.loc[df["ID"] == praise_id]["AVG SCORE"].values[0]
                quantifier_score = row["QUANT_VALUE"]
                # when others most likely don't give it such high score
                if quantifier_score > maxscore and prase_avscore <= maxscore:
                    print(
                        f'{QUANT_ID} gave {quantifier_score} for the praise "{praise_reason}"'
                    )


def _get_participant_metrics(base_df, quantratingdf, quantlist):
    # TODO: make this more modularized so the user can easily choose what analysis to include
    quantifier_coef = []
    quantifier_score_displace = []

    quantifier_rating_table = quantratingdf
    df = base_df
    for QUANT_ID in quantlist:
        quantdf = quantifier_rating_table.loc[
            quantifier_rating_table["QUANT_ID"] == QUANT_ID
        ]
        av_scores_others = []
        score_quant = []
        scoredist = []
        scoredisplace = []
        for kr, row in quantdf.iterrows():
            quantifier_score = row["QUANT_VALUE"]
            if np.isnan(quantifier_score):
                continue
            praise_id = row["PRAISE_ID"]
            praise_row = df.loc[df["ID"] == praise_id]

            otherscores = praise_row.filter(like="SCORE ").values.tolist()[0]
            otherscores.remove(quantifier_score)

            otherscores = np.array(otherscores)
            otherscores = otherscores[~np.isnan(otherscores)]

            if len(otherscores) < 2:
                continue
            av_scores_others.append(np.mean(otherscores))
            score_quant.append(quantifier_score)
            # like "standar deviation" from this score
            scoredist.append(
                np.sqrt(sum((quantifier_score - otherscores) ** 2)) / (len(otherscores))
            )
            scoredisplace.append(np.mean(quantifier_score - otherscores))

        coef = np.corrcoef(score_quant, av_scores_others)[1, 0]
        quantifier_coef.append(coef)
        quantifier_score_displace.append(np.mean(scoredisplace))
    quantifier_metrics_df = pd.DataFrame(
        index=quantlist,
        data={
            "pearson_coef": quantifier_coef,
            "av_score_displacement": quantifier_score_displace,
        },
    )
    return quantifier_metrics_df


def data_by_quantifier(praise_data):
    quant_only = pd.DataFrame()
    # praise_data.drop(['DATE', 'TO USER ACCOUNT', 'TO USER ACCOUNT ID', 'TO ETH ADDRESS', 'FROM USER ACCOUNT', 'FROM USER ACCOUNT ID', 'FROM ETH ADDRESS', 'REASON', 'SOURCE ID', 'SOURCE NAME', 'AVG SCORE'], axis=1, inplace=True)
    num_of_quants = len(praise_data.filter(like="QUANTIFIER").columns)
    for i in range(num_of_quants):
        q_name = str("QUANTIFIER " + str(i + 1) + " USERNAME")
        q_value = str("SCORE " + str(i + 1))
        q_duplicate = str("DUPLICATE ID " + str(i + 1))
        buf = praise_data[["ID", q_name, q_value, q_duplicate]].copy()

        # delete the duplicated rows
        buf = buf.loc[buf[q_duplicate].isnull()]  # only include the non-duplicated rows
        buf = buf[["ID", q_name, q_value]]  # don't need the duplication info anymore
        buf = (
            buf.dropna()
        )  # NA comes from when the quantifier is less than given in cross-period analysis

        buf.rename(
            columns={
                q_name: "QUANT_ID",
                q_value: "QUANT_VALUE",
                "ID": "PRAISE_ID",
            },
            inplace=True,
        )

        quant_only = quant_only.append(buf.copy(), ignore_index=True)

    columnsTitles = ["QUANT_ID", "PRAISE_ID", "QUANT_VALUE"]
    quant_only.sort_values(["QUANT_ID", "PRAISE_ID"], inplace=True)
    quant_only = quant_only.reindex(columns=columnsTitles).reset_index(drop=True)
    return quant_only
