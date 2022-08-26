# STRAIGHT DISTRIBUTION
# This system represents a simple rewards system where everybody shares a set amount of funds equally

import pandas as pd


from src.rewardDistribution import RewardDistribution
from reward_systems.praise import Praise
from reward_systems.straight_distribution.straightRewards import StraightRewards


class StraightDistribution(RewardDistribution):
    def __init__(
        self,
        _name,
        _beneficiaries,
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
        super().__init__(_name, "straight_distribution")
        self.beneficiaries = _beneficiaries

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
            "From str method of StrightDistr: totalDistAmount is % s, tokenName is % s, results are % s"
            % (self.totalDistAmount, self.tokenName, str(self.distribution_results))
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
        # [TODO] prepare for receiving multiple sources and combining them
        beneficiaries_input = pd.DataFrame()
        for obj in _sources:
            beneficiaries_input = pd.concat(
                [beneficiaries_input, pd.DataFrame(_sources[obj].beneficiaries)]
            )
        # lets pipe this through pandas to be sure we don't run into issues
        beneficiaries = pd.DataFrame.to_dict(beneficiaries_input)

        return cls(
            _name=_objectName,
            _beneficiaries=beneficiaries,
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
        name = _dict["name"]
        beneficiaries = _dict["beneficiaries"]

        return cls(
            _name=name,
            _beneficiaries=beneficiaries,
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

        dist_results = pd.DataFrame.from_dict(self.beneficiaries)
        dist_results["AMOUNT TO RECEIVE"] = self.totalDistAmount / len(
            dist_results.index
        )
        self.distributionResults = pd.DataFrame.to_dict(dist_results)
