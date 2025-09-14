import os
import sys
import promptutils
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QVBoxLayout, QWidget, QLineEdit, QButtonGroup

from promptutils import create_profiles, get_profile_script_files, exec_script_button, get_profile_path

class CreateProfileWindow(QMainWindow):                           # <===
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generate new command profile")

        self.label = QLabel("Enter a new name for the command profile:", self)
        self.label.setFont(QtGui.QFont('Arial', 9))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.adjustSize()
        self.profilenamebox = QLineEdit()

        self.button = QPushButton("Create profile", self)
        self.cancelbutton = QPushButton("Cancel", self)
        self.button.clicked.connect(self.on_button_create)
        self.cancelbutton.clicked.connect(self.on_button_cancel)


        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.profilenamebox)
        layout.addWidget(self.button)
        layout.addWidget(self.cancelbutton)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_button_create(self):
        # Generate new folder, open window for new profile
        # This makes the new profile directory if the name is available, and doesn't if it is taken or invalid
        # The function returns text, so display it for the user
        profileCreationResult = create_profiles(self.profilenamebox.text())
        self.label.setText(profileCreationResult[0])

        # Open new window
        if profileCreationResult[1]:
            self.w = PromptCommandPanelWindow(self.profilenamebox.text())
            self.w.show()
            self.hide()
            pass


    def on_button_cancel(self):
        # Close this window
        self.label.setText("You clicked the button!")

"""
Ok so this window is very important so read how it works here.

This window should:
Generate as many buttons as there are scripts in a profile.
Load all scripts to make them callbacks for the buttons
LEFT-CLICKING ON A BUTTON = running the script as a one shot.
RIGHT-CLICKING ON A BUTTON = generates information window for command
"""

class PromptCommandPanelWindow(QMainWindow):                           # <===
    def __init__(self, profileWindowTitle):
        super().__init__()
        # Use name of profile for window title
        self.setWindowTitle(profileWindowTitle)

        # self.label = QLabel("Enter a new name for the command profile:", self)
        # self.label.setFont(QtGui.QFont('Arial', 11))
        # self.label.setAlignment(QtCore.Qt.AlignCenter)
        # self.label.adjustSize()
        # self.profilenamebox = QLineEdit()

        # Instead of pressing a button, use this callback to generate more buttons
        # Use a button group
        self.panelButtonGroup = QButtonGroup()
        self.panelButtonGroup.buttonClicked.connect(self.on_script_click)

        layout = QVBoxLayout()

        # If no scripts, spawn text saying there aren't any and to add one
        scriptList = get_profile_script_files(self.windowTitle())
        if scriptList:
            for scripts in scriptList:
                # If this string is in the name, don't include it
                if "EXCLUDE_" not in scripts:
                    newButton = QPushButton(scripts)
                    layout.addWidget(newButton)
                    self.panelButtonGroup.addButton(newButton)
                pass
        else:
            self.label = QLabel("No scripts found. Add some to the profile first, then press refresh.", self)
            self.label.setFont(QtGui.QFont('Arial', 11))
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            self.label.adjustSize()
            layout.addWidget(self.label)

            self.button = QPushButton("Refresh Scripts", self)
            # self.cancelbutton = QPushButton("Cancel", self)
            self.button.clicked.connect(self.on_script_retrieval)
            # self.cancelbutton.clicked.connect(self.on_button_cancel)
            layout.addWidget(self.button)



        # layout.addWidget(self.profilenamebox)
        # layout.addWidget(self.button)
        # layout.addWidget(self.cancelbutton)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def on_script_retrieval(self):
        # get_profile_script_files(self.windowTitle())
        self.destroy()
        self.w = PromptCommandPanelWindow(self.windowTitle())
        self.w.show()

    def on_script_click(self, button):
        print(f'Button "{button.text()}" activated.\n')
        exec_script_button(get_profile_path(self.windowTitle()), button.text())
        # Get script lines, execute in bash
        # Check if left or right click, as well
        pass
