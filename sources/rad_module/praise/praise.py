# PRAISE SYSTEM OBJECT

# Instantiation of a raw praise epoch

#   constructor:
#       -raw praise data and parameters
#   has functions to return:
#       -praise distribution by user
#       -dataframe where praise is sorted by quantifier
#       -the praise megatable

from tokenize import Number
import pandas as pd
import json
import os
from ..rewardSystem import RewardSystem


class Praise(RewardSystem):
    def __init__(
        self,
        _name,
        _dataTable,
        _quantPerPraise,
        _quantAllowedValues,
        _duplicatePraiseValuation,
        _pseudonymsActive,
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
        self.duplicatePraiseValuation = float(_duplicatePraiseValuation)
        self.pseudonymsActive = bool(_pseudonymsActive)

        self.calc_percentages()

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

        # [TODO] Redo for new format, right now it breaks
        return (
            "From str method of Praise: quantPerPraise is % s, duplicate Praise valuation is % s"
            % (self.quantPerPraise, self.duplicatePraiseValuation)
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

        return cls(
            _name=_objectName,
            _dataTable=dataTable,
            _quantPerPraise=quantPerPraise,
            _quantAllowedValues=quantAllowedValues,
            _duplicatePraiseValuation=duplicatePraiseValuation,
            _pseudonymsActive=pseudonymsActive,
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
        dataTable = _dict["dataTable"]
        quantPerPraise = _dict["quantPerPraise"]
        quantAllowedValues = _dict["quantAllowedValues"]
        duplicatePraiseValuation = _dict["duplicatePraiseValuation"]
        pseudonymsActive = _dict["pseudonymsActive"]

        return cls(
            _name=name,
            _dataTable=dataTable,
            _quantPerPraise=quantPerPraise,
            _quantAllowedValues=quantAllowedValues,
            _duplicatePraiseValuation=duplicatePraiseValuation,
            _pseudonymsActive=pseudonymsActive,
        )

    @classmethod
    def load_from_json(cls, _path):
        params = {}
        with open(_path, "r") as read_file:
            params = json.load(read_file)

        _path = os.path.split(_path)

        params["input_files"]["praise_data"] = os.path.abspath(
            os.path.join(_path[0], params["input_files"]["praise_data"])
        )

        return cls.generate_from_params(params["name"], params)

    def calc_percentages(self):

        pctTable = pd.DataFrame(self.dataTable)

        totalPraisePoints = pctTable["AVG SCORE"].sum()
        pctTable["PERCENTAGE"] = pctTable["AVG SCORE"] / totalPraisePoints

        self.dataTable = pctTable.to_dict()

    def get_praise_by_user(self):
        """
        Returns a DataFrame of the total praise score received by each user
        Args:
           - None
        Raises:
            [TODO]: Check for errors and raise them
        Returns:
            praise_by_user: DataFrame containing name, address, total praise points and corresponding % for all users

        """

        praiseData = pd.DataFrame(self.dataTable)

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
                ]
            ]
            .copy()
            .groupby(["USER IDENTITY", "USER ADDRESS"])
            .agg("sum")
            .reset_index()
        )

        return praise_by_user

    def get_data_by_quantifier(self):
        """
        Returns a DataFrame of the praise sorted by quantifier
        Args:
           - None
        Raises:
            [TODO]: Check for errors and raise them
        Returns:
            quant_only: DataFrame containing name, address and score given by that quantifier for all praise

        """

        praise_data = pd.DataFrame(self.dataTable)

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
