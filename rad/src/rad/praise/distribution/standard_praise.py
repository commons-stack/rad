# STANDARD PRAISE DISTRIBUTION

# Instantiation of a praise distribution round

#   constructor:
#       -raw praise data and parameters -> executes reward distribution
#   has functions to return:
#       -praise distribution by user
#       -dataframe where praise is sorted by quantifier
#       -the praise megatable

import pandas as pd

from ...rewardDistribution import RewardDistribution
from ..praiseObj import Praise
from ...straight_distribution import StraightRewards


class PraiseDistribution(RewardDistribution):
    def __init__(
        self,
        _name,
        _praiseInstance,
        _rewardboardInstance,
        _maxDistAmount,
        _ceilingCutoff,
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
            _maxDistAmount: number, the amount of tokens to be distributed
            _tokenName: string indicating the name of the token the rewards will be paid out in
            _tokenAddress: the address of the reward token
            _distributionResults: Optional. Dictionary containing the results of a distribution.
        Raises:
            [TODO]: Check for errors and raise them
        Returns:
            nothing.

        """
        super().__init__(_name, "praise")
        self.praiseInstance = _praiseInstance
        self.rewardboardInstance = _rewardboardInstance

        self.userRewardPct = _userRewardPct
        self.quantifierRewardPct = _quantifierRewardPct
        self.rewardboardRewardPct = _rewardboardRewardPct
        self.maxDistAmount = int(_maxDistAmount)
        self.ceilingCutoff = int(_ceilingCutoff)
        self.totalDistributedTokens =  float(_maxDistAmount)
        if len(self.praiseInstance.dataTable) < self.ceilingCutoff:
            self.totalDistributedTokens = (
                len(self.praiseInstance.dataTable)
                / self.ceilingCutoff
                * self.totalDistributedTokens
            )
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
            "From str method of Praise: totalDistributedTokens is % s, tokenName is % s, results are % s"
            % (self.totalDistributedTokens, self.tokenName, str(self.distributionResults))
        )

    @classmethod
    def generate_from_params(cls, _objectName, _params, _sources):
        """
        Creates an instance of the rewards system from the parameters as speified in the "parameters.json" file.

        Args:
            (_params): a dictionary from which we want to instatiate the class from. Loaded from the parameters.json file.
            _sources: existing reward system objects
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
            if _sources[obj].type == "praise" and praiseObj == {}:
                praiseObj = _sources[obj]
            if _sources[obj].type == "straight_distribution" and rewardObj == {}:
                rewardObj = _sources[obj]

        maxDistAmount = _params["max_distribution_amount"]
        ceilingCutoff = _params["ceiling_cutoff"]
        userRewardPct = _params["user_dist_pct"]
        quantifierRewardPct = _params["quantifiers_dist_pct"]
        rewardboardRewardPct = _params["reward_dist_pct"]
        tokenName = _params["payout_token"]["token_name"]
        tokenAddress = _params["payout_token"]["token_address"]

        return cls(
            _name=_objectName,
            _praiseInstance=praiseObj,
            _rewardboardInstance=rewardObj,
            _maxDistAmount=maxDistAmount,
            _ceilingCutoff=ceilingCutoff,
            _userRewardPct=userRewardPct,
            _quantifierRewardPct=quantifierRewardPct,
            _rewardboardRewardPct=rewardboardRewardPct,
            _tokenName=tokenName,
            _tokenAddress=tokenAddress,
        )

    @classmethod
    def import_from_dict(cls, _dict):
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
        praiseObj = Praise.import_from_dict(_dict["praiseInstance"])
        rewardboardObj = StraightRewards.import_from_dict(_dict["rewardboardInstance"])

        userRewardPct = _dict["userRewardPct"]
        quantifierRewardPct = _dict["quantifierRewardPct"]
        rewardboardRewardPct = _dict["rewardboardRewardPct"]
        maxDistAmount = _dict["maxDistAmount"]
        ceilingCutoff = _dict["ceilingCutoff"]
        totalDistributedTokens = dict["totalDistributedTokens"] 
        tokenName = _dict["tokenName"]
        tokenAddress = _dict["tokenAddress"]
        distributionResults = _dict["distributionResults"]

        return cls(
            _name=name,
            _praiseInstance=praiseObj,
            _rewardboardInstance=rewardboardObj,
            _maxDistAmount=maxDistAmount,
            _ceilingCutoff=ceilingCutoff,
            _totalDistributedTokens=totalDistributedTokens,
            _userRewardPct=userRewardPct,
            _quantifierRewardPct=quantifierRewardPct,
            _rewardboardRewardPct=rewardboardRewardPct,
            _tokenName=tokenName,
            _tokenAddress=tokenAddress,
            _distributionResults=distributionResults,
        )

    @classmethod
    def export_to_dict(cls, self):

        exp_dict = super().export_to_dict(self)

        exp_dict["praiseInstance"] = self.praiseInstance.export_to_dict(
            self.praiseInstance
        )
        exp_dict["rewardBoardInstance"] = self.rewardboardInstance.export_to_dict(
            self.rewardboardInstance
        )

        exp_dict["userRewardPct"] = self.userRewardPct
        exp_dict["quantifierRewardPct"] = self.quantifierRewardPct
        exp_dict["rewardboardRewardPct"] = self.rewardboardRewardPct
        exp_dict["maxDistAmount"] = self.maxDistAmount
        exp_dict["totalDistributedTokens"] = self.totalDistributedTokens
        exp_dict["tokenName"] = self.tokenName
        exp_dict["tokenAddress"] = self.tokenAddress
        exp_dict["distributionResults"] = self.distributionResults

        return exp_dict

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

        # if the amount of praise is below the cutoff, adapt number of distributed tokens
        total_tokens_allocated = self.maxDistAmount
        if len(self.praiseInstance.dataTable) < self.ceilingCutoff:
            total_tokens_allocated = (
                len(self.praiseInstance.dataTable)
                / self.ceilingCutoff
                * float(total_tokens_allocated)
            )

        praiseTokenAmount = self.totalDistributedTokens * self.userRewardPct / 100
        quantTokenAmount = self.totalDistributedTokens * self.quantifierRewardPct / 100

        praise_by_user = self.praiseInstance.get_praise_by_user()

        praise_by_user["TOKEN TO RECEIVE"] = (
            praise_by_user["PERCENTAGE"] * praiseTokenAmount
        )

        quantifier_rating_table = self.praiseInstance.get_data_by_quantifier()

        quant_rewards = self.calc_quantifier_rewards(
            quantifier_rating_table.copy(), quantTokenAmount
        )

        # generate rewardboard rewards here and send them to the next method

        final_token_allocations = self.prepare_merged_reward_table(
            praise_by_user.copy(), quant_rewards.copy()
        )

        self.distributionResults = pd.DataFrame.to_dict(final_token_allocations)



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
