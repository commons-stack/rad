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
import src.exporter as exportBuilder


def run_rad(_inputPath):

    _inputParameters = _inputPath + "/parameters.json"

    params = {}
    with open(_inputParameters, "r") as read_file:
        params = json.load(read_file)

    rewardsystem_objects = {}
    for reward_system in params["rewards"]:
        # make sure the notebook finds the path to the files
        for file in params["rewards"][reward_system]["input_files"]:
            params["rewards"][reward_system]["input_files"][file] = os.path.abspath(
                os.path.join(
                    input_path, params["rewards"][reward_system]["input_files"][file]
                )
            )

        # create rewards Object
        rewardsystem_objects[reward_system] = objBuilder.build_reward_object(
            reward_system,
            params["rewards"][reward_system]["type"],
            params["rewards"][reward_system],
        )
        # print(rewardsystem_objects[reward_system].get_distribution_results())

    for template_name in params["reports"]:
        # add all relevant praise objects to the input and build the notebook
        _data = {}
        for source_system in params["reports"][template_name]["sources"]:
            _data[source_system] = rewardsystem_objects[source_system]
        nbBuilder.build_and_run(template_name, _data)

    # [TODO] for export in params["exports"]
    for export in params["exports"]:
        _data = {}
        for source_system in params["reports"][export]["sources"]:
            _data[source_system] = rewardsystem_objects[source_system]
        exportBuilder.run_export(export, _data)

    # [TODO] Save the different kinds of exports at different places, or handle as separately
    for output_file in os.listdir():
        if output_file.endswith(".csv"):
            file_destination = _inputPath + "/my_reports/" + output_file
            os.rename(output_file, file_destination)

        if output_file.endswith(".html"):
            file_destination = _inputPath + "/my_reports/" + output_file
            os.rename(output_file, file_destination)

        if output_file.endswith(".ipynb"):
            file_destination = _inputPath + "/my_reports/" + output_file
            os.rename(output_file, file_destination)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="RAD main script")
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        required=True,
        help="Path to the folder in which we'll perform the analysis",
    )
    args = parser.parse_args()

    input_path = args.path
    # quick conveniency check
    input_path = input_path if input_path[-1] == "/" else (input_path + "/")

    run_rad(input_path)
