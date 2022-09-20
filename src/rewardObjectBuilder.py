# from . import *
from sources.praise.praise import Praise
from ..sources.straight_distribution import *

# from .straight_distribution import StraightDistribution
# from .sourcecred import Sourcecred

import pandas as pd


# [TODO] reasses if there is a better way to do this


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
    return StraightRewards.generate_from_params(_name, _params)


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
    return Praise.generate_from_params(_name, _params)
