# -*- coding: utf-8 -*-
"""Shared functions and objects for pyprinciple

Copyright (C) 2017 Radomir Matveev GPL 3.0+
"""

# --------------------------------------------------------------------------- #
# Import libraries
# --------------------------------------------------------------------------- #
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QProgressBar,
                             QFormLayout, QGridLayout)
#from PyQt5.QtGui import QPixmap


# --------------------------------------------------------------------------- #
# Define classes
# --------------------------------------------------------------------------- #
class QProgressList(QWidget):
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
