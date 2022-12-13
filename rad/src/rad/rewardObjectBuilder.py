from .praise import Praise
from .straight_distribution import *


import pandas as pd


# [TODO] reasses if there is a better way to do this. Probably some kind of enum?


def build_reward_object(_name, _type, _params):
    """
    Creates a reward system object of a specfic type

    Args:
        _name: String specifying the name of the reward system
        _params: the parameters with which to instantiate it
    Raises:
        [TODO]: Check for errors and raise them
    Returns:
        cls: An instance of the rewards system

    """
    if _type == "praise":
        # return create_praise_object(_params)
        return create_praise_object(_name, _params)
    if _type == "straight_distribution":
        return create_straight_distribution_object(_name, _params)
    if _type == "sourcecred":
        # return create_sourcecred_object(_params)
        print("sourcecred not implemented")
        pass


def create_straight_distribution_object(_name, _params):
    """
    Creates a straight distribution object

    Args:
        _params: the parameters with which to instantiate it
    Raises:
        [TODO]: Check for errors and raise them
    Returns:
        cls: An instance of a straight rewards distribution
    """
    str = StraightRewards.generate_from_params(_name, _params)
    return str


def create_praise_object(_name, _params):
    """
    Creates a Praise object

    Args:
        _params: the parameters with which to instantiate it
    Raises:
        [TODO]: Check for errors and raise them
    Returns:
        cls: An instance of a straight rewards distribution
    """
    pr = Praise.generate_from_params(_name, _params)
    return pr
