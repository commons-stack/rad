# STRAIGHT DISTRIBUTION
# This system represents a simple rewards system where everybody shares a set amount of funds equally

import pandas as pd

from src.rewardSystem import RewardSystem


class StraightRewards(RewardSystem):
    def __init__(
        self,
        _name,
        _beneficiaries,
    ):
        """
        The class constructor

        Args:
            _benficiaries: list of the users participating in the reward system
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
            "This is a Straight Distribution Object. It contains a list of % s beneficiaries"
            % (len(self.beneficiaries))
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
        beneficiaries_input = pd.read_csv(_params["input_files"]["beneficiary_list"])
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
