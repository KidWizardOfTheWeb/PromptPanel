import os
import sys
import promptutils
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QVBoxLayout, QWidget, QLineEdit

from childuiwindows import CreateProfileWindow, PromptCommandPanelWindow
from promptutils import get_profiles_for_script_listing


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Setup
        self.setWindowTitle("Prompt Panel - Dev")
        self.setGeometry(800, 400, 310, 200)

        # Text label
        self.label = QLabel("Welcome to Prompt Panel.\n\n"
                            "Add your command line sequences into a profile,\n"
                            "and watch them turn into easy-to-use buttons on a GUI!\n\n"
                            "Select a command profile from the dropdown,\n"
                            "or generate a new one with the button.\n", self)
        self.label.setFont(QtGui.QFont('Arial', 11))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.adjustSize()

        # Dropdown
        # This gets all the profiles we need and populates the dropdown
        self.profilelist = QComboBox()
        self.profilelist.setEditable(True) # Allows text searching the box (add substring autocomplete, google it)
        self.profilelist.setInsertPolicy(QtWidgets.QComboBox.NoInsert) # Cannot add items yourself
        self.profilelist.addItems(get_profiles_for_script_listing()) # Add a refresh option for this later with a button.
        # If they click on an option, then open the Prompt Command Panel
        self.profilelist.activated.connect(self.opencommandpanelcall)

        # Generate button
        self.generatebutton = QPushButton("Generate new command profile", self)
        self.generatebutton.clicked.connect(self.createprofilecall)

        # Refresh button
        self.refreshbutton = QPushButton("Refresh command profile list", self)
        self.refreshbutton.clicked.connect(self.refreshprofiles)

        # Layout and container
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.generatebutton)
        layout.addWidget(self.refreshbutton)
        layout.addWidget(self.profilelist)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    # Opens another window to generate a new profile
    def createprofilecall(self):  # <===
        self.w = CreateProfileWindow()
        self.w.show()
        # self.hide()

    def opencommandpanelcall(self, index):  # <===
        # Since this always sorts alphabetically it seems, this seems safe to use
        profileName = get_profiles_for_script_listing()[index]
        self.w = PromptCommandPanelWindow(profileName)
        self.w.show()

    def refreshprofiles(self):
        self.destroy()
        self.w = MainWindow()
        self.w.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

