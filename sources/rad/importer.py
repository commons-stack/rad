# TO DO: Implement.

# def load_sources_from_json(path):
# This method will contain the logic to load all reward objects specified in a JSON file and return them as an array for further processing. A big part of the implmentation already exists in main.py

# def load_dist_conf_from_json(path):
# This method will contain the logic to load the necessary configuration paramaters to perform a distribution over an existing rewards object. A big part of the implementation already exists in main.py, although furher development on the praiseDistribtion class will probably be necessary.

# def load_exports_from_json(path):
# This method will contain the logic to load the necessary configuration to execte all the exports from an existing distribution object. A part of the implmentation already exists in main.py

import os
import json
from natsort import natsorted

from . import rewardObjectBuilder as objBuilder
from . import distributionObjectBuilder as distBuilder

# import src.notebookbuilder as nbBuilder
# import src.exporter as exportBuilder


def load_sources_from_json(_fullPath):

    input_path, input_name = os.path.split(_fullPath)

    params = {}
    with open(_fullPath, "r") as read_file:
        params = json.load(read_file)

    rewardsystem_objects = {}
    for reward_system in params["sources"]:
        # make sure the notebook finds the path to the files
        for file in params["sources"][reward_system]["input_files"]:
            params["sources"][reward_system]["input_files"][file] = os.path.abspath(
                os.path.join(
                    input_path, params["sources"][reward_system]["input_files"][file]
                )
            )
        # create rewards Object
        rewardsystem_objects[reward_system] = objBuilder.build_reward_object(
            reward_system,
            params["sources"][reward_system]["type"],
            params["sources"][reward_system],
        )

    distribution_objects = {}
    for distribution in params["distributions"]:
        dist_sources = {}
        for source in params["distributions"][distribution]["sources"]:
            dist_sources[source] = rewardsystem_objects[source]

        distribution_objects[distribution] = distBuilder.build_distribution_object(
            distribution,
            params["distributions"][distribution]["type"],
            params["distributions"][distribution],
            dist_sources,
        )
    # print(distribution_objects)

    return (rewardsystem_objects, distribution_objects)


def load_from_file_list(file_list):

    rwdObjs = {}
    rwdDists = {}

    for file in file_list:
        # load data and append to array
        (buf_obj, buf_dist) = load_sources_from_json(file)

        for obj in buf_obj:
            if buf_obj[obj].type not in rwdObjs:
                rwdObjs[buf_obj[obj].type] = [buf_obj[obj]]
            else:
                rwdObjs[buf_obj[obj].type].append(buf_obj[obj])
        for dist in buf_dist:
            if buf_dist[dist].type not in rwdDists:
                rwdDists[buf_dist[dist].type] = [buf_dist[dist]]
            else:
                rwdDists[buf_dist[dist].type].append(buf_dist[dist])

    return (rwdObjs, rwdDists)


# create method load_dicts_from_buffer(path, list[])


def load_multiple_periods(_fullPath):

    # load the parameters for the cross_period:
    input_path, input_name = os.path.split(_fullPath)

    params = {}
    with open(_fullPath, "r") as read_file:
        params = json.load(read_file)

    _cross_period_root = params["report_settings"]["cross_period_settings"]["data"]
    _mode = params["report_settings"]["cross_period_settings"]["mode"]

    # config mode: file list or root_folder

    # goes through folders in _cross_period_root / file list

    rwdObjs = {}
    rwdDists = {}

    if _mode == "file_list":
        (rwdObjs, rwdDists) = load_from_file_list(_cross_period_root)

    elif _mode == "root_folder":

        # create the file list

        # dirname = os.path.dirname(input_path)
        datadir = os.path.join(input_path, _cross_period_root)

        # datadir = _cross_period_root
        foldername_list = natsorted(os.listdir(datadir))
        file_list = []

        for round_name in foldername_list:
            # load params.jon file and append to array
            if not os.path.isdir(f"{datadir}/{round_name}"):
                # not a folder
                continue
            if not os.path.exists(f"{datadir}/{round_name}/parameters.json"):
                # not a round folder
                continue
            round_path = f"{datadir}/{round_name}/parameters.json"
            file_list.append(round_path)

        (rwdObjs, rwdDists) = load_from_file_list(file_list)

    return (rwdObjs, rwdDists)
