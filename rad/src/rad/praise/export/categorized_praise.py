import pandas as pd
from ..praiseObj import Praise
from ..analysis import cross_period_category_analysis as cross_cat
from ..analysis import sort_by_controversial as contr_sort


def run_export(_data, _config={}):
    """
    Creates a CSV file of the categorized praise dataset.

        Args:
            _data: the necessary data to generate it
            _config:(Optional) dict with extra configuration data, if necessary.
        Raises:
            [TODO] Implement errors and list them here.
        Returns:
            nothing, just saves the files
    """

    categ_keywords = _config["categ_keywords"]

    # print(categ_keywords)

    # get the cuantification df
    _prData = contr_sort.run(_data)

    praise_df = cross_cat.create_clean_df(_prData)

    categ_df = cross_cat.create_category_df(praise_df, categ_keywords)

    # categ_df = cross_cat.create_category_df(_distData, categ_keywords)

    all_categorized_praise = categ_df.to_csv(sep=",", index=False)
    uncategorized_praise = categ_df.loc[categ_df["category"].isnull()].to_csv(
        sep=",", index=False
    )

    return all_categorized_praise, uncategorized_praise, ".csv"


"""     if save_csv==true:
        # save the categorization into csv; there's a file including only uncategorized praise
        category_df.loc[category_df["category"].isnull()].to_csv("uncategorized.csv")
        print(
            f"{sum(category_df['category'].isnull())} out of {len(category_df)} praises uncategorized"
        )
        category_df.to_csv("categorized_praise.csv") """


def save_export(_name, _data, _config={}):

    export_all, export_uncateogrized, export_extension = run_export(_data, _config)

    # filename = "export_" + _name + "_" + _config["type"] + ".csv"
    filename1 = _name + "_allCategorizedPraise" + export_extension
    with open(filename1, "w") as f:
        f.write(export_all)

    filename2 = _name + "_uncategorizedPraise" + export_extension
    with open(filename2, "w") as f:
        f.write(export_uncateogrized)

    return [filename1, filename2]
