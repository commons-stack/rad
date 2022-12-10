import json, os
from . import importer
import importlib
from importlib.metadata import distribution


def process_all_exports(parameters_path, output_path):
    params = {}
    all_filenames = []
    with open(parameters_path, "r") as read_file:
        params = json.load(read_file)
    if "exports" in params:

        (reward_system_objects, distribution_objects) = importer.load_sources_from_json(
            parameters_path
        )

        for export in params["exports"]:
            _data = {}
            for source_system in params["exports"][export]["sources"]:
                _data[source_system] = distribution_objects[source_system]

            new_files = run_export(export, params["exports"][export], _data)
            # [all_filenames.append(item) for item in new_files]
            all_filenames += new_files

    # move all the generated files to the right folder
    for filename in all_filenames:
        # print(filename)
        file_destination = output_path + filename
        os.rename(filename, file_destination)


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
        distObj = _data[_config["sources"][0]]
        return run_single_export(_name, _config, distObj)
    else:
        return run_combined_export(_name, _config, _data)


def run_single_export(_name, _config, _distObj):
    """
    Runs a specified export scirpt for a specific dataset

        Args:
            _name: user-defined name of the export (for the filename etc)
            _config: dict with configuration data specifying the type of export and the source objects
            _data: the necessary data to generate it
        Raises:
            [TODO] Implement errors and list them here.
        Returns:
            the names of the saved files
    """

    PATH_TO_MODULE = "rad." + _distObj.type + ".export." + _config["type"]
    mod = importlib.import_module(PATH_TO_MODULE)

    return mod.save_export(_name, _distObj, _config)


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
    print(f"{_name}: Multi-system export not yet implemented. Pass")
    return []
