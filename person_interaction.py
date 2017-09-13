# -*- coding: utf-8 -*-
"""

Copyright (C) 2017 Radomir Matveev GPL 3.0+

"""

# --------------------------------------------------------------------------- #
# Import libraries
# --------------------------------------------------------------------------- #
from pathlib import Path

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QFrame, QListView, QSizePolicy, QDialog,
                             QVBoxLayout,
                             QGridLayout)
from PyQt5.QtCore import Qt, pyqtSlot, QRect
from PyQt5.QtGui import QBrush, QColor, QPalette, QFont


# --------------------------------------------------------------------------- #
# Define classes
# --------------------------------------------------------------------------- #
class PersonInteraction(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # create widgets
        self.Interaction_view = QListView(self)
        self.Interaction_Label = QLabel(self)
        self.Category_view = QListView(self)
        self.Category_Label = QLabel(self)
        self.interaction_subject = QLabel(self)
#        self.frame = QFrame(self)
#        self.BackBtn = QPushButton(self.frame)
        self.BackBtn = QPushButton(self)

        # create layouts
        vbox = QVBoxLayout(self)
#        grid = QGridLayout(self)

        vbox.addWidget(self.interaction_subject)
        vbox.addWidget(self.Category_Label)

#        sizePolicy = QSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
#        sizePolicy.setHorizontalStretch(0)
#        sizePolicy.setVerticalStretch(0)
#        sizePolicy.setHeightForWidth(
#                self.Category_view.sizePolicy().hasHeightForWidth())
        # TODO: does this work? I think Category_view will get the same sizePolicy as  Interaction_View
#        self.Category_view.setSizePolicy(sizePolicy)
#        grid.addWidget(self.Category_view, 2, 9, 1, 1)
        vbox.addWidget(self.Category_view)

        vbox.addWidget(self.Interaction_Label)

#        sizePolicy.setHeightForWidth(
#                self.Interaction_view.sizePolicy().hasHeightForWidth())
#        self.Interaction_view.setSizePolicy(sizePolicy)
#        grid.addWidget(self.Interaction_view, 4, 9, 1, 1)
        vbox.addWidget(self.Interaction_view)

#        grid.addWidget(self.Category_Label, 1, 9, 1, 1)
#        grid.addWidget(self.Interaction_Label, 3, 9, 1, 1)
#        grid.addWidget(self.interaction_subject, 0, 9, 1, 1)
#        grid.addWidget(self.frame, 6, 9, 1, 1)
#        vbox.addWidget(self.frame)
        vbox.addWidget(self.BackBtn)

#        self.setLayout(grid)
        self.setLayout(vbox)

        # style widgets
        self.Category_Label.setPalette(text_palette)
        self.Category_Label.setFont(font2)
        self.Category_Label.setAlignment(text_align)
        self.Interaction_Label.setPalette(text_palette)
        self.Interaction_Label.setFont(font2)
        self.Interaction_Label.setAlignment(text_align)
        self.interaction_subject.setPalette(text_palette)
        self.interaction_subject.setFont(font3)
        self.interaction_subject.setAlignment(text_align)
#        self.frame.setFrameShape(QFrame.StyledPanel)
#        self.frame.setFrameShadow(QFrame.Plain)

        # configure widgets
#        self.BackBtn.setGeometry(QRect(140, 170, 91, 25))

        # connect signals
        self.BackBtn.clicked.connect(self.accept)

        self.retranslateUi()
#        self.setVisible(True)
#        self.hide()

    def retranslateUi(self):
        tra = QApplication.translate
        self.Category_Label.setText(tra("HHSpp", "Category"))
        self.Interaction_Label.setText(tra("HHSpp", "Interaction"))
        self.interaction_subject.setText(tra("HHSpp", "Susan Hooter"))
        self.BackBtn.setText(tra("HHSpp", "Back"))

#    @pyqtSlot()
#    def on_hide(self):
#        self.setVisible(False)
#        self.hide()
#        pass


# --------------------------------------------------------------------------- #
# Define module globals
# --------------------------------------------------------------------------- #
white_brush = QBrush(QColor(255, 255, 255, 255))
gray_brush = QBrush(QColor(190, 190, 190, 255))
text_palette = QPalette()
text_palette.setBrush(QPalette.Active, QPalette.WindowText, white_brush)
text_palette.setBrush(QPalette.Inactive, QPalette.WindowText, white_brush)
text_palette.setBrush(QPalette.Disabled, QPalette.WindowText, gray_brush)
font2 = QFont()
font2.setPointSize(14)
font3 = QFont("sans", 14)
text_align = Qt.AlignBottom | Qt.AlignLeading | Qt.AlignLeft
