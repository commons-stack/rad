# Runs through the JSON as calls all export functions, combines stuff when necessary and saves it. Moves stuff at the end if necessary


import importlib
from importlib.metadata import distribution

# from .rewardSystem import RewardSystem

"""
Runs a specified export scirpt for a specific dataset

    Args:
        _name: user-defined name of the export (for the filename etc)
        _data: the necessary data to generate it
    Raises:
        [TODO] Implement errors and list them here.
    Returns:
        nothing, just saves the files
"""


def run_export(_name, _config, _data):
    if len(_config["sources"]) == 1:
        rewardObj = _data[_config["sources"][0]]
        run_single_export(_name, _config, rewardObj)
    else:
        run_combined_export(_name, _config, _data)


def run_single_export(_name, _config, _rewardObj):

    PATH_TO_MODULE = "reward_systems." + _rewardObj.type + ".exports." + _config["type"]
    mod = importlib.import_module(PATH_TO_MODULE)

    final_allocation_csv = mod.run_export(_rewardObj, _config)

    filename = "export_" + _name + "_" + _config["type"] + ".csv"
    with open(filename, "w") as f:
        f.write(final_allocation_csv)

    return


def run_combined_export(_name, _config, _data):
    # TODO
    print("Multi-system export not yet implemented. Pass")
    pass
