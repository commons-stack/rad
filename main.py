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


import argparse
import pandas as pd
import numpy as np
import json

import reward_systems.rewardObjectBuilder as objBuilder
import src.notebookbuilder as nbBuilder


parser = argparse.ArgumentParser(
    description='RAD main script')
parser.add_argument("-p", "--path", type=str, required=True,
                    help="Path to the folder in which we'll perform the analysis")

args = parser.parse_args()
input_parameters = args.path + "/parameters.json"


params = {}
with open(input_parameters, "r") as read_file:
    params = json.load(read_file)

rewardsystem_objects = {}
for reward_system in params["rewards"]:
    # create rewards Object
    rewardsystem_objects[reward_system] = objBuilder.build_reward_object(
        params["rewards"][reward_system]["type"], params["rewards"][reward_system])
    print(rewardsystem_objects[reward_system])


# for template in params["reports"]:
for template in params["reports"]:
    # create template path (for builder to find it)
    path_to_template = "./reward_systems/" + \
        params["reports"][template]["system"] + "/reports/" + \
        params["reports"][template]["name"] + "/"
    # create list of necessary inputs (it will receive all necessary praise objects as input)
    _data = {}
    for source_system in params["reports"][template]["sources"]:
        _data[source_system] = rewardsystem_objects[source_system]
    nbBuilder.build_and_run(path_to_template, _data)


# for export in params["exports"]
    # run export

# move files to destination folder and clean up
