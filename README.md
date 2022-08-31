# To run
* Create a python virtual environment
* run "pip install -r requirements.txt"
* run "python main.py -p test_data/"


#Current TO DOs:
- [ ] [Epic] Go through all functions and implement error checking/ raising
- [ ] Review file output structure. Righ now it all goes into the folder called "my_reports"
- [ ] Specify jupyter kernel and other basic info in the notebook creation step (currently done by papermill in runtime, which makes re-running the notebooks as standalone fail)
- [ ] implement some kind of naming policy for the notebooks.
- [ ] [minor] check if there is a more elegant way to code the notebookbuilder.append_cell_set function. There probably is.
- [ ] implement combined exports
- [ ] (related) Review if it is necessary to implement a separate "combinator" module, or if the other modules can handle that internally.
- [ ] In the Aragon export, allow to send a link in the config dict that substitutes IDs for addresses. Should come in handy for adding sourcecred
- [ ] Research if there is a way to get rid of the rewardObjectBuilder class completely and natively handle new reward system objects.
- [ ] Delete the template notebook after running it 
- [x] [Epic] [Lots of refactor probably]Add the option to add config data to the notebook builder cells, so we can use parameters for stuff like praise flows. The parameters will be specified in the report json file
- [ ] Hard praise flow refactor
- [ ] Something in the praise flow makes a warning pop up when converting. figure out what it is
- [ ] rating_distribution.py:  removing no-raters got lost somewhere. Redo
- [ ] allow to user to create their own templates in the folder the fork and store data in. (so they would only need to fork the rad without modifying anything, all changes would be in their "tec-reward" equivalent)
- [x] separate distirbution from reward-system-instance, to allow for different distribution algorithms [Epic] [Brainstorm]
- [ ] clean up praise and straightRewards classes to address new structure where the distribution is separate
- [ ] prepare the praise object to be able to receive several sources of the same tipe and combine them
- [ ] "full praise table" export


