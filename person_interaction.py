# -*- coding: utf-8 -*-
"""

Copyright (C) 2017 Radomir Matveev GPL 3.0+

"""

# --------------------------------------------------------------------------- #
# Import libraries
# --------------------------------------------------------------------------- #
from PyQt5.QtWidgets import (QApplication, QLabel, QPushButton, QListView,
                             QDialog, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QPalette, QFont


# --------------------------------------------------------------------------- #
# Define classes
# --------------------------------------------------------------------------- #
class PersonInteraction(QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # create widgets
        self.interaction_view = QListView(self)
        self.interaction_lbl = QLabel(self)
        self.category_view = QListView(self)
        self.category_lbl = QLabel(self)
        self.interaction_subject = QLabel(self)
        self.back_btn = QPushButton(self)

        # create layouts
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.interaction_subject)
        vbox.addWidget(self.category_lbl)
        vbox.addWidget(self.category_view)
        vbox.addWidget(self.interaction_lbl)
        vbox.addWidget(self.interaction_view)
        vbox.addWidget(self.back_btn)
        self.setLayout(vbox)

        # style widgets
        self.category_lbl.setPalette(text_palette)
        self.category_lbl.setFont(font2)
        self.category_lbl.setAlignment(text_align)
        self.interaction_lbl.setPalette(text_palette)
        self.interaction_lbl.setFont(font2)
        self.interaction_lbl.setAlignment(text_align)
        self.interaction_subject.setPalette(text_palette)
        self.interaction_subject.setFont(font3)
        self.interaction_subject.setAlignment(text_align)
#        self.frame.setFrameShape(QFrame.StyledPanel)
#        self.frame.setFrameShadow(QFrame.Plain)

        # configure widgets
        self.retranslateUi()

        # connect signals
        self.back_btn.clicked.connect(self.accept)

#        self.setVisible(True)
#        self.hide()

    def retranslateUi(self):
        tra = QApplication.translate
        self.category_lbl.setText(tra("HHSpp", "Category"))
        self.interaction_lbl.setText(tra("HHSpp", "Interaction"))
        self.interaction_subject.setText(tra("HHSpp", "Susan Hooter"))
        self.back_btn.setText(tra("HHSpp", "Back"))


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
