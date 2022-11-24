import pandas as pd
import numpy as np
from IPython.display import Markdown, display
from re import search
import plotly.express as px

from . import cross_period_round_stats


def run(allrounds_df, categ_keywords, _config={}):

    praise_df = create_clean_df(allrounds_df)

    category_df = create_category_df(praise_df, categ_keywords)

    # When there's a praise matching more than one category, they will be counted multiple times
    # organize the data for easier analysis
    categ_praise_scores = {k: [] for k in categ_keywords.keys()}

    for kr, row in category_df.iterrows():
        if type(row["category"]) is list:
            for key in row["category"]:
                categ_praise_scores[key] += [
                    {
                        "praise": row["REASON"],
                        "avg_score": row["AVG SCORE"],
                        "receiver": row["TO USER ACCOUNT"],
                        "date": row["DATE"],
                    }
                ]
    categ_praise_scores_df = dict.fromkeys(categ_keywords.keys())
    for key, item in categ_praise_scores.items():
        categ_praise_scores_df[key] = pd.DataFrame(item)

    return categ_praise_scores_df


def printDescription(praise_distribution_data, categ_keywords, _config={}):
    categ_praise_df = run(praise_distribution_data, categ_keywords, _config={})
    if _config == {}:
        _mode = "summary-table"
        _num = 0
    else:
        _mode = _config["mode"]
        _num = _config["num"]
    # mode: basic table (get_categ_stats?)
    if _mode == "summary-table":
        display(get_categ_stats(categ_praise_df, categ_keywords))

    # mode top x per cat
    if _mode == "top-scored":
        mdtext = ""
        for categ in categ_praise_df.keys():
            categ_name = "# " + categ + "\n"
            toppraise = (
                categ_praise_df[categ]
                .sort_values(by="avg_score", ascending=False)
                .iloc[:_num]
            )
            top3_table = f"\
        | Avg. score | To | Reason | Date |\n \
        |:-----------|----|--------|-----:|\n"
            for kr, row in toppraise.iterrows():
                to_user = row["receiver"]
                reason = row["praise"]
                score = row["avg_score"]
                date = row["date"][:10]

                top3_table += f"| {score} | {to_user} | {reason} | {date} |\n"
                # print(f'Praise score average: {score}\nFROM {from_user} TO {to_user},reason:\n{reason}\n')
            mdtext += categ_name + top3_table
        display(Markdown(mdtext))


def printGraph(praise_distribution_data, categ_keywords, _config={}):
    categ_praise_df = run(praise_distribution_data, categ_keywords, _config={})

    if _config == {}:
        _mode = "avg-stats"
        _y = "number"
    else:
        _mode = _config["mode"]
        _y = _config["y"]

    # mode avg score box
    if _mode == "avg-stats":
        # plot it out
        categ_stats = get_categ_stats(categ_praise_df, categ_keywords)
        categ_stats["max-mean"] = categ_stats["max"] - categ_stats["mean"]
        categ_stats["mean-min"] = categ_stats["mean"] - categ_stats["min"]

        fig = px.bar(
            categ_stats,
            y="mean",
            error_y="max-mean",
            error_y_minus="mean-min",
            title="average score of each category",
        )
        fig.show()
        display(Markdown("errorbars mark the maximum average score for this category"))

    # mode trend, y = "number"/ "avg_score"
    if _mode == "trend":
        trend_df = create_trend_df(praise_distribution_data, categ_keywords)
        px.line(
            trend_df.filter(like=_y),
            title="number of praise in each category, across time",
        )

    pass


def get_categ_stats(categ_praise_scores_df, keywords):
    df = categ_praise_scores_df.copy()
    categ_stats = dict.fromkeys(keywords.keys())
    for categ in keywords.keys():
        if len(df[categ]) == 0:  # empty category, skip this
            continue
        categ_stats[categ] = {
            "mean": np.mean(df[categ]["avg_score"]),
            "max": np.max(df[categ]["avg_score"]),
            "min": np.min(df[categ]["avg_score"]),
        }

    categ_stats_df = pd.DataFrame(categ_stats)
    categ_stats_df = categ_stats_df.transpose().sort_values(by="mean")
    return categ_stats_df


