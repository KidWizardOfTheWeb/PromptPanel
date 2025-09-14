import os
import struct
import sys
from os import getenv
from pathlib import Path
import subprocess
import shlex

# note: rewrite this to my needs (copied from geckoloader for now: https://github.com/JoshuaMKW/GeckoLoader/blob/master/fileutils.py)

def resource_path(relPath: str = "") -> Path:
    """
    Get absolute path to resource, works for dev and for cx_freeze
    """
    import sys

    if hasattr(sys, "_MEIPASS"):
        return Path(getattr(sys, "_MEIPASS", Path(__file__).parent)) / relPath
    else:
        if getattr(sys, "frozen", False):
            # The application is frozen
            base_path = Path(sys.executable).parent
        else:
            base_path = Path(__file__).parent

        return base_path / relPath


def get_program_folder(folder: str = "") -> Path:
    """Get path to appdata"""
    if sys.platform == "win32":
        datapath = Path(getenv("APPDATA")) / folder
    elif sys.platform == "darwin":
        if folder:
            folder = "." + folder
        datapath = Path("~/Library/Application Support").expanduser() / folder
    elif "linux" in sys.platform:
        if folder:
            folder = "." + folder
        datapath = Path.home() / folder
    else:
        raise NotImplementedError(f"{sys.platform} OS is unsupported")
    return datapath


def get_profiles_for_script_listing():
    # For our dropdown of profiles, get all of them here to populate it
    return os.listdir(resource_path("Profiles"))


def create_profiles(newProfileName):
    # Check if they entered a name. If not, return false.
    if not newProfileName:
        return "No name entered, try a different name.", False
    profilePath = os.path.join(resource_path("Profiles"), newProfileName)
    if not os.path.exists(profilePath):
        os.mkdir(profilePath)
        return "Profile generated successfully.", True
    else:
        return "Profile already taken, try a different name.", False



def get_profile_path(profileID):
    # Get the path of the profile that is being accessed
    return os.path.join(resource_path("Profiles"), profileID)


def get_profile_script_files(profileID):
    # Check for scripts in here, get a list of all scripts in the given profile
    # This can be none, add handling for that
    return os.listdir(get_profile_path(profileID))


def exec_script_button(profilePath, scriptName):
    # Get the path to the script to run
    scriptToRun = os.path.join(profilePath, scriptName)

    # Read all lines of the script
    with open(scriptToRun, "r") as file:
        commands = file.readlines()
        # Clean list of commands with shlex.
        # NOTE: any win paths will be decimated due to linux-isms.
        # Fix them by either ensuring users use quote marks are there or some other security.

        # Activating raw scripts that aren't bash without prefixes will also not work.
        # Add detection for file types probs, then append the run commands?
        splitComms = [shlex.split(line) for line in commands]

        # Then, open subproc and run all lines in shell
        # Note: you can add breakpoint functionality between lines later this way. Neat.
        for currCommand in splitComms:
            output = subprocess.check_output(currCommand)
            print(output.decode())
    pass