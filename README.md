# To run
* Create a python virtual environment
* run "pip install -r requirements.txt"
* run "python main.py -p test_data/"


#Current TO DOs:
- [Epic] Go through all functions and implement error checking/ raising
- Review file output structure. Righ now it all goes into the folder called "my_reports"
- Specify jupyter kernel and other basic info in the notebook creation step (currently done by papermill in runtime, which makes re-running the notebooks as standalone fail)
- implement some kind of naming policy for the notebooks.
- [minor] check if there is a more elegant way to code the notebookbuilder.append_cell_set function. There probably is.
- implement combined exports
- (related) Review if it is necessary to implement a separate "combinator" module, or if the other modules can handle that internally.
- In the Aragon export, allow to send a link in the config dict that substitutes IDs for addresses. Should come in handy for adding sourcecred
- Research if there is a way to get rid of the rewardObjectBuilder class completely and natively handle new reward system objects.


