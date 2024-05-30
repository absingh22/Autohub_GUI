# Automation Hub GUI

This GUI application is designed to manage and run automation scripts efficiently. Built using `customtkinter`, it allows users to select scripts, fill in required inputs, and execute them with ease. The application's primary functionality includes changing the appearance mode, scaling, input handling, and executing scripts while managing working directories and optional environment configurations.

## Features

- *Dynamic Script Loading:* Load and display scripts based on categories.
- *Input Handling:* Manage mandatory and optional inputs dynamically.
- *Tool Configuration:* Configure tools and versions as needed.
- *Working Directory Management:* Change and create working directories for script execution.
- *.ucdprod Handling:* Create or copy .ucdprod files for environment setup.
- *Run and Print Commands:* Execute scripts and print constructed commands.

## Prerequisites

- Python 3.10.4
- Required Python libraries:
  - customtkinter
  - pandas
  - PIL (Pillow)

## Usage

1. *Run the Application:*
    bash
    ./path_to_your_python_executable/python main.py
    
2. *Navigate the GUI:*
    - *Appearance Mode:* Change between System, Dark, and Light modes.
    - *Scaling:* Adjust the scaling of the GUI.
    - *Select Scripts:* Choose scripts from the displayed categories.
    - *Fill Inputs:* Enter mandatory and optional inputs.
    - *Run Script:* Execute the script and view output.
    - *Print Command:* Print the constructed command for verification.

## File Structure

- `autohub_main.py`: Entry point of the GUI application.
- `scripts_file_new.csv`: CSV file containing script details.
- `README.md`: Documentation file.

## Example Script Entry in CSV

The `scripts_file_new.csv` should have the following columns:

- `Category`: Category of the script.
- `ScriptPath`: Path to the script.
- `MandatoryInputs`: Space-separated list of mandatory inputs.
- `OptionalInputs`: Space-separated list of optional inputs.
- `ScriptType`: Type of script (1, <script> <-argument> <arg> or 2, <script> <arg>), .
- `ToolsInput`: Tools and versions required.
- `Info`: Additional information about the script.

Example row:

Category,ScriptPath,MandatoryInputs,OptionalInputs,ScriptType,ToolsInput,Info
MyCategory,/path/to/script.sh,arg1 arg2,arg3 arg4,1,tool1::tool2@version,This is a sample script.

## Screenshot

![Main Screen](https://github.com/absingh22/Autohub_GUI/blob/main/Autohub_GUI_New.png)
