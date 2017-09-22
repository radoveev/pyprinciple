# -*- coding: utf-8 -*-
"""Shared functions and objects for pyprinciple

Copyright (C) 2017 Radomir Matveev GPL 3.0+
"""

# --------------------------------------------------------------------------- #
# Import libraries
# --------------------------------------------------------------------------- #
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QProgressBar,
                             QFormLayout, QGridLayout)
from PyQt5.QtCore import QObject
#from PyQt5.QtGui import QPixmap


# --------------------------------------------------------------------------- #
# Define classes
# --------------------------------------------------------------------------- #
class QProgressList(QWidget):
    """A list of progress bars with icons and labels.
    """
    def __init__(self, translation_context, parent=None):
        super().__init__(parent)
        assert isinstance(translation_context, str), "not a string"
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

    def schoolDays(self):
        """Returns a tuple of days were the school is open."""
        return ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday")

    def timeTablePeriods(self):
        """Return a tuple of periods for the timetable of the school."""
        return ("7:50 - 9:20", "9:40 - 11:10", "11:30 - 13:00",
                "14:30 - 16:00")


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
