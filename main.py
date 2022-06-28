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


import argparse, os
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
# declare the paths where we want to save stuff as constants for easy reference
ROOT_INPUT_PATH = args.path


# quick conveniency check
ROOT_INPUT_PATH = ROOT_INPUT_PATH if ROOT_INPUT_PATH[-1] == "/" else (
    ROOT_INPUT_PATH+"/")


input_parameters = ROOT_INPUT_PATH + "/parameters.json"




params = {}
with open(input_parameters, "r") as read_file:
    params = json.load(read_file)

rewardsystem_objects = {}
for reward_system in params["rewards"]:
    # make sure the notebook finds the path to the files
    for file in params["rewards"][reward_system]["input_files"]:
        params["rewards"][reward_system]["input_files"][file] = os.path.abspath(
            os.path.join(ROOT_INPUT_PATH, params["rewards"][reward_system]["input_files"][file])) 
            
    # create rewards Object
    rewardsystem_objects[reward_system] = objBuilder.build_reward_object(
        params["rewards"][reward_system]["type"], params["rewards"][reward_system])
    #print(rewardsystem_objects[reward_system].get_distribution_results())


# for template in params["reports"]:
for template_name in params["reports"]:

    # create list of necessary inputs (it will receive all necessary praise objects as input)
    _data = {}
    for source_system in params["reports"][template_name]["sources"]:
        _data[source_system] = rewardsystem_objects[source_system]
    nbBuilder.build_and_run(template_name, _data)


# for export in params["exports"]
    # run export

# move files to destination folder and clean up
