# from . import *
from .straight_distribution import *

# from .straight_distribution import StraightDistribution
# from .sourcecred import Sourcecred

import pandas as pd


# [TODO] reasses if there is a better way to do this


def build_reward_object(_name, _params):
    if _name == "praise":
        # return create_praise_object(_params)
        print("praise not implemented")
        pass
    if _name == "straight_distribution":
        return create_straight_distribution_object(_params)
    if _name == "sourcecred":
        # return create_sourcecred_object(_params)
        print("sourcecred not implemented")
        pass


def create_straight_distribution_object(_params):
    return StraightDistribution.generate_from_params(_params)
