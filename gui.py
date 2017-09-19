# -*- coding: utf-8 -*-
"""The central module of the GUI of pyprinciple

Copyright (C) 2017 Radomir Matveev GPL 3.0+

The Qt main loop is executed in the main function of this module.

TODO: Style
MainWin:
    setPalette(backgroundStyle());

    QFont font("sans", 13);

    QFont font1;
    font1.setPointSize(11);
    font1.setBold(true);
    font1.setWeight(75);

    time_display.setPalette(HHStyle::hdr_text);
    time_display.setFont(font1);
    time_display.setAlignment(Qt::AlignCenter);

    date_display.setPalette(HHStyle::white_text);
    date_display.setFont(font1);
    date_display.setAlignment(Qt::AlignCenter);

    energy_bar.setPalette(progressStyle(QColor(0, 255, 255, 255)));

    arousal_bar.setPalette(progressStyle(QColor(255, 110, 249, 255)));

    location.setPalette(HHStyle::white_text);
    location.setFont(font);
"""

# --------------------------------------------------------------------------- #
# Import libraries
# --------------------------------------------------------------------------- #
import logging
import sys
from collections import OrderedDict

from PyQt5.QtWidgets import (QApplication, QProgressBar, QStackedWidget,
                             QLabel, QWidget, QDialog, QDesktopWidget,
                             QPushButton, QGridLayout, QVBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.Qt import QRect, QMainWindow

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
        self.time_display = QLabel(w)
        self.date_display = QLabel(w)
        self.location = QLabel(w)
        self.energy_bar = QProgressBar(w)
        self.arousal_bar = QProgressBar(w)
        self.stackWidget = QStackedWidget(self)  # TODO: rename to stack_widget
        self.locview = LocationView(self)  # TODO: rename to LocationView
        self.school_management = SchoolManagement(self)
        # TODO: is gridW necessary?
        self.gridW = QWidget(w)  # TODO: rename to gridw

        self.retranslateUi()

        # create layout
        grid = QGridLayout(self.gridW)
        grid.setContentsMargins(0, 0, 0, 0)
        grid.addWidget(self.time_display, 0, 5, 1, 2)
        grid.addWidget(self.date_display, 0, 3, 1, 2)
        grid.addWidget(self.energy_bar, 0, 7, 1, 5)
        grid.addWidget(self.arousal_bar, 1, 7, 1, 5)
        grid.addWidget(self.location, 2, 0, 3, 3)

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

        self.stackWidget.addWidget(self.locview)
        self.stackWidget.addWidget(self.school_management)

        grid.addWidget(self.stackWidget, 4, 0, 50, 12)

#        self.gridW.setLayout(grid)
#        self.gridW.setLayout(grid)
#        vbox = QVBoxLayout(w)
#        vbox.addWidget(self.gridW)
        w.setLayout(grid)
        self.setCentralWidget(w)

        # configure window
        self.setWindowTitle("pyprinciple")
        geom = QDesktopWidget().availableGeometry()
#        geom.adjust(10, 10, -20, -20)
#        self.setGeometry(geom)
        self.setGeometry(100, 50, 800, 600)

        # configure widgets
#        geom.setHeight(geom.height()*0.98)
#        w.setGeometry(geom)
        w.setContentsMargins(0, 0, 0, 0)

        geom.setHeight(geom.height()*0.98)

        self.gridW.setContentsMargins(0, 0, 0, 0)
#        gridW.setGeometry(geom)
        self.energy_bar.setValue(60)
        self.energy_bar.setTextVisible(False)
        self.arousal_bar.setValue(48)
        self.arousal_bar.setTextVisible(False)

        geom.setHeight(geom.height()*10/11)  # removes space for header
        self.location.setGeometry(geom)
        self.school_management.setGeometry(geom)

        self.stackWidget.setCurrentIndex(0)

        # TODO only shown if window contains locationview
        for i in range(0, len(self.wait_times)):
            pw = QPushButton("Wait %d min" % self.wait_times[i])
            self.push_wait.append(pw)
            grid.addWidget(pw, 0, i, 2, 1)

        self.dummyStartup()

        self.show()

    def retranslateUi(self):
        tra = QApplication.translate
        self.setWindowTitle(tra("HHSpp", "Main window"))
        # TODO: use ordered dict instead
        displaystat = ["Education", "Happiness", "Loyalty", "Inhibition",
                       "Lust", "Corruption", "Reputation", "Students", "Money"]
        self.displaystat_hdr = [tra("HHSpp", stat) for stat in displaystat]
        self.displaystat_val = [tra("HHSpp", "30.1")
                                for stat in displaystat[:-2]]
        self.displaystat_val.append(tra("HHSpp", "91"))
        self.displaystat_val.append(tra("HHSpp", "$10,000"))

        for waittime, pushbu in zip(self.wait_times, self.push_wait):
            pushbu.setText(tra("HHSpp", "Wait %s min" % waittime))

        # TODO: translating dates and times is easier via datetime objects
        self.time_display.setText(tra("HHSpp", "8:00"))
        self.date_display.setText(tra("HHSpp", "Monday (1/1/2017)"))
        self.location.setText(tra("HHSpp", "Home"))

    def dummyStartup(self):
        for name in ("Annette", "Peter"):
            self.locview.addPerson(Person(name))

    @pyqtSlot()
    def toggle_school_management(self):
        if self.stackWidget.currentIndex() is 1:
            self.stackWidget.setCurrentIndex(0)
        else:
            self.stackWidget.setCurrentIndex(1)


# --------------------------------------------------------------------------- #
# Define functions
# --------------------------------------------------------------------------- #
def main():
    global app, mainwin
    app = QApplication(sys.argv)
    mainwin = MainWin()
    sys.exit(app.exec_())


# --------------------------------------------------------------------------- #
# Define module globals
# --------------------------------------------------------------------------- #
log = logging.getLogger(__name__)
app = None  # the QApplication instance
mainwin = None  # the main window of the application
