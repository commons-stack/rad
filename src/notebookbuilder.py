# ON-THE-FLY NOTEBOOK BUILDER

#   receives:
#       - a template name
#       - the necessary data to run that template in JSON format
#
#   outputs:
#       - a notebook following the specified template, executed with the received data. Saved as a file

#   execution:
#       -load template JSON
#       -create empty notebook
#       -prepare papermill parameters
#       - append header from template
#       - run module/cellbuilder.py for every analysis step and append them to notebook
#       - append footer from template
#       - run the notebook with papermill (maybe we can avoid saving it to a file?)
#       - save the executed notebook


from sys import path
import nbformat as nbf
import importlib
import json


def build_and_run(_templateName, _data):

    nb = nbf.v4.new_notebook()

    path_to_report = "./reports/" + _templateName + "/"

    parameters_path = path_to_report + _templateName + ".json"
    parameters = {}
    with open(parameters_path, "r") as read_file:
        parameters = json.load(read_file)


    imports = nbf.read(
        str(path_to_report + parameters["sources"]["imports"]), as_version=4)
    header = nbf.read(
        str(path_to_report + parameters["sources"]["header"]), as_version=4)
    footer = nbf.read(
        str(path_to_report + parameters["sources"]["footer"]), as_version=4)

    # prepare giant papermill input list:
    papermill_input = {}
    papermill_input["_data"] = _data

    analysis_list = {}
    #   for each analysis in parameters["analysis"]
    for analysis in parameters["analysis"]:
        #       create a list with the required raw input and save under the analysis name
        analysis_list[analysis["name"]] = {
            "template": analysis["template"], "parameters": analysis["parameters"]}

    # prepare papermill inputs cell
    papermill_cell = nbf.v4.new_code_cell("input_params= {}")
    papermill_cell.metadata.tags = ["parameters"]
    nb["cells"].append(papermill_cell)

    # generate cell with imports (specially the analysis module)
    nb = append_cell_set(nb, imports)
  
    # append header
    nb = append_cell_set(nb, header)
  

    # here we go call the cellbuilder for analysis
    for analysis in analysis_list:
        papermill_input[analysis["name"]] = analysis["parameters"]
        template_path = path_to_templates + analysis["template"]

        template = nbf.read(template_path, as_version=4)
        nb = append_cell_set(nb, template)


    # append footer
    nb = append_cell_set(nb, footer)

    fname = 'test_output.ipynb'

    with open(fname, 'w') as f:
        nbf.write(nb, f)

    # run it with papermill


def append_cell_set(_originalCells, _append):
    
    #There must be a native wa to do this in a generalized way

    newSet = _originalCells
    for cell in _append['cells']:
        # print(cell)
        if cell['cell_type'] == 'code':
            newSet['cells'].append(nbf.v4.new_code_cell(cell['source']))
        elif cell['cell_type'] == 'markdown':
            newSet['cells'].append(nbf.v4.new_markdown_cell(cell['source']))

    return newSet


# MOVED FROM NOTEBOOK CELL-BUILDER.PY 

#   receives:
#       - the JSON of an analysis step
#   returns:
#       - a set of jupyter notebook cell objects, which a markdown text introduction to the analysis step, the execution  of the analysis and relevant visualization instruction
#
#   execution:
#        - import the function based on the JSON data 
#        - generate cell objects
#        - return them

def build_cells(_name):
    output_cells = []
    #import library from the relevant folder

    #create markdown cell with Header
    #create markdown cell with description
    #create code cell that runs the print function (or just create cell with the results of the print func?) 

    #return set of cells
    return output_cells

    # CODE FROM KRISTOFER
    #     import importlib
    # modnames = [
    #   "sources.praise.analysis.modules.giverTotalScore", 
    #   "sources.praise.analysis.modules.giverTotalScore2"
    # ]
    # modlist = []
    # for lib in modnames:
    #   mod = importlib.import_module(lib)
    #   print(mod.header)
    #   print(mod.description)
    #   mod.run(praise_distribution)

