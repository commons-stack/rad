import pandas as pd
import datetime
from ..praiseObj import Praise


def run_export(_data, _config={}):
    """
    Creates a Forum Post detailing the distribution.

        Args:
            _data: the necessary data to generate it
            _config:(Optional) dict with extra configuration data, if necessary.
        Raises:
            [TODO] Implement errors and list them here.
        Returns:
            forum_post: The text of the post
            export_extension: The file extension under which to save the file, as string
    """

    forum_post = generate_post(_data)

    export_extension = ".md"

    return forum_post, export_extension


def save_export(_name, _data, _config={}):

    export_file, export_extension = run_export(_data, _config)

    # filename = "export_" + _name + "_" + _config["type"] + ".csv"
    filename = _name + export_extension
    with open(filename, "w") as f:
        f.write(export_file)

    return [filename]


def generate_post(_data):
    # praise_path = params["system_settings"]["praise"]["input_files"]["praise_data"]
    # token_table_path = ROOT_INPUT_PATH + "distribution_results/raw_csv_exports/final_praise_token_allocation.csv"
    # params["token_allocation_per_reward_system"] = list(map(int, params["token_allocation_per_reward_system"]))

    # data = pd.read_csv(praise_path)
    dataTable = pd.DataFrame(_data.praiseInstance.dataTable)
    start_date = pd.to_datetime(dataTable["DATE"].min()).date()

    end_date = pd.to_datetime(dataTable["DATE"].max()).date()
    total_tokens = _data.totalDistributedTokens
    praise_pct = _data.userRewardPct
    sourcecred_pct = _data.quantifierRewardPct

    rewards_amt = _data.totalDistributedTokens * _data.userRewardPct / 100
    quant_amt = _data.totalDistributedTokens * _data.quantifierRewardPct / 100

    token_table = pd.DataFrame(_data.distributionResults)
    token_table = token_table[["USER IDENTITY", "TOTAL TO RECEIVE"]].copy()
    token_table.rename(
        columns={"USER IDENTITY": "Username", "TOTAL TO RECEIVE": "Rewards in TEC"},
        inplace=True,
    )
    markdown_table = token_table.to_markdown(index=False)
    output = f"""# TEC Rewards Distribution - {_data.name}  - {start_date.strftime("%d/%m/%y")} to {end_date.strftime("%d/%m/%y")} 
This period covers praise given between **{start_date.strftime("%d %B %Y")} and {end_date.strftime("%d %B %Y")}**. 
We allocated **{total_tokens}** TEC tokens for rewards, with a **{praise_pct}:{sourcecred_pct}** split between Praisees and quantifiers. Some praise accounts still haven’t been activated so the total amount below will be less than what we set aside to distribute. Out of the total rewards:   
* {rewards_amt} tokens were given as praise rewards :pray:  
* {quant_amt} distributed among quantifiers :balance_scale: 
    
This data has been reviewed by the Quantifiers and the Reward Board, and has been submitted for distribution to the [Reward Board DAO](https://xdai.aragon.blossom.software/#/rewardboardtec/)    
You can check out the [full period analysis here](ADD LINK HERE). :bar_chart:    
This post will be open to the community for review for 48 hours then submitted to the Reward Board for final execution. :heavy_check_mark:   
The Rewards Distribution for this round is as follows:
"""
    output += markdown_table
    return output
