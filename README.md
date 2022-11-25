# Run using local Python installation

- Create a python virtual environment
- Run "pip install -r requirements.txt"
- Run "python main.py -p test_data/"

# Run using Docker

- Prerequisite: Docker
- `bash start.sh [absoute path to root data folder]`
- In RAD cli: `bash rad.sh data_folder`

# Current TO DOs:

- [ ] [Epic] Go through all functions and implement error checking/ raising
- [ ] [minor] check if there is a more elegant way to code the notebookbuilder.append_cell_set function. There probably is, but extend() doesn't seem to work.
- [ ] In the Aragon export, allow to send a link in the config dict that substitutes IDs for addresses. Should come in handy for adding sourcecred
- [ ] "praise flow" refactor
- [ ] Something in the praise flow makes a warning pop up when converting. figure out what it is
- [ ] rating_distribution.py: removing no-raters got lost somewhere. Redo
- [ ] allow to user to create their own folder with reports/dstributions/exports and call them from inside RAD
- [ ] general renaming/cleanup
- [ ] Cross-period: Fix breaking bug in last cell
- [ ] Fix printing bug
- [ ] Compare results with original to make sure everything works
- [ ] Refactor cross period modules and function calls
