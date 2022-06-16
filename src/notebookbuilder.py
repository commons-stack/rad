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


def build(_templateName, _data):

    nb = nbf.v4.new_notebook()

    path_to_template = "./templates/" + _templateName + "/"

    parameters_path = path_to_template + _templateName + "-template.json"
    parameters = {}
    with open(parameters_path, "r") as read_file:
        parameters = json.load(read_file)

    header = nbf.read(
        str(path_to_template + parameters["sources"]["header"]), as_version=4)
    footer = nbf.read(
        str(path_to_template + parameters["sources"]["footer"]), as_version=4)

    # prepare giant papermill input list:
    #   for each analysis in parameters["analysis"]
    #       create a  list with the required raw input and save under the analysis name

    # prepare papermill inputs cell
    papermill_cell = nbf.v4.new_code_cell("input_params= {}")
    papermill_cell.metadata.tags = ["parameters"]
    nb["cells"].append(papermill_cell)

    # generate cell with imports (specially the analysis module)

    # append header
    for cell in header['cells']:
        # print(cell)
        if cell['cell_type'] == 'code':
            nb['cells'].append(nbf.v4.new_code_cell(cell['source']))
        elif cell['cell_type'] == 'markdown':
            nb['cells'].append(nbf.v4.new_markdown_cell(cell['source']))

    # here we go call the cellbuilder for analysis
        # for each analysis in parameters["analysis"]:
        #       cells =  cellbuilder.build(analysis)
        #       nb["cells"].append(cells)

    # append footer
    for cell in footer['cells']:
        # print(cell)
        if cell['cell_type'] == 'code':
            nb['cells'].append(nbf.v4.new_code_cell(cell['source']))
        elif cell['cell_type'] == 'markdown':
            nb['cells'].append(nbf.v4.new_markdown_cell(cell['source']))

    fname = 'test_output.ipynb'

    with open(fname, 'w') as f:
        nbf.write(nb, f)
