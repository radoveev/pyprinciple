# -*- coding: utf-8 -*-
"""

Copyright (C) 2017 Radomir Matveev GPL 3.0+

"""

# --------------------------------------------------------------------------- #
# Import libraries
# --------------------------------------------------------------------------- #
#from string import Template

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QSizePolicy,
                             QListView, QPushButton, QFrame, QStackedWidget,
                             QGridLayout, QHBoxLayout, QVBoxLayout,
                             QStackedLayout)
from PyQt5.QtCore import (Qt, pyqtSlot, QSize, QItemSelection,
                          QItemSelectionModel, QStringListModel)
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QColor, QIcon

from widgets import QScalingNoticeBoard, QIconPushButton
import common as cmn
import style
from person_interaction import PersonInteraction


# --------------------------------------------------------------------------- #
# Define classes
# --------------------------------------------------------------------------- #
class LocationView(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ppl = []
        # create widgets
        self.stack = QStackedWidget(self)
        self.location_page = QWidget()
        self.location_widget = LocationPage(self.location_page)
        self.phone_page = SmartPhone()

        # create layout
        box = QHBoxLayout(self.location_page)
        box.addWidget(self.location_widget)

        self.stack.layout().setStackingMode(QStackedLayout.StackAll)
        self.stack.addWidget(self.location_page)
        self.stack.addWidget(self.phone_page)

        layout = QHBoxLayout(self)
        layout.addWidget(self.stack)

        # connect signals
        mainwin = self.parent()
        self.location_widget.push_alt_views[0].clicked.connect(
                mainwin.show_school_management
                )
        self.location_widget.phone_btn.clicked.connect(self.toggle_phone)
        self.phone_page.return_btn.clicked.connect(self.toggle_phone)

    def addPerson(self, person):
        self.ppl.append(person)
        self.location_widget.people_list.model().setStringList(self.forenames)

    def removePerson(self, person):
        pass  # TODO

    @property
    def forenames(self):
        return [p.forename for p in self.ppl]

    @pyqtSlot()
    def toggle_phone(self):
        if self.stack.currentIndex() is 0:
            self.stack.setCurrentIndex(1)
            self.phone_page.setFocus()
        else:
            self.stack.setCurrentIndex(0)
            self.setFocus()


class LocationPage(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO load this from the data layer
        self.name = "Your Home"  # the name of the shown location
        self.push_alt_views = []
        self.push_ctl = []
        nrof_controls = 2
        # create widgets
        self.site_view = QScalingNoticeBoard(parent=self)
        self.person_interact = PersonInteraction(self)
        self.people_list = QListView(self)
        self.calendar_notes_lbl = QLabel(self)
        self.person_site_lbl = QLabel(self)
        self.phone_btn = QPushButton(self)
        self.inventory_btn = QPushButton(self)
        self.map_btn = QPushButton(self)

        # create layout
        grid = QGridLayout(self)
        grid.setRowStretch(0, 2)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 7)
        grid.setColumnStretch(2, 2)
        grid.addWidget(self.site_view, 0, 0, 1, 2)
        grid.addWidget(self.people_list, 0, 2, 1, 1)

        hbox = QHBoxLayout()
        hbox.addWidget(self.phone_btn)
        hbox.addWidget(self.inventory_btn)
        hbox.addWidget(self.map_btn)
        grid.addLayout(hbox, 1, 0, 1, 1)

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
        selectionModel.selectionChanged.connect(self.on_selectionChanged)

        self.site_view.show()

    def setImage(self, path):
        self.site_view.setPixmap(QPixmap(str(path)))

    def retranslateUi(self):
        tra = QApplication.translate
        ctxt = "LocationView"
        self.person_site_lbl.setText(tra(ctxt, "Oliver Klozoff | Lubriscity"))
        self.calendar_notes_lbl.setText(
                tra(ctxt, "No calendar notes for today")
                )
        self.phone_btn.setText(tra(ctxt, "&Smartphone"))
        self.inventory_btn.setText(tra(ctxt, "&Inventory"))
        self.map_btn.setText(tra(ctxt, "&Map"))
        self.push_ctl[0].setText(tra(ctxt, "Settings"))
        self.push_ctl[1].setText(tra(ctxt, "&Debug"))
        btnnames = [data[0] for data in world.locationButtons(self.name)]
        for btn, text in zip(self.push_alt_views, btnnames):
            btn.setText(tra(ctxt, text))

    @pyqtSlot(QItemSelection, QItemSelection)
    def on_selectionChanged(self, selected, deselected):
        # TODO: implement blur
#        self.site_view.toggle_blur()
#        self.person_interact.setVisible(True)
        self.person_interact.exec()


class SmartPhone(QScalingNoticeBoard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # create widgets
        self.return_btn = QIconPushButton(self)
        self.display = QLabel(self)

        # create layout
        btnwidth = 70
        btnheight = 70
#        self.return_btn.setGeometry(510, 210, btnwidth,
#                                    btnheight)
        self.return_btn.setGeometry(117, 6, btnwidth, btnheight)
        self.addNotice(self.return_btn)

        # add apps buttons to display
        # display geometry is (35, 190, 565, 770)
        rowcount = 770 // btnheight
        colcount = 565 // btnwidth
        rowpad = (770 - ((rowcount - 4) * btnheight)) // (rowcount + 1)
        colpad = (565 - ((colcount - 4) * btnwidth)) // (colcount + 1)

        x = colpad + 45
        y = rowpad + 205
        apps = world.phoneApps()
        for row in range(rowcount):
            if not apps:
                break
            for col in range(colcount):
                try:
                    tooltip, iconpath = apps.pop()
                except IndexError:
                    break
                btn = QIconPushButton(self)
                btn.setToolTip(tooltip)
                btn.setGeometry(x, y, btnwidth, btnheight)
                btn.setIcon(QIcon(QPixmap(str(iconpath))))
                self.addNotice(btn)
                x += colpad + btnwidth
            y += rowpad + btnheight

        # configure widgets
        self.retranslateUi()

        self.setEnabled(True)

#        sheet = Template(
#                """QPixmapLabel { background: none; }
#                QPushButton { min-width: ${w}; min-height: ${h}px;
#                              max-width: ${w}; max-height: ${h}px;
#                             }
#                """
#                ).substitute(w=btnwidth, h=btnheight)
        sheet = """QPixmapLabel { background: none; }
                .QLabel { background: none; }
                QPushButton { min-width: 0; min-height: 0;
                              max-width: 16777000; max-height: 16777000;
                             }
                """
        self.setStyleSheet(sheet)

        path = cmn.resdir / "icons/SmartphoneOff.png"
        pixmap = QPixmap(str(path))
#        pixmap = pixmap.scaled(btnwidth - 5, btnheight - 5,
#                               transformMode=Qt.SmoothTransformation)
        self.return_btn.setIcon(QIcon(pixmap))

        path = (cmn.schooldir /
                "Images/EventPictures/Custom/SmartphoneBackground.png")
        self.setPixmap(QPixmap(str(path)))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.return_btn.click()

    def retranslateUi(self):
        tra = QApplication.translate
        ctxt = "SmartPhone"
        self.return_btn.setToolTip((tra(ctxt, "Stop using your smartphone")))


# --------------------------------------------------------------------------- #
# Define module globals
# --------------------------------------------------------------------------- #
world = cmn.world
