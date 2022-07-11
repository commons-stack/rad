# PRAISE SYSTEM OBJECT

# Instantiation of a praise round

#   constructor:
#       -raw praise data and parameters -> executes reward distribution
#   has functions to return:
#       -praise distribution by user
#       -dataframe where praise is sorted by quantifier
#       -the praise megatable

from tokenize import Number
import pandas as pd

from src.rewardSystem import RewardSystem


class Praise(RewardSystem):
    def __init__(
        self,
        _name,
        _dataTable,
        _quantPerPraise,
        _quantAllowedValues,
        _duplicatePraiseValuation,
        _pseudonymsActive,
        _distAmount,
        _userRewardPct,
        _quantifierRewardPct,
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
        self.dataTable = _dataTable
        self.quantPerPraise = int(_quantPerPraise)
        self.quantAllowedValues = _quantAllowedValues
        self.duplicatePraiseValuation = Number(_duplicatePraiseValuation)
        self.pseudonymsActive = bool(_pseudonymsActive)
        self.userRewardPct = _userRewardPct
        self.quantifierRewardPct = _quantifierRewardPct
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
    def generate_from_params(cls, _objectName, _params):
        """
        Creates an instance of the rewards system from the parameters as speified in the "parameters.json" file.

        Args:
            (_params): a dictionary from which we want to instatiate the class from. Loaded from the parameters.json file.
        Raises:
            [TODO]: Check for errors and raise them
        Returns:
            cls: an instance of the class with the specified parameters

        """

        dataTable_input = pd.read_csv(_params["input_files"]["praise_data"])
        # lets pipe this through pandas to be sure we don't run into issues
        dataTable = pd.DataFrame.to_dict(dataTable_input)

        quantPerPraise = _params["quantifiers_per_praise"]
        quantAllowedValues = _params["praise_quantify_allowed_values"]
        duplicatePraiseValuation = _params["duplicate_praise_valuation"]
        pseudonymsActive = _params["pseudonyms_used"]

        distAmount = _params["distribution_amount"]
        userRewardPct = _params["user_dist_pct"]
        quantifierRewardPct = _params["quantifiers_dist_pct"]

        tokenName = _params["payout_token"]["token_name"]
        tokenAddress = _params["payout_token"]["token_address"]

        return cls(
            _name=_objectName,
            _dataTable=dataTable,
            _quantPerPraise=quantPerPraise,
            _quantAllowedValues=quantAllowedValues,
            _duplicatePraiseValuation=duplicatePraiseValuation,
            _pseudonymsActive=pseudonymsActive,
            _distAmount=distAmount,
            _userRewardPct=userRewardPct,
            _quantifierRewardPct=quantifierRewardPct,
            _tokenName=tokenName,
            _tokenAddress=tokenAddress,
        )

    @classmethod
    def generate_from_dict(cls, _dict):
        """
        Creates an instance of the rewards system from a dictionary. The dictionary must be structured like the class itself

        Args:
            (_dict): the the dictionary from which we want to instatiate the class from. Must contain all the class attributes.
        Raises:
            [TODO]: Check for errors and raise them
        Returns:
            cls: an instance of the class with the specified parameters


        """

        # REDO with new structure

        name = _dict["name"]
        dataTable = _dict["dataTable"]
        quantPerPraise = _dict["quantPerPraise"]
        quantAllowedValues = _dict["quantAllowedValues"]
        duplicatePraiseValuation = _dict["duplicatePraiseValuation"]
        pseudonymsActive = _dict["pseudonymsActive"]
        userRewardPct = _dict["userRewardPct"]
        quantifierRewardPct = _dict["quantifierRewardPct"]
        distAmount = _dict["distAmount"]
        tokenName = _dict["tokenName"]
        tokenAddress = _dict["tokenAddress"]
        distributionResults = _dict["distributionResults"]

        return cls(
            _name=name,
            _dataTable=dataTable,
            _quantPerPraise=quantPerPraise,
            _quantAllowedValues=quantAllowedValues,
            _duplicatePraiseValuation=duplicatePraiseValuation,
            _pseudonymsActive=pseudonymsActive,
            _distAmount=distAmount,
            _userRewardPct=userRewardPct,
            _quantifierRewardPct=quantifierRewardPct,
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

        # calc praise rewards
        # WILL PROBABLY NEED DEBUGGING

        praiseTokenAmount = self.distAmount * self.userRewardPct / 100
        quantTokenAmount = self.distAmount * self.quantifierRewardPct / 100

        praise_distribution = calc_praise_rewards(
            self.dataTable.copy(), praiseTokenAmount
        )
		
	#Process praise to merge it with quant rewards
        processed_praise, praise_by_user = prepare_praise(praise_distribution.copy())

        quantifier_rating_table = return_data_by_quantifier(self.dataTable.copy())

        quant_rewards = calc_quantifier_rewards(
            quantifier_rating_table.copy(), quantTokenAmount
        )

        final_token_allocations = prepare_total_data_chart(
            praise_by_user.copy(), quant_rewards.copy()
        )

        # [TODO] Choose what to save in object state (do we need dataTable or is processed_praise enough?)

    def calc_praise_rewards(praiseData, tokensToDistribute):
        # we discard all we don't need and and calculate the % worth of each praise

        totalPraisePoints = praiseData["AVG SCORE"].sum()

        praiseData["PERCENTAGE"] = praiseData["AVG SCORE"] / totalPraisePoints
        praiseData["TOKEN TO RECEIVE"] = praiseData["PERCENTAGE"] * tokensToDistribute
        return praiseData

    def prepare_praise(praise_data):

        praise_data.rename(columns={"TO USER ACCOUNT": "USER IDENTITY"}, inplace=True)
        praise_data.rename(columns={"TO ETH ADDRESS": "USER ADDRESS"}, inplace=True)
        praise_data["USER ADDRESS"].fillna("MISSING USER ADDRESS", inplace=True)

        processed_praise = praise_data[
            ["USER IDENTITY", "USER ADDRESS", "PERCENTAGE", "TOKEN TO RECEIVE"]
        ]
        praise_by_user = (
            praise_data[
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

        return processed_praise, praise_by_user

    def calc_quantifier_rewards(quantifierData, tokensToDistribute):
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

    def return_data_by_quantifier(praise_data):
        quant_only = pd.DataFrame()
        # praise_data.drop(['DATE', 'TO USER ACCOUNT', 'TO USER ACCOUNT ID', 'TO ETH ADDRESS', 'FROM USER ACCOUNT', 'FROM USER ACCOUNT ID', 'FROM ETH ADDRESS', 'REASON', 'SOURCE ID', 'SOURCE NAME', 'AVG SCORE'], axis=1, inplace=True)
        num_of_quants = NUMBER_OF_QUANTIFIERS_PER_PRAISE
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
    def prepare_total_data_chart(
        praise_rewards, quantifier_rewards, rewardboard_rewards
    ):

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

        rewardboard_rewards.rename(
            columns={"ID": "USER ADDRESS", "TOKEN TO RECEIVE": "REWARDBOARD_REWARD"},
            inplace=True,
        )
        rewardboard_rewards["USER ADDRESS"] = rewardboard_rewards[
            "USER ADDRESS"
        ].str.lower()

        final_allocations = pd.merge(
            rewardboard_rewards,
            quantifier_rewards,
            on=["USER ADDRESS", "USER ADDRESS"],
            how="outer",
        )
        final_allocations = pd.merge(
            final_allocations,
            praise_rewards,
            left_on=["USER ADDRESS"],
            right_on=["USER ADDRESS"],
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
            final_allocations["PRAISE_REWARD"]
            + final_allocations["QUANT_REWARD"]
            + final_allocations["REWARDBOARD_REWARD"]
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
                "REWARDBOARD_REWARD",
                "TOTAL TO RECEIVE",
            ]
        ]

        return final_allocations
