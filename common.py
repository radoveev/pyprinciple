# -*- coding: utf-8 -*-
"""Shared functions and objects for pyprinciple

Copyright (C) 2017 Radomir Matveev GPL 3.0+
"""

# --------------------------------------------------------------------------- #
# Import libraries
# --------------------------------------------------------------------------- #
from pathlib import Path

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QProgressBar,
                             QFormLayout, QGridLayout)
from PyQt5.QtCore import QObject
#from PyQt5.QtGui import QPixmap
import os

# --------------------------------------------------------------------------- #
# Define classes
# --------------------------------------------------------------------------- #
class QProgressList(QWidget):
    """A list of progress bars with icons and labels.
    """
    def __init__(self, translation_context=None, parent=None):
        super().__init__(parent)
        assert isinstance(translation_context, str), "not a string"
        if translation_context is None:
            self.translation_context = type(self).__name__
        else:
            self.translation_context = translation_context
        self.labelmap = {}  # maps label texts to (icon, label, bar) tuples
        # create layout
        self.layout = QGridLayout(self)

    def addBar(self, label, icon=None):
        # if we have been given a string, turn it into a label
        if not isinstance(label, QLabel):
            label = QLabel(label, self)
        icon_lbl = QLabel(self)
        if icon is not None:
            icon_lbl.setPixmap(icon)
        bar = QProgressBar(self)
        self.labelmap[label.text()] = (icon_lbl, label, bar)
        row = self.layout.rowCount()
        for col, widget in enumerate((icon_lbl, label, bar)):
            self.layout.addWidget(widget, row, col)
        self.retranslateUi()

    def retranslateUi(self):
        tra = QApplication.translate
        for text in self.labelmap:
            icon, label, bar = self.labelmap[text]
            label.setText(tra(self.translation_context, text))


class WorldInterface(QObject):
    """Serves data from the game logic layer to the python layer.

    # TODO: actually connect to C++ and fetch the data from there
    """
    def __init__(self):
        super().__init__()
        self.button_data = {
                "Your Home": (("Paperwork:\nManage School", (125, 370)),
                              ("Kitchen:\nOpen Fridge", (100, 250)),
                              ("Video Library:\nOpen Library", (650, 380)),
                              ("Computer", (850, 400))
                              )
                }
        self.location_images = {
                "Your Home": (os.path.dirname(os.path.abspath(__file__))+"/Schools/NormalSchool/Images/Locations/" +
                              "Your Home/empty.jpg")
                }
        self.people_in_locations = {
                "Your Home": ("Annette", "Peter")
                }

    def schoolDays(self):
        """Returns a tuple of days were the school is open."""
        return ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")

    def timeTablePeriods(self):
        """Return a tuple of periods for the timetable of the school."""
        return ("7:50 - 9:20", "9:40 - 11:10", "11:30 - 13:00",
                "14:30 - 16:00")

    def classes(self):
        """Return all classes of the school."""
        return ("Class 1", "Class 2")

    def teachers(self):
        """Return all teachers, wether they are employees or not."""
        return ("April Raymund", "Beth Manili", "Carl Walker", "Carmen Smith",
                "Claire Fuzushi", "Jessica Underwood", "Nina Parker",
                "Ronda Bells", "Samantha Keller")

    def subjects(self):
        """Return all school subjects."""
        return ("Anatomy Class", "Art", "Biology", "Bondage Class",
               "Chemistry", "Computer Science", "Economics", "English",
               "Geography", "History", "Math", "Music", "Philosophy",
               "Physics", "Practical Sex Education", "Religion",
               "School Sport", "Swimming", "Theoretical Sex Education")

    def subjectFamilies(self):
        return ("Mathematics", "Language Arts", "Natural Science",
                "Life Science", "Computer Studies", "Social Science",
                "Humanities", "Fine Arts", "Physical Education",
                "Sexual Education")

    def balanceItems(self):
        """Return the current balance items of the school."""
        return (("State Funding", 18945),
                ("Principal Salary", 2585),
                ("Staff Salary", -34563),
                ("Investigator", -3000),
                ("Building Maintenance", -1684),
                ("Cabaret Rental", -600),
                ("Bathroom Spycam Pics", 252),
                ("Changing Room Spycam Pics", 504),
                ("Cheerleading Club Spycam Pics", 504),
                ("Swim Club Spycam Pics", 352),
                ("Secret Panty Exchange sales", 384),
                ("Your Sister's rent", 400)
                )

    def locationButtons(self, location):
        """Return the buttons for the given location."""
        return self.button_data[location]

    def locationImage(self, location):
        """Return the image for the given location."""
        path = Path(QApplication.applicationDirPath())
        path = path / self.location_images[location]
        path.resolve()
        return path

    def peopleAt(self, location):
        """List all people at the given location."""
        return self.people_in_locations[location]


# --------------------------------------------------------------------------- #
# Define functions
# --------------------------------------------------------------------------- #
def translate_form(form, context, labels):
    """Translates the labels of a QFormLayout.
    """
    tra = QApplication.translate
    for row, text in enumerate(labels):
        label = form.itemAt(row, QFormLayout.LabelRole).widget()
        label.setText(tra(context, text))


# --------------------------------------------------------------------------- #
# Declare module globals
# --------------------------------------------------------------------------- #
world = WorldInterface()
