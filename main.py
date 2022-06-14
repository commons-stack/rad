# MAIN COORDINATOR SCRIPT

# This program:
#   -Takes the Paramter JSON file
#   -Loads the data from the addresses specified there
#   -Creates object instances of every employed rewards system
#   -loops through all the specifed analysis notebook reports, sending them the necessary data objects
#       - executed notebooks get saved
#   - loops through all the specified exports
#      - the data for the exports can be sourced either from the reward object of from the analysis (maybe?)
#      - exports get saved
#   -moves all the exports + notebooks to the correct output folder
#   -cleans up


import pandas as pd
import numpy as np
import json

import argparse


parser = argparse.ArgumentParser(
    description='RAD main script')
parser.add_argument("-p", "--path", type=str, required=True,
                    help="Path to the folder in which we'll perform the analysis")

args = parser.parse_args()
input_parameters = args.path + "/parameters.json"


params = {}
with open(input_parameters, "r") as read_file:
    params = json.load(read_file)


# for reward_system in params["reward_systems"]
    # create rewards Object

# for template in params["reports"]:
    # create list of necessary
    notebookbuilder.build()
