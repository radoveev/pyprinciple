# -*- coding: utf-8 -*-
"""The central module of the GUI of pyprinciple

Copyright (C) 2017 Radomir Matveev GPL 3.0+

The Qt main loop is executed in the main function of this module.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

# --------------------------------------------------------------------------- #
# Import libraries
# --------------------------------------------------------------------------- #
import logging
import sys
from pathlib import Path
from collections import OrderedDict

from PyQt5.QtWidgets import (QApplication, QProgressBar, QStackedWidget,
                             QLabel, QWidget, QDesktopWidget,
                             QPushButton, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.Qt import QMainWindow

import common as cmn
import style
from location_view import LocationView
from school_management import SchoolManagement


# --------------------------------------------------------------------------- #
# Define classes
# --------------------------------------------------------------------------- #
class Person(object):
    def __init__(self, forename):
        self.forename = forename
        # TODO


class MainWin(QMainWindow):

    def __init__(self):
        super().__init__()
        self.wait_times = [10, 30, 60]
        self.push_wait = []  # list of wait buttons
        self.displaystat_hdr = []  # TODO replace with OrderedDict?
        self.displaystat_val = []
        self.statlabels = OrderedDict()  # statname: (namelabel, vallabel)
        # create widgets
        w = QWidget(self)
        self.central_widget = w
        self.time_lbl = QLabel(w)
        self.date_lbl = QLabel(w)
        self.location_lbl = QLabel(w)
        self.energy_bar = QProgressBar(w)
        self.arousal_bar = QProgressBar(w)
        self.widget_stack = QStackedWidget(self)
        self.location_view = LocationView(self)
        self.school_management = SchoolManagement(self)

        # create layout
        self.retranslateUi()
        grid = QGridLayout(self.central_widget)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.addWidget(self.time_lbl,   0, 5, 1, 2)
        grid.addWidget(self.date_lbl,   0, 3, 1, 2)
        grid.addWidget(self.energy_bar, 0, 7, 1, 5)
        grid.addWidget(self.arousal_bar, 1, 7, 1, 5)
        grid.addWidget(self.location_lbl, 2, 0, 2, 3)

        for i, stat in enumerate(self.displaystat_hdr):
            val = self.displaystat_val[i]
            statlabel = QLabel(stat, w)
            vallabel = QLabel(val, w)
            self.statlabels[stat] = (statlabel, vallabel)
            grid.addWidget(statlabel, 2, 3 + i, 1, 1)
            grid.addWidget(vallabel, 3, 3 + i, 1, 1)
            # TODO: style
#            displaystat_hdr[i].setPalette(HHStyle::hdr_text);
#            displaystat_hdr[i].setAlignment(Qt::AlignCenter);
#            displaystat_val[i].setPalette(HHStyle::white_text);
#            displaystat_val[i].setAlignment(Qt::AlignCenter);

        self.widget_stack.addWidget(self.location_view)
        self.widget_stack.addWidget(self.school_management)

        grid.addWidget(self.widget_stack, 4, 0, 50, 12)

        self.setCentralWidget(w)

        # configure window
#        geom = QDesktopWidget().availableGeometry()
        self.setGeometry(100, 50, 800, 600)

        # configure widgets
        w.setContentsMargins(0, 0, 0, 0)
        w.setObjectName("central_widget")

        self.time_lbl.setObjectName("text")  # use text style from style sheet
        self.time_lbl.setFont(style.big_font)
        self.time_lbl.setAlignment(Qt.AlignCenter)
        self.date_lbl.setObjectName("text")
        self.date_lbl.setFont(style.big_font)
        self.date_lbl.setAlignment(Qt.AlignRight)
        self.location_lbl.setObjectName("text")
        self.location_lbl.setFont(style.location_font)

        self.energy_bar.setValue(60)
        self.energy_bar.setObjectName("energy")
        self.arousal_bar.setValue(48)
        self.arousal_bar.setObjectName("arousal")

        self.widget_stack.setCurrentIndex(0)

        # TODO only shown if window contains locationview
        for i in range(0, len(self.wait_times)):
            pw = QPushButton("Wait %d min" % self.wait_times[i])
            self.push_wait.append(pw)
            grid.addWidget(pw, 0, i, 2, 1)

        for name in world.peopleAt("Your Home"):
            self.location_view.addPerson(Person(name))

        self.retranslateUi()

        self.show()

    def retranslateUi(self):
        tra = QApplication.translate
        ctxt = "MainWin"
        self.setWindowTitle(tra(ctxt, "pyPrinciple"))
        # TODO: use ordered dict instead
        displaystat = ["Education", "Happiness", "Loyalty", "Inhibition",
                       "Lust", "Corruption", "Reputation", "Students", "Money"]
        self.displaystat_hdr = [tra(ctxt, stat) for stat in displaystat]
        self.displaystat_val = [tra(ctxt, "30.1")
                                for stat in displaystat[:-2]]
        self.displaystat_val.append(tra(ctxt, "91"))
        self.displaystat_val.append(tra(ctxt, "$10,000"))

        for waittime, pushbu in zip(self.wait_times, self.push_wait):
            pushbu.setText(tra(ctxt, "Wait %s min" % waittime))

        # TODO: translating dates and times is easier via datetime objects
        self.time_lbl.setText(tra(ctxt, "8:00"))
        self.date_lbl.setText(tra(ctxt, "Monday (1/1/2017)"))
        self.location_lbl.setText(tra(ctxt, "Home"))

    @pyqtSlot()
    def show_school_management(self):
        self.widget_stack.setCurrentIndex(1)

    @pyqtSlot()
    def show_location_view(self):
        self.widget_stack.setCurrentIndex(0)


# --------------------------------------------------------------------------- #
# Define functions
# --------------------------------------------------------------------------- #
def main():
    global app, mainwin
    app = QApplication(sys.argv)

    # load application style sheet from file
    stylefile = cmn.srcdir / "appstyle.qss"
    with stylefile.open() as f:
        application_style = f.read()
    app.setStyleSheet(application_style)

    mainwin = MainWin()
    sys.exit(app.exec_())


# --------------------------------------------------------------------------- #
# Define module globals
# --------------------------------------------------------------------------- #
log = logging.getLogger(__name__)
app = None  # the QApplication instance
mainwin = None  # the main window of the application
world = cmn.world
