# PromptPanel
#### Your solution for preventing command line fatigue.

# Running the program
Quite simple to use, simply start `mainwindowui.py` (will move in the future) and the program will start.
From a fresh launch, you will have no command profiles. Use `Generate new command profile` to create one. This manifests as a folder in the `Profiles` directory.
After creating a profile, you'll need to add scripts to use. Write your CLI commands into a text file (line-by-line), store them in the new profile created in the `Profiles` directory, then press `Refresh scripts` to watch them populate as buttons.
Pressing a buttons will invoke the script it's named after as a subprocess.
You can link other scripts by invoking them as you would in the command line, but by including them in the text file, e.g. `py "C:\path\to\script\invokescript.py"`.

# Things to note
If you want to include a script in a profile, but not have it show up in the GUI, write `EXCLUDE_` in the name of the script. It will then not be included in the button list on the GUI.

# Current limitations
Only absolute paths are allowed right now (i.e. windows users will need to use quotes around paths), wildcard support for file paths is TBA.
