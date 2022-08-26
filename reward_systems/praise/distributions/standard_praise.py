# STANDARD PRAISE DISTRIBUTION

# Instantiation of a praise distribution round

#   constructor:
#       -raw praise data and parameters -> executes reward distribution
#   has functions to return:
#       -praise distribution by user
#       -dataframe where praise is sorted by quantifier
#       -the praise megatable

import pandas as pd

from src.rewardDistribution import RewardDistribution
from reward_systems.praise import Praise
from reward_systems.straight_distribution import StraightRewards


class PraiseDistribution(RewardDistribution):
    def __init__(
        self,
        _name,
        _praiseTable,
        _rewardboard,
        _quantPerPraise,
        _quantAllowedValues,
        _duplicatePraiseValuation,
        _pseudonymsActive,
        _distAmount,
        _userRewardPct,
        _quantifierRewardPct,
        _rewardboardRewardPct,
        _tokenName,
        _tokenAddress,
        _distributionResults={},
    ):
        """
        The class constructor

        Args:
            _benficiaries: list of the users participating in the reward system
            _distAmount: number, the amount of tokens to be distributed
            _tokenName: string indicating the name of the token the rewards will be paid out in
            _tokenAddress: the address of the reward token
            _distributionResults: Optional. Dictionary containing the results of a distribution.
        Raises:
            [TODO]: Check for errors and raise them
        Returns:
            nothing.

        """
        super().__init__(_name, "praise")
        self.praiseTable = _praiseTable
        self.rewardboard = _rewardboard
        self.quantPerPraise = int(_quantPerPraise)
        self.quantAllowedValues = _quantAllowedValues
        self.duplicatePraiseValuation = float(_duplicatePraiseValuation)
        self.pseudonymsActive = bool(_pseudonymsActive)
        self.userRewardPct = _userRewardPct
        self.quantifierRewardPct = _quantifierRewardPct
        self.rewardboardRewardPct = _rewardboardRewardPct
        self.distAmount = int(_distAmount)
        self.tokenName = _tokenName
        self.tokenAddress = _tokenAddress
        self.distributionResults = _distributionResults

        if _distributionResults == {}:
            self.do_distribution()

    def __str__(self):
        """
        A stringified description of the object
        Args:
            none
        Raises:
            [TODO]: Check for errors and raise them
        Returns:_
            str: A string describing the object and relevant state variables

        """
        return (
            "From str method of Praise: distAmount is % s, tokenName is % s, results are % s"
            % (self.distAmount, self.tokenName, str(self.distribution_results))
        )

    @classmethod
    def generate_from_params(cls, _objectName, _params, _sources):
        """
        Creates an instance of the rewards system from the parameters as speified in the "parameters.json" file.

        Args:
            (_params): a dictionary from which we want to instatiate the class from. Loaded from the parameters.json file.
        Raises:
            [TODO]: Check for errors and raise them
        Returns:
            cls: an instance of the class with the specified parameters

        """
        praiseObj = {}
        rewardObj = {}
        # load praise Object
        for obj in _sources:
            # future feature: if more than one, merge them (implement method in Praise object)
            # print(_sources[obj].type)
            if _sources[obj].type == "praise" and praiseObj == {}:
                praiseObj = _sources[obj]
            if _sources[obj].type == "straight_distribution" and rewardObj == {}:
                rewardObj = _sources[obj]

        quantPerPraise = praiseObj.quantPerPraise
        quantAllowedValues = praiseObj.quantAllowedValues
        duplicatePraiseValuation = praiseObj.duplicatePraiseValuation
        pseudonymsActive = praiseObj.pseudonymsActive

        praiseTable = praiseObj.dataTable
        rewardboard = rewardObj.beneficiaries

        distAmount = _params["distribution_amount"]
        userRewardPct = _params["user_dist_pct"]
        quantifierRewardPct = _params["quantifiers_dist_pct"]
        rewardboardRewardPct = _params["reward_dist_pct"]

        tokenName = _params["payout_token"]["token_name"]
        tokenAddress = _params["payout_token"]["token_address"]

        return cls(
            _name=_objectName,
            _praiseTable=praiseTable,
            _rewardboard=rewardboard,
            _quantPerPraise=quantPerPraise,
            _quantAllowedValues=quantAllowedValues,
            _duplicatePraiseValuation=duplicatePraiseValuation,
            _pseudonymsActive=pseudonymsActive,
            _distAmount=distAmount,
            _userRewardPct=userRewardPct,
            _quantifierRewardPct=quantifierRewardPct,
            _rewardboardRewardPct=rewardboardRewardPct,
            _tokenName=tokenName,
            _tokenAddress=tokenAddress,
        )

    @classmethod
    def generate_from_dict(cls, _dict):
        """
        Recreates an existing instance of the rewards system from a dictionary. The dictionary must be structured like the class itself

        Args:
            (_dict): the the dictionary from which we want to instatiate the class from. Must contain all the class attributes.
        Raises:
            [TODO]: Check for errors and raise them
        Returns:
            cls: an instance of the class with the specified parameters


        """

        # REDO with new structure

        name = _dict["name"]
        praiseTable = _dict["praiseTable"]
        rewardboard = _dict["rewardboard"]
        quantPerPraise = _dict["quantPerPraise"]
        quantAllowedValues = _dict["quantAllowedValues"]
        duplicatePraiseValuation = _dict["duplicatePraiseValuation"]
        pseudonymsActive = _dict["pseudonymsActive"]
        userRewardPct = _dict["userRewardPct"]
        quantifierRewardPct = _dict["quantifierRewardPct"]
        rewardboardRewardPct = _dict["rewardboardRewardPct"]
        distAmount = _dict["distAmount"]
        tokenName = _dict["tokenName"]
        tokenAddress = _dict["tokenAddress"]
        distributionResults = _dict["distributionResults"]

        return cls(
            _name=name,
            _praiseTable=praiseTable,
            _rewardboard=rewardboard,
            _quantPerPraise=quantPerPraise,
            _quantAllowedValues=quantAllowedValues,
            _duplicatePraiseValuation=duplicatePraiseValuation,
            _pseudonymsActive=pseudonymsActive,
            _distAmount=distAmount,
            _userRewardPct=userRewardPct,
            _quantifierRewardPct=quantifierRewardPct,
            _rewardboardRewardPct=rewardboardRewardPct,
            _tokenName=tokenName,
            _tokenAddress=tokenAddress,
            _distributionResults=distributionResults,
        )

    def do_distribution(self) -> None:
        """
        Performs the reward distribution and saves it in object state under self.distribution results

        Args:
            (self): the object with initialized parameters
        Raises:
            [TODO]: Check for errors and raise them
        Returns:
            nothing. Changes local state of the object


        """

        # ONLY DOES PRAISE FOR NOW, integrate stragiht_dist for rewardboard

        # calc praise rewards
        # WILL PROBABLY NEED DEBUGGING  -> seems to work

        # calculate praise rewards and update the datatable

        praiseTokenAmount = self.distAmount * self.userRewardPct / 100

        praise_distribution = self.calc_praise_rewards(
            pd.DataFrame(self.praiseTable), praiseTokenAmount
        )

        self.praiseTable = pd.DataFrame.to_dict(praise_distribution)

        # Generate the final allocation including quant rewards and save it as distribution results
        quantTokenAmount = self.distAmount * self.quantifierRewardPct / 100

        praise_by_user = self.get_praise_by_user()
        quantifier_rating_table = self.get_data_by_quantifier()

        quant_rewards = self.calc_quantifier_rewards(
            quantifier_rating_table.copy(), quantTokenAmount
        )

        # generate rewardboard rewars here and send them to the next method

        final_token_allocations = self.prepare_merged_reward_table(
            praise_by_user.copy(), quant_rewards.copy()
        )

        self.distributionResults = pd.DataFrame.to_dict(final_token_allocations)

        # exports we want to build:
        # extended praise
        # final praise alloc
        # aragon_dist

        # print(quant_rewards)

        # save to file for testing purposes
        # filename = "TEST_PRAISE_EXPORT.csv"
        # final_allocation_csv = final_token_allocations.to_csv(sep=",", index=False)
        # with open(filename, "w") as f:
        #     f.write(final_allocation_csv)

        # filename = "TEST_QUANT_EXPORT.csv"
        # final_allocation_csv = quant_rewards.to_csv(sep=",", index=False)
        # with open(filename, "w") as f:
        #     f.write(final_allocation_csv)

        # filename = "TEST_EXTENDED_EXPORT.csv"
        # final_allocation_csv = praise_distribution.to_csv(sep=",", index=False)
        # with open(filename, "w") as f:
        #     f.write(final_allocation_csv)

    def calc_praise_rewards(self, praiseData, tokensToDistribute):
        # we discard all we don't need and and calculate the % worth of each praise

        totalPraisePoints = praiseData["AVG SCORE"].sum()

        praiseData["PERCENTAGE"] = praiseData["AVG SCORE"] / totalPraisePoints
        praiseData["TOKEN TO RECEIVE"] = praiseData["PERCENTAGE"] * tokensToDistribute

        return praiseData

    def get_praise_by_user(self):

        praiseData = pd.DataFrame(self.praiseTable)

        praiseData.rename(columns={"TO USER ACCOUNT": "USER IDENTITY"}, inplace=True)
        praiseData.rename(columns={"TO ETH ADDRESS": "USER ADDRESS"}, inplace=True)
        praiseData["USER ADDRESS"].fillna("MISSING USER ADDRESS", inplace=True)

        praise_by_user = (
            praiseData[
                [
                    "USER IDENTITY",
                    "USER ADDRESS",
                    "AVG SCORE",
                    "PERCENTAGE",
                    "TOKEN TO RECEIVE",
                ]
            ]
            .copy()
            .groupby(["USER IDENTITY", "USER ADDRESS"])
            .agg("sum")
            .reset_index()
        )

        return praise_by_user

    def calc_quantifier_rewards(self, quantifierData, tokensToDistribute):
        quantifier_sum = (
            quantifierData[["QUANT_ID", "QUANT_VALUE"]].groupby("QUANT_ID").sum()
        )
        norating_quantifiers = quantifier_sum.loc[
            quantifier_sum["QUANT_VALUE"] == 0
        ].index.tolist()

        quantifier_rewards = pd.DataFrame(
            quantifierData[["QUANT_ID", "QUANT_ADDRESS"]]
            .value_counts()
            .reset_index()
            .copy()
        )

        quantifier_rewards = quantifier_rewards[
            ~quantifier_rewards["QUANT_ID"].isin(norating_quantifiers)
        ]

        quantifier_rewards = quantifier_rewards.rename(
            columns={quantifier_rewards.columns[2]: "NUMBER_OF_PRAISES"}
        ).reset_index(drop=True)

        total_praise_quantified = quantifier_rewards["NUMBER_OF_PRAISES"].sum()
        quantifier_rewards["TOKEN TO RECEIVE"] = (
            quantifier_rewards["NUMBER_OF_PRAISES"]
            / total_praise_quantified
            * tokensToDistribute
        )

        return quantifier_rewards

    def get_data_by_quantifier(self):

        praise_data = pd.DataFrame(self.praiseTable)

        quant_only = pd.DataFrame()
        # praise_data.drop(['DATE', 'TO USER ACCOUNT', 'TO USER ACCOUNT ID', 'TO ETH ADDRESS', 'FROM USER ACCOUNT', 'FROM USER ACCOUNT ID', 'FROM ETH ADDRESS', 'REASON', 'SOURCE ID', 'SOURCE NAME', 'AVG SCORE'], axis=1, inplace=True)
        num_of_quants = self.quantPerPraise
        for i in range(num_of_quants):
            q_name = str("QUANTIFIER " + str(i + 1) + " USERNAME")
            q_addr = str("QUANTIFIER " + str(i + 1) + " ETH ADDRESS")
            q_value = str("SCORE " + str(i + 1))
            q_duplicate = str("DUPLICATE ID " + str(i + 1))

            buf = praise_data[["ID", q_name, q_addr, q_value, q_duplicate]].copy()

            # delete the duplicated rows
            buf = buf.loc[
                buf[q_duplicate].isnull()
            ]  # only include the non-duplicated rows
            buf = buf[
                ["ID", q_name, q_addr, q_value]
            ]  # don't need the duplication info anymore

            buf.rename(
                columns={
                    q_name: "QUANT_ID",
                    q_addr: "QUANT_ADDRESS",
                    q_value: "QUANT_VALUE",
                    "ID": "PRAISE_ID",
                },
                inplace=True,
            )

            quant_only = quant_only.append(buf.copy(), ignore_index=True)

        columnsTitles = ["QUANT_ID", "QUANT_ADDRESS", "PRAISE_ID", "QUANT_VALUE"]
        quant_only.sort_values(["QUANT_ID", "PRAISE_ID"], inplace=True)
        quant_only = quant_only.reindex(columns=columnsTitles).reset_index(drop=True)
        return quant_only

    # def return_total_data_chart
    def prepare_merged_reward_table(self, praise_rewards, quantifier_rewards):

        praise_rewards = praise_rewards.copy()[
            ["USER IDENTITY", "USER ADDRESS", "TOKEN TO RECEIVE"]
        ].rename(columns={"TOKEN TO RECEIVE": "PRAISE_REWARD"})
        praise_rewards["USER ADDRESS"] = praise_rewards["USER ADDRESS"].str.lower()

        quantifier_rewards.rename(
            columns={
                "QUANT_ADDRESS": "USER ADDRESS",
                "QUANT_ID": "USER IDENTITY",
                "NUMBER_OF_PRAISES": "NR_OF_PRAISES_QUANTIFIED",
                "TOKEN TO RECEIVE": "QUANT_REWARD",
            },
            inplace=True,
        )
        quantifier_rewards["USER ADDRESS"] = quantifier_rewards[
            "USER ADDRESS"
        ].str.lower()

        final_allocations = pd.merge(
            praise_rewards,
            quantifier_rewards,
            on=["USER ADDRESS", "USER ADDRESS"],
            how="outer",
        )

        # now we can merge the IDs, replacing any missing values
        final_allocations["USER IDENTITY_x"] = final_allocations[
            "USER IDENTITY_x"
        ].combine_first(final_allocations["USER IDENTITY_y"])
        final_allocations.rename(
            columns={"USER IDENTITY_x": "USER IDENTITY"}, inplace=True
        )
        final_allocations.drop("USER IDENTITY_y", axis=1, inplace=True)

        final_allocations["USER IDENTITY"].fillna("missing username", inplace=True)
        final_allocations.fillna(0, inplace=True)
        final_allocations["TOTAL TO RECEIVE"] = (
            final_allocations["PRAISE_REWARD"] + final_allocations["QUANT_REWARD"]
        )

        final_allocations = final_allocations.sort_values(
            by="TOTAL TO RECEIVE", ascending=False
        ).reset_index(drop=True)

        # put the columns into the desired order
        final_allocations = final_allocations[
            [
                "USER IDENTITY",
                "USER ADDRESS",
                "PRAISE_REWARD",
                "QUANT_REWARD",
                "NR_OF_PRAISES_QUANTIFIED",
                "TOTAL TO RECEIVE",
            ]
        ]

        return final_allocations
