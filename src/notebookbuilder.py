from sys import path
import subprocess
import nbformat as nbf
import importlib
import json
import papermill as pm


def build_and_run(_templateName, _templateType, _data):
    """
    Builds and runs a notebook from a specified template and dataset

    Args:
        _templateName(string): The name of the report notebook we want to generate.
        _templateType(string): The name of the template we'll use to build it. Must match the folder name where the JSON specification of the template is stored.
        _data(RewardSystem):  A list of all reward system objects necessary to run the analysis notebook

    Raises:
        [TODO] Implement errors and list them here.

    Returns:
        result(bool): True if everything worked correctly.

    Stores:
        report instance (.html): An instance of the chosen analysis report in HTML format. This is a non-modifiable export of the generated notebook, while keeping the interactive graphs.
        output_notebook(.ipynb): A copy of the generated notebook in executed state with the relevant data imported through the papermill library for easy re-running.


    """

    path_to_report = "./reports/" + _templateType + "/"
    parameters_path = path_to_report + _templateType + ".json"

    parameters = {}
    with open(parameters_path, "r") as read_file:
        parameters = json.load(read_file)

    # The main notebook which we will build
    # [TODO] specify kernel and other basic info in the creation step (currently done by papermill)
    nb = nbf.v4.new_notebook()

    # prepare papermill inputs cell
    papermill_cell = nbf.v4.new_code_cell("input_params= {}")
    papermill_cell.metadata.tags = ["parameters"]
    nb["cells"].append(papermill_cell)

    imports = nbf.read(
        str(path_to_report + parameters["sources"]["imports"]), as_version=4
    )
    nb = append_cell_set(nb, imports)

    header = nbf.read(
        str(path_to_report + parameters["sources"]["header"]), as_version=4
    )
    nb = append_cell_set(nb, header)

    # prepare giant papermill input list:
    papermill_input = {}

    for analysis_module in parameters["analysis"]:
        # generates the full module path for the notebook, stores all necessary data as papermill input and appends the set of cells to the notebook which will run said analysis

        module_path = (
            "reward_systems."
            + parameters["analysis"][analysis_module]["reward_system"]
            + ".analysis_tools."
            + parameters["analysis"][analysis_module]["type"]
        )

        papermill_input[analysis_module] = {
            "module": module_path,
            "data": _data[parameters["analysis"][analysis_module]["source"]].__dict__,
        }

        new_cells = build_module_cells(analysis_module)

        nb = append_cell_set(nb, new_cells)

    footer = nbf.read(
        str(path_to_report + parameters["sources"]["footer"]), as_version=4
    )
    nb = append_cell_set(nb, footer)

    # [TODO] implement sensible naming policy
    fname = "test_" + _templateName + ".ipynb"

    with open(fname, "w") as f:
        nbf.write(nb, f)

    dist_input_path = "./" + fname
    dist_output_path = "./output_" + fname

    # run it with papermill
    # [TODO] see comment on notebook creation (~line 40)
    pm.execute_notebook(
        dist_input_path,
        dist_output_path,
        parameters=papermill_input,
        kernel_name="python",
        language="python",
    )

    # convert the executed notebook to HTML
    return_buf = subprocess.run(
        "jupyter nbconvert --log-level=0 --to html --TemplateExporter.exclude_input=True %s"
        % dist_output_path,
        shell=True,
    )

    # [TODO] we can now delete the template notebook

    # return true to confirm everything worked fine.
    return True


def append_cell_set(_originalCells, _append):
    """
    Appends a group of cells to an already existing notebook

    Args:
        _originalCells(list): An already existing set of notebook cells
        _append(list): A list of cells to be appended to said notebook

    Raises:
        [TODO]: Check for errors and raise them

    Returns:
        newSet(list): A notebook object with the new cells appended.

    """

    # [TODO] There must be a native way to do this in a generalized fashion

    newSet = _originalCells
    for cell in _append["cells"]:
        # print(cell)
        if cell["cell_type"] == "code":
            newSet["cells"].append(nbf.v4.new_code_cell(cell["source"]))
        elif cell["cell_type"] == "markdown":
            newSet["cells"].append(nbf.v4.new_markdown_cell(cell["source"]))

    return newSet


def build_module_cells(_name):
    """
    Generates a set of cells that will run a specified analysis module inside the notebook.

    Args:
        _name(string): The name of the module we want to build. The name must match one of the modules specified in the JSON template loaded into papermill by the build_and_run function.

    Raises:
        [TODO]: Check for errors and raise them

    Returns:
        output_cells(list): A list of cells to be added to the notebook which, when run, will generate the specified analysis in the "print-ready" representation for the report.

    """
    output_cells = nbf.v4.new_notebook()

    code = "current_analysis = " + _name + "\n#print(current_analysis)"
    output_cells["cells"].append(nbf.v4.new_code_cell(code))

    template = nbf.read(str("./src/builder_template.ipynb"), as_version=4)

    append_cell_set(output_cells, template)

    return output_cells
