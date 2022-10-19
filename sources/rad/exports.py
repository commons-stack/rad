#
# ====================
#  BIG REVIEW PENDING
# ====================
#


import importlib
from importlib.metadata import distribution

# from .rewardSystem import RewardSystem


def run_export(_name, _config, _data):
    """
    Main entry point to the module. Checks if the export will involve just one rewards system or require combining results from several different ones.

        Args:
            _name: user-defined name of the export (for the filename etc)
            _config: dict with configuration data specifying the type of export and the source objects
            _data: the necessary data to generate it
        Raises:
            [TODO] Implement errors and list them here.
        Returns:
            nothing, just saves the files
    """

    if len(_config["sources"]) == 1:
        rewardObj = _data[_config["sources"][0]]
        run_single_export(_name, _config, rewardObj)
    else:
        run_combined_export(_name, _config, _data)


def run_single_export(_name, _config, _rewardObj):
    """
    Runs a specified export scirpt for a specific dataset

        Args:
            _name: user-defined name of the export (for the filename etc)
            _config: dict with configuration data specifying the type of export and the source objects
            _data: the necessary data to generate it
        Raises:
            [TODO] Implement errors and list them here.
        Returns:
            nothing, just saves the files
    """

    PATH_TO_MODULE = "reward_systems." + _rewardObj.type + ".exports." + _config["type"]
    mod = importlib.import_module(PATH_TO_MODULE)

    export_file, export_extension = mod.run_export(_rewardObj, _config)

    # filename = "export_" + _name + "_" + _config["type"] + ".csv"
    filename = _name + export_extension
    with open(filename, "w") as f:
        f.write(export_file)

    return


def run_combined_export(_name, _config, _data):
    """
    Runs a specified export scirpt for a several datasets and combines the result

        Args:
            _name: user-defined name of the export (for the filename etc)
            _config: dict with configuration data specifying the type of export and the source objects
            _data: the necessary data to generate it
        Raises:
            [TODO] Implement errors and list them here.
        Returns:
            nothing, just saves the files
    """
    # [TODO] Implement this
    print("Multi-system export not yet implemented. Pass")
    pass
