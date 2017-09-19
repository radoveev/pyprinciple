# -*- coding: utf-8 -*-
"""Shared functions and objects for pyprinciple

Copyright (C) 2017 Radomir Matveev GPL 3.0+
"""

# --------------------------------------------------------------------------- #
# Import libraries
# --------------------------------------------------------------------------- #
from PyQt5.QtWidgets import QApplication, QFormLayout


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
