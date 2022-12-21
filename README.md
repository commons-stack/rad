# Rewards Analysis and Distribution (RAD) Module

The RAD Module empowers user to easily analyze the reward distributions of their DAO, and generate automated reports which can be shared with the community.

# General Structure

RAD consists of two main parts:

- **RAD module package** : A python package implementing objects for supporte reward systems, which can be used to process and analyze them.
- **Reports** : Jupyter notebooks wich focus on specific parts of the data, and can be re-run or converted to html for easy distribution.

The main rad script takes a folder contiaing distribution data as input. It will look for a file called parameters.json in it, and run all reports in the `/local` folder with that file as input. Results are stored in a folder called `analysis-results` in the same place the data was taken from.

Usually the output consists of three folders:
-Reports: HTML version of the reports for easy sharing
-Executed_notebooks: A copy of jupyter notebooks in executed state for easy audit
-Exports: Other files saved as specified inside parameters.json

# Setup

Clone the repository locally. Copy all .ipynb files in 'report_templates/' into the 'local/' folder. These will be executed anytime you run RAD.

# Run using local Python installation

- Create a python virtual environment
- Run "pip install -r requirements.txt"
- Run "pip install -e rad/"
- Run "python main.py -p path_to_data/"

# Run using Docker

- Prerequisite: Docker
- `bash start.sh [absoute path to root data folder]`
- In RAD cli: `bash rad.sh data_folder`

**After a run, results are saved in a folder called 'analysis_results' in the same folder as the original data (if you didn't specify a differente place with the -o flag).**

# Expanding and Adapting RAD

Since the whole RAD package is installed locally in editable mode, you can freely modify and add modules. For example, to try out a modified distribution algorithm, you'd go to the 'distributions' folder in the relevant reward system, and create a new .py file which inherits from "RewardDistribution". You can copy existing distributions and use them as a template.
Adding analysis modules works in the same way, but in the analysis folder. Analysis modules should contain a "run", "printDescription" and "printGraph" function.

> RAD is still a "work in progress". Expected future changes involve forcing a common structure for RewardObjects, DistributionObjects and Analysis Modules through abstract classes, and moving all user-generated modules to a separate folder to not need to install the whole package locally.
