# -*- coding: utf-8 -*-
"""

Copyright (C) 2017 Radomir Matveev GPL 3.0+

TODO: style
    Calendar_notes.setPalette(HHStyle::white_text);
    Calendar_notes.setAlignment(Qt::AlignCenter);

    Person_site.setPalette(HHStyle::hdr_text);
    Person_site.setAlignment(Qt::AlignCenter);

"""

# --------------------------------------------------------------------------- #
# Import libraries
# --------------------------------------------------------------------------- #
from pathlib import Path

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QSizePolicy,
                             QStackedWidget, QListView, QPushButton, QFrame,
                             QGridLayout, QHBoxLayout)
from PyQt5.QtCore import (Qt, pyqtSlot, QItemSelection, QItemSelectionModel,
                          QStringListModel)
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QColor

from person_interaction import PersonInteraction
from widgets import QScalingNoticeBoard


# --------------------------------------------------------------------------- #
# Define classes
# --------------------------------------------------------------------------- #
class LocationView(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ppl = []
        self.push_alt_views = []
        self.push_actions = []
        self.push_ctl = []
        nrof_actions = 3
        nrof_controls = 2
        # create widgets
        # TODO: rename
        self.SW = QStackedWidget()
#        self.siteView = AspectRatioPixmapLabel(self)
        self.siteView = QScalingNoticeBoard(parent=self)
        self.pplInterAct = PersonInteraction(self)
        self.pplListView = QListView()
        self.Calendar_notes = QLabel()
        self.Person_site = QLabel()

        # create layout
        grid = QGridLayout(self)

        grid.setRowStretch(0, 2)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 7)
        grid.setColumnStretch(2, 2)

        grid.addWidget(self.siteView, 0, 0, 1, 2)
        grid.addWidget(self.pplListView, 0, 2, 1, 1)

        hbox2 = QHBoxLayout()
        for _ in range(nrof_actions):
            pushbtn = QPushButton(self)
            hbox2.addWidget(pushbtn)
            self.push_actions.append(pushbtn)
        grid.addLayout(hbox2, 1, 0, 1, 1)

        grid.addWidget(self.Calendar_notes, 1, 1, 1, 1)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.Person_site, 2, Qt.AlignLeft)

        for _ in range(nrof_controls):
            pushbtn = QPushButton(self)
            hbox3.addWidget(pushbtn)
            self.push_ctl.append(pushbtn)
        grid.addLayout(hbox3, 1, 2, 1, 1)

        self.setLayout(grid)

        # configure widgets
        self.setContentsMargins(0, 0, 0, 0)
        maximized = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        maximized.setHorizontalStretch(0)
        maximized.setVerticalStretch(0)
        self.setSizePolicy(maximized)
#        self.siteView.setScaledContents(True)

        model = QStringListModel()
#        model.setStringList(self.forenames)
        self.pplListView.setModel(model)
        self.pplListView.setStyleSheet(pplliststyle)
        self.pplListView.setFrameShape(QFrame.NoFrame)
        self.pplListView.setFrameShadow(QFrame.Plain)
        self.pplListView.setLineWidth(0)
        self.pplListView.setEditTriggers(QListView.NoEditTriggers)
        self.pplListView.setProperty("showDropIndicator", False)
        self.pplListView.setDefaultDropAction(Qt.IgnoreAction)
        selectionModel = QItemSelectionModel(model)
        self.pplListView.setSelectionModel(selectionModel)

        # TODO: do not hardcode the location of game data
        path = (Path(QApplication.applicationDirPath()) /
                "../Schools/NormalSchool/Images/Locations/Your Home/empty.jpg")
        self.setImage(path.resolve())

        # TODO: location buttons belong to a location
        alt_view_btn = QPalette()
        brush8 = QBrush(QColor(166, 202, 240, 255))
        brush8.setStyle(Qt.SolidPattern)
        alt_view_btn.setBrush(QPalette.Active, QPalette.Button, brush8)
        alt_view_btn.setBrush(QPalette.Inactive, QPalette.Button, brush8)
        alt_view_btn.setBrush(QPalette.Disabled, QPalette.Button, brush8)

        btn_size = (100, 35)
        loc_btn_data = (
                ("Paperwork:\nManage School", (125, 370)),
                ("Kitchen:\nOpen Fridge", (100, 250)),
                ("Video Library:\nOpen Library", (650, 380)),
                ("Computer", (850, 400)))
        for text, pos in loc_btn_data:
            pushbtn = QPushButton(self.siteView)
            pushbtn.setGeometry(*pos, *btn_size)
            pushbtn.setText(text)
            pushbtn.setToolTip(text)
            pushbtn.setPalette(alt_view_btn)
            notice = self.siteView.addNotice(pushbtn)
            notice.setFixedGeometry(True)
            self.push_alt_views.append(pushbtn)

        # load translations
        tra = QApplication.translate
        self.Person_site.setText(tra("HHSpp", "Oliver Klozoff | Lubriscity"))
        self.Calendar_notes.setText(tra("HHSpp",
                                        "No calendar notes for today"))
        self.push_actions[0].setText(tra("HHSpp", "Smartphone"))
        self.push_actions[1].setText(tra("HHSpp", "Inventory"))
        self.push_actions[2].setText(tra("HHSpp", "Map"))
        self.push_ctl[0].setText(tra("HHSpp", "Settings"))
        self.push_ctl[1].setText(tra("HHSpp", "Debug"))

        # connect signals
        self.push_alt_views[0].clicked.connect(
                self.parent().toggle_school_management)
        selectionModel.selectionChanged.connect(self.on_selectionChanged)

        self.siteView.show()

    def addPerson(self, person):
        self.ppl.append(person)
        self.pplListView.model().setStringList(self.forenames)

    def removePerson(self, person):
        pass  # TODO

    def setImage(self, path):
        self.siteView.setPixmap(QPixmap(str(path)))

    @property
    def forenames(self):
        return [p.forename for p in self.ppl]

    @pyqtSlot(QItemSelection, QItemSelection)
    def on_selectionChanged(self, selected, deselected):
        # TODO: implement blur
#        self.siteView.toggle_blur()
#        self.pplInterAct.setVisible(True)
        self.pplInterAct.exec()


# --------------------------------------------------------------------------- #
# Define module globals
# --------------------------------------------------------------------------- #
pplliststyle = """color: rgb(255, 110, 249);
    selection-color: rgb(255, 110, 249);
    selection-background-color: rgb(10, 36, 106);
    background-color: qlineargradient(spread:reflect,
                                      x1:0.495, y1:0, x2:1, y2:0,
                                      stop:0.409574 rgba(19, 34, 39, 255),
                                      stop:1 rgba(25, 45, 52, 255));"""