def create_clean_df(allrounds_df):
    # clean the data
    allpraise_df = allrounds_df[["REASON", "AVG SCORE", "TO USER ACCOUNT", "DATE"]]
    nonzerodf = allpraise_df.loc[
        (allpraise_df["AVG SCORE"] > 0) * (~allpraise_df["REASON"].isnull())
    ]
    # print(f'among {len(allpraise_df)} praises, {len(nonzerodf)} have scores more than 0. Only include them')
    nonzerodf.insert(0, "CLEANED REASON", nonzerodf["REASON"].apply(clean_praise))

    return nonzerodf


# cleaning master function
def clean_praise(praise):
    # code adapted from: https://ourcodingclub.github.io/tutorials/topic-modelling-python/
    my_stopwords = nltk.corpus.stopwords.words("english")
    word_rooter = nltk.stem.snowball.PorterStemmer(
        ignore_stopwords=False
    ).stem  # clean words to the "stem" (e.g. words->word, talked->talk)
    my_punctuation = "!\"$%&'()*+,-./:;<=>?[\\]^_`{|}~•@"

    praise = praise.lower()  # lower case
    praise = re.sub("[" + my_punctuation + "]+", " ", praise)  # strip punctuation
    praise = re.sub("\s+", " ", praise)  # remove double spacing
    praise = re.sub("([0-9]+)", "", praise)  # remove numbers
    praise_token_list = [
        word for word in praise.split(" ") if word not in my_stopwords
    ]  # remove stopwords

    praise_token_list = [
        word_rooter(word) if "#" not in word else word for word in praise_token_list
    ]  # apply word rooter

    praise = " ".join(praise_token_list)
    return praise


def create_category_df(input_df, categ_keywords):
    # do categorization
    allcategs = []
    for kr, row in input_df.iterrows():
        category = []
        praise = row["CLEANED REASON"].lower()
        for praise_type, keywords in categ_keywords.items():
            if search(keywords, praise):
                category.append(praise_type)
        if len(category):
            allcategs.append(category)
        else:
            allcategs.append(np.nan)
    category_df = pd.concat(
        [input_df.reset_index(), pd.DataFrame({"category": allcategs})], axis=1
    )
    return category_df

    # TODO Make an export out of this


"""     if save_csv==true:
        # save the categorization into csv; there's a file including only uncategorized praise
        category_df.loc[category_df["category"].isnull()].to_csv("uncategorized.csv")
        print(
            f"{sum(category_df['category'].isnull())} out of {len(category_df)} praises uncategorized"
        )
        category_df.to_csv("categorized_praise.csv") """


def create_trend_df(praise_distribution_data, categ_keywords):

    round_stats = cross_period_round_stats.run(allrounds_df)

    allrounds_df = praise_distribution_data.copy()
    mean_score_dict = {k: [] for k in categ_keywords.keys()}
    praise_num_dict = {k: [] for k in categ_keywords.keys()}
    for round_name in allrounds_df["DIST_ROUND"].unique():
        round_categ_praise_score_df, _ = run(allrounds_df[round_name], categ_keywords)
        round_categ_stats = get_categ_stats(round_categ_praise_score_df, categ_keywords)
        for key in mean_score_dict.keys():
            mean_score_dict[key].append(round_categ_stats["mean"].loc[key])
            praise_num_dict[key].append(len(round_categ_praise_score_df[key]))
    for key in mean_score_dict.keys():
        round_stats[key + "_avg_score"] = mean_score_dict[key]
        round_stats[key + "_praise_num"] = praise_num_dict[key]

    return round_stats
