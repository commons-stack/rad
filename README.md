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
- [ ] In the Aragon export, allow to send a link in the config dict that substitutes IDs for addresses. Should come in handy for adding sourcecred
- [ ] "praise flow" refactor
- [ ] Something in the praise flow makes a warning pop up when converting. figure out what it is
- [ ] rating_distribution.py: removing no-raters got lost somewhere. Redo
- [ ] allow to user to create their own folder with reports/dstributions/exports and call them from inside RAD
- [ ] general renaming/cleanup
- [x] Cross-period: Fix breaking bug in last cell
- [x] Make export for category analysis (look at TODO in analysis module)
- [x] Look into "root-folder" parameter bug
- [ ] Decide how to implement Nakamoto score/ratio
- [ ] Compare results with original to make sure everything works
- [ ] Refactor cross period modules and function calls
- [ ] Make sure the forum post reflects the final distributed tokens, not the maximum
- [x] Allow to specify the name of the parameters file (to easily adapt tec-rewards)
