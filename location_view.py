# -*- coding: utf-8 -*-
"""

Copyright (C) 2017 Radomir Matveev GPL 3.0+

"""

# --------------------------------------------------------------------------- #
# Import libraries
# --------------------------------------------------------------------------- #
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QSizePolicy,
                             QListView, QPushButton, QFrame,
                             QGridLayout, QHBoxLayout)
from PyQt5.QtCore import (Qt, pyqtSlot, QItemSelection, QItemSelectionModel,
                          QStringListModel)
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QColor

from widgets import QScalingNoticeBoard
import common as cmn
import style
from person_interaction import PersonInteraction


# --------------------------------------------------------------------------- #
# Define classes
# --------------------------------------------------------------------------- #
class LocationView(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO load this from the data layer
        self.name = "Your Home"  # the name of the shown location
        self.ppl = []
        self.push_alt_views = []
        self.push_actions = []
        self.push_ctl = []
        nrof_actions = 3
        nrof_controls = 2
        # create widgets
        self.site_view = QScalingNoticeBoard(parent=self)
        self.person_interact = PersonInteraction(self)
        self.people_list = QListView(self)
        self.calendar_notes_lbl = QLabel(self)
        self.person_site_lbl = QLabel(self)

        # create layout
        grid = QGridLayout(self)
        grid.setRowStretch(0, 2)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 7)
        grid.setColumnStretch(2, 2)
        grid.addWidget(self.site_view, 0, 0, 1, 2)
        grid.addWidget(self.people_list, 0, 2, 1, 1)

        hbox2 = QHBoxLayout()
        for _ in range(nrof_actions):
            pushbtn = QPushButton(self)
            hbox2.addWidget(pushbtn)
            self.push_actions.append(pushbtn)
        grid.addLayout(hbox2, 1, 0, 1, 1)

        grid.addWidget(self.calendar_notes_lbl, 1, 1, 1, 1)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.person_site_lbl, 2, Qt.AlignLeft)

        for _ in range(nrof_controls):
            pushbtn = QPushButton(self)
            hbox3.addWidget(pushbtn)
            self.push_ctl.append(pushbtn)
        grid.addLayout(hbox3, 1, 2, 1, 1)

        self.setLayout(grid)

        # configure widgets
        self.setContentsMargins(0, 0, 0, 0)
        self.person_site_lbl.setObjectName("text")  # use text style
        self.calendar_notes_lbl.setObjectName("text")
        self.calendar_notes_lbl.setAlignment(Qt.AlignCenter)
        maximized = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        maximized.setHorizontalStretch(0)
        maximized.setVerticalStretch(0)
        self.setSizePolicy(maximized)
#        self.site_view.setScaledContents(True)

        model = QStringListModel()
#        model.setStringList(self.forenames)
        self.people_list.setModel(model)
        self.people_list.setStyleSheet(style.people_list_style)
        self.people_list.setEditTriggers(QListView.NoEditTriggers)
        self.people_list.setProperty("showDropIndicator", False)
        self.people_list.setDefaultDropAction(Qt.IgnoreAction)
        selectionModel = QItemSelectionModel(model)
        self.people_list.setSelectionModel(selectionModel)

        self.setImage(world.locationImage(self.name))

        # TODO: location buttons belong to a location
        btn_size = (100, 35)
        for text, pos in world.locationButtons(self.name):
            pushbtn = QPushButton(self.site_view)
            pushbtn.setGeometry(*pos, *btn_size)
            pushbtn.setText(text)
            pushbtn.setToolTip(text)
            notice = self.site_view.addNotice(pushbtn)
            notice.setFixedGeometry(True)
            self.push_alt_views.append(pushbtn)

        self.retranslateUi()

        # connect signals
        self.push_alt_views[0].clicked.connect(
                self.parent().toggle_school_management)
        selectionModel.selectionChanged.connect(self.on_selectionChanged)

        self.site_view.show()

    def addPerson(self, person):
        self.ppl.append(person)
        self.people_list.model().setStringList(self.forenames)

    def removePerson(self, person):
        pass  # TODO

    def setImage(self, path):
        self.site_view.setPixmap(QPixmap(str(path)))

    def retranslateUi(self):
        tra = QApplication.translate
        ctxt = "LocationView"
        self.person_site_lbl.setText(tra(ctxt, "Oliver Klozoff | Lubriscity"))
        self.calendar_notes_lbl.setText(
                tra(ctxt, "No calendar notes for today")
                )
        self.push_actions[0].setText(tra(ctxt, "Smartphone"))
        self.push_actions[1].setText(tra(ctxt, "Inventory"))
        self.push_actions[2].setText(tra(ctxt, "Map"))
        self.push_ctl[0].setText(tra(ctxt, "Settings"))
        self.push_ctl[1].setText(tra(ctxt, "Debug"))
        btnnames = [data[0] for data in world.locationButtons(self.name)]
        for btn, text in zip(self.push_alt_views, btnnames):
            btn.setText(tra(ctxt, text))

    @property
    def forenames(self):
        return [p.forename for p in self.ppl]

    @pyqtSlot(QItemSelection, QItemSelection)
    def on_selectionChanged(self, selected, deselected):
        # TODO: implement blur
#        self.site_view.toggle_blur()
#        self.person_interact.setVisible(True)
        self.person_interact.exec()


# --------------------------------------------------------------------------- #
# Define module globals
# --------------------------------------------------------------------------- #
world = cmn.world
