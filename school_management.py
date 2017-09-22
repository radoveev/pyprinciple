# -*- coding: utf-8 -*-
"""This module contains the school management window of pyprinciple

Copyright (C) 2017 Radomir Matveev GPL 3.0+
"""

# --------------------------------------------------------------------------- #
# Import libraries
# --------------------------------------------------------------------------- #
from pathlib import Path
from collections import OrderedDict

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QFrame, QListView, QListWidget, QListWidgetItem,
                             QSizePolicy, QDialog, QGraphicsView, QTabWidget,
                             QTableWidget, QTableWidgetItem, QProgressBar,
                             QTextEdit, QColumnView, QCheckBox, QComboBox,
                             QItemEditorFactory, QStyledItemDelegate,
                             QHBoxLayout, QVBoxLayout, QGridLayout,
                             QFormLayout,
                             QTableView, QHeaderView, QSpacerItem)
from PyQt5.QtCore import (Qt, pyqtSlot, QRect, QLocale, QVariant,
                          QAbstractTableModel, QModelIndex)
from PyQt5.QtGui import QBrush, QColor, QPalette, QFont, QPainter
from PyQt5.QtChart import QChart, QChartView, QLineSeries

from widgets import QPixmapLabel, QEditableTableModel
import common as cmn
import style


# --------------------------------------------------------------------------- #
# Define classes
# --------------------------------------------------------------------------- #
class StatsTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#        self.dataseries = []  # list of QLineSeries dummy data
#        self.dataitems = []  # list of QListWidgetItem
        self.seriesmap = {}  # map items to series
        # create widgets
        self.statList = QListWidget(self)
        chart = QChart()
        self.chartView = QChartView(chart, self)

        for i in range(30):
            series = QLineSeries(self)
            for j in range(20):
                series.append(j, i * 3 + j)

            item = QListWidgetItem()
            item.setData(Qt.DisplayRole, str(i))
            item.setData(Qt.UserRole, i)

            if i < 10:
                item.setData(Qt.CheckStateRole, Qt.Checked)
            else:
                item.setData(Qt.CheckStateRole, Qt.Unchecked)
                series.hide()

            chart.addSeries(series)
            self.statList.addItem(item)
            self.seriesmap[i] = series

        # create layout
        layout = QHBoxLayout(self)
        layout.addWidget(self.statList)
        layout.addWidget(self.chartView)
        layout.setStretchFactor(self.chartView, 3)

        # configure widgets
        chart.legend().hide()
        chart.createDefaultAxes()
        chart.setTitle("Daily aggregated stats of your school")
        self.chartView.setRenderHint(QPainter.Antialiasing)

        # connect signals
        self.statList.itemClicked.connect(self.on_stat_clicked)

    @pyqtSlot(QListWidgetItem)
    def on_stat_clicked(self, item):
        key = item.data(Qt.UserRole)
        series = self.seriesmap[key]
        series.setVisible(not series.isVisible())
#        if series.isVisible():
#            series.hide()
#        else:
#            series.show()


class AccountingTab(QWidget):
    """

    TODO: style

    balanceLbl.setPalette(HHStyle::white_text);
    balanceVal.setPalette(HHStyle::white_text);

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # create widgets
        self.table = QTableWidget(len(balanceItem), 4, self)
        self.balanceLbl = QLabel(self)
        self.balanceVal = QLabel(self)
#        vertStretch = QSpacerItem()

        # create layouts
        layout = QGridLayout(self)
        layout.addWidget(self.balanceLbl, 0, 0, 1, 1)
        layout.addWidget(self.balanceVal, 0, 1, 1, 1)
        self.table.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        layout.addWidget(self.table, 1, 0, 20, 30)

        # configure widgets
        self.table.setStyleSheet(
                """QTableWidget {background-color: rgb(254, 245, 232);
                alternate-background-color: rgb(230, 230, 230);}""")
        self.table.verticalHeader().hide()
        self.table.setAlternatingRowColors(True)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionMode(QTableWidget.NoSelection)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

        self.retranslateUi()

    def retranslateUi(self):
        tra = QApplication.translate
        self.balanceLbl.setText(tra("AccountingTab", "Monthly Loss:"))
        self.balanceVal.setText(tra("AccountingTab", "-$10,000"))
        red = QColor(200, 0, 0)
        black = QColor(0, 0, 0)
        for i, data in enumerate(zip(balanceItem, balanceItemExample)):
            name, val = data
            item = QTableWidgetItem(tra("AccountingTab", name))
            item.setForeground(QBrush(red if val < 0 else black))
            self.table.setItem(i, 0, QTableWidgetItem(item))
            item.setText(QLocale().toCurrencyString(val))
            self.table.setItem(i, 1, QTableWidgetItem(item))
            item.setText(QLocale().toCurrencyString(7 / 30 * val)
                         if i > 2 and i != 5 else "")
            self.table.setItem(i, 2, QTableWidgetItem(item))
            item.setText(QLocale().toCurrencyString(val / 30)
                         if i > 2 and i != 5 else "")
            self.table.setItem(i, 3, QTableWidgetItem(item))

        self.table.setHorizontalHeaderLabels((
                tra("AccountingTab", "Account"),
                tra("AccountingTab", "Monthly"),
                tra("AccountingTab", "Weekly"),
                tra("AccountingTab", "Daily")
                ))


class ClubsTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clubinfo = QFormLayout()
        # create widgets
        self.name_field = QLabel(self)
        self.members_field = QLabel(self)
        self.president_field = QLabel(self)
        self.balance_field = QLabel(self)
        self.time_field = QLabel(self)
        self.location_field = QLabel(self)
        self.openbtn = QPushButton(self)
        self.new_clubs_lbl = QLabel(self)
        self.active_clubs_lbl = QLabel(self)
        self.new_clubs_list = QListView(self)
        self.active_clubs_list = QListView(self)
        self.clubimage = QPixmapLabel(self)
        self.presidentview = QGraphicsView(self)

        # create layouts
        self.clubinfo.addRow("Name", self.name_field)
        self.clubinfo.addRow("Members", self.members_field)
        self.clubinfo.addRow("Club President", self.president_field)
        self.clubinfo.addRow("Weekly Balance", self.balance_field)
        self.clubinfo.addRow("Time", self.time_field)
        self.clubinfo.addRow("Location", self.location_field)

        grid = QGridLayout(self)
        grid.addWidget(self.new_clubs_lbl,      0, 0)
        grid.addWidget(self.new_clubs_list,     1, 0, 10, 1)
        grid.addWidget(self.clubimage,          12, 0, 10, 1)

        grid.addWidget(self.openbtn,            10, 1)
        grid.addLayout(self.clubinfo,           12, 1, 10, 1)

        grid.addWidget(self.active_clubs_lbl,   0, 2)
        grid.addWidget(self.active_clubs_list,  1, 2, 10, 1)
        grid.addWidget(self.presidentview,      12, 2, 10, 1)

        for row in range(12, 22):
            grid.setRowStretch(row, 10)
        grid.setColumnStretch(0, 2)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 2)

        # configure widgets
        self.retranslateUi()

    def retranslateUi(self):
        tra = QApplication.translate
        ctxt = "ClubsTab"  # the translation context
        self.openbtn.setText(tra(ctxt, "Open"))
        self.new_clubs_lbl.setText(tra(ctxt, "Available Clubs"))
        self.active_clubs_lbl.setText(tra(ctxt, "Active Clubs"))
        cmn.translate_form(self.clubinfo, ctxt,
                           ("Name", "Members", "Club President",
                            "Weekly Balance", "Time", "Location")
                           )


class ExpansionsTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#        grid = QGridLayout()
#        self.expansionList = QListView()
#        self.upgradeCostLbl = QLabel()
#        self.upgradeCostVal = QLabel()
#        self.maintenanceCostLbl = QLabel()
#        self.maintenanceCostVal = QLabel()
#        self.upgradeBtn = QPushButton()
#        self.expansionViewLbl = QLabel()
#        self.lowInfoLbl = QLabel()

        self.costform = QFormLayout()
        # create widgets
        self.upgradebtn = QPushButton(self)
        self.expansionimage = QPixmapLabel(self)
        self.upgrade_cost_lbl = QLabel(self)
        self.maintenance_cost_lbl = QLabel(self)
        self.expansionlist = QListView(self)
        self.expansiontext = QTextEdit(self)

        # create layout
        self.costform.addRow("Upgrade cost", self.upgrade_cost_lbl)
        self.costform.addRow("Maintenance cost", self.maintenance_cost_lbl)

        btnbox = QHBoxLayout()
        btnbox.addWidget(self.upgradebtn)
        btnbox.addLayout(self.costform)

        leftbox = QVBoxLayout()
        leftbox.addLayout(btnbox)
        leftbox.addWidget(self.expansionlist)
        leftbox.addWidget(self.expansiontext)

        layout = QHBoxLayout(self)
        layout.addLayout(leftbox)
        layout.addWidget(self.expansionimage)

        # configure widgets
        self.retranslateUi()
        # TODO: load image

    def retranslateUi(self):
        tra = QApplication.translate
        ctxt = "ExpansionsTab"  # the translation context
        self.upgradebtn.setText(tra(ctxt, "Upgrade"))
        cmn.translate_form(self.costform, ctxt,
                           ("Upgrade cost", "Maintenance cost")
                           )


class PolicyTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # create widgets
        self.explanation_lbl = QLabel(self)
#        self.topic_lbl = QLabel(self)
#        self.rule_lbl = QLabel(self)
        self.policy_view = QColumnView(self)
        self.policy_text = QTextEdit(self)

        # create layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.explanation_lbl)
        layout.addWidget(self.policy_view)
        layout.addWidget(self.policy_text)

        # configure widgets
        self.retranslateUi()
        # TODO: load policies from scenario and display them

    def retranslateUi(self):
        tra = QApplication.translate
        ctxt = "PolicyTab"  # the translation context
        infotxt = ("This tab lets you adjust your school policies.\n" +
                   "Enacted rules may directly impact the stats of the " +
                   "affected persons on a daily basis or influence the " +
                   "outcome of certain ingame events.")
        self.explanation_lbl.setText(tra(ctxt, infotxt))
#        self.topic_lbl.setText(tra(ctxt, "Topic"))
#        self.rule_lbl.setText(tra(ctxt, "Rule"))
        # TODO: translate policy text


class AssignmentsTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.chbmap = {}  # maps checkbox ids to teacher, subject tuples
        # create widgets
        self.explanation_lbl = QLabel(self)
        self.table = QTableWidget(len(subjectName), len(teacher), self)
        for r in range(len(subjectName)):
            for c in range(len(teacher)):
                chb = QCheckBox(self.table)
                self.table.setCellWidget(r, c, chb)
                self.chbmap[chb] = (teacher[c], subjectName[r])
        self.nameLbl = QLabel(self)
        self.subjNameLbl = QLabel(self)
        self.subjExpLbl = QLabel(self)
        self.genQualfLbl = QLabel(self)
        self.subjExpPB = QProgressBar(self)
        self.genQualfPB = QProgressBar(self)

        # create layout
        subjectgrid = QGridLayout()
        subjectgrid.addWidget(self.nameLbl,     0, 0, 1, 2)
        subjectgrid.addWidget(self.subjNameLbl, 0, 4, 1, 1)
        subjectgrid.addWidget(self.subjExpLbl,  1, 1, 1, 1)
        subjectgrid.addWidget(self.subjExpPB,   1, 2, 1, 3)
        subjectgrid.addWidget(self.genQualfLbl, 2, 1, 1, 1)
        subjectgrid.addWidget(self.genQualfPB,  2, 2, 1, 3)

        layout = QVBoxLayout(self)
        layout.addWidget(self.explanation_lbl)
        layout.addWidget(self.table, 2)  # set stretch factor to 2
        layout.addLayout(subjectgrid)

        # configure widgets
        self.retranslateUi()

        self.table.setStyleSheet("""
                QTableWidget {background: rgb(41, 60, 67);
                              gridline-color: white;}
                QCheckBox {margin-left: 50%; margin-right:50%;}
                QHeaderView::section, QTableCornerButton::section {
                        1px solid white; background: rgb(25, 45, 52);
                        color:white;}
                """)
#        minimum = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
#        self.table.setSizePolicy(minimum)
#        preferred = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
#        self.table.setSizePolicy(preferred)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalHeaderLabels(teacher)
        self.table.setVerticalHeaderLabels(subjectName)
        # TODO: icons

        self.nameLbl.setPalette(style.white_text)
        self.subjNameLbl.setPalette(style.white_text)
        self.subjExpLbl.setPalette(style.white_text)
        self.subjExpPB.setPalette(style.progress_bar)
        self.subjExpPB.setValue(60)
        self.subjExpPB.setTextVisible(False)
        self.genQualfLbl.setPalette(style.white_text)
        self.genQualfPB.setPalette(style.progress_bar)
        self.genQualfPB.setValue(60)
        self.genQualfPB.setTextVisible(False)

    def retranslateUi(self):
        tra = QApplication.translate
        ctxt = "AssignmentsTab"  # the translation context
        infotxt = (
"This tab lets you assign which subjects can be taught by which teacher. " +
"Subjects must be assigned to a teacher in this panel before they can be " +
"selected in the curriculum.\n\n" +
"Every teacher has a specific amount of subject experience in the " +
"inidividual subjects, which increases naturally over time as the subject " +
"is taught by that teacher.\n" +
"The general qualification to teach a subject is determined by the " +
"teacher's current stats that are relevant for the specific subject. " +
"It improves as the teacher's stats\nimprove. Some subjects share a " +
"common field, so gaining qualification for one subject may also improve " +
"the qualification for a related subject. Each subject may have\n" +
"different effects on the stats of teachers and students alike, but " +
"teachers with higher subject experience and qualification will increase " +
"those effects even further.\n\n"+
"Checked entries in this list are the available subjects that this person " +
"is allowed to teach."
                   )
        self.explanation_lbl.setText(tra(ctxt, infotxt))
        # TODO: translate labels from lower grid layout


class JobsTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.subLbl = []  # labels for subject name array
        self.avgSubjExpVal = []
        self.teacherDisplay = QGraphicsView()

        self.subj_exp_bars = []  # list of subject experience progress bars
        # create widgets
        self.applicants_lbl = QLabel(self)
        self.applicants_list = QListView(self)
        self.staff_lbl = QLabel(self)
        self.staff_list = QListView(self)
        self.hire_btn = QPushButton(self)
        self.income_lbl = QLabel(self)
        self.salary_lbl = QLabel(self)
        self.biography_lbl = QLabel(self)
        self.biography_val = QLabel(self)
        self.avgSubjExpHdrLbl = QLabel(self)
        for name in subjectFamilies:
            self.subj_exp_bars.append(QProgressBar(self))
        self.teacher_view = QGraphicsView(self)

        # create layout
        self.balanceform = QFormLayout()
        self.balanceform.addRow("Monthly Income:", self.income_lbl)
        self.balanceform.addRow("Staff Salary:", self.salary_lbl)

        self.subjectform = QFormLayout()
        for name, bar in zip(subjectFamilies, self.subj_exp_bars):
            self.subjectform.addRow(name, bar)

        layout = QGridLayout(self)
        layout.addWidget(self.applicants_lbl,   0, 0, 1, 1)
        layout.addWidget(self.applicants_list,  1, 0, 5, 1)
        layout.addLayout(self.balanceform,      1, 2)
        layout.addWidget(self.staff_lbl,        0, 4, 1, 1)
        layout.addWidget(self.staff_list,       1, 4, 5, 1)
        layout.addWidget(self.hire_btn,         3, 2, 1, 1)
        layout.addWidget(self.biography_lbl,    6, 0)
        layout.addWidget(self.biography_val,    7, 0, 1, 3)
        layout.addWidget(self.avgSubjExpHdrLbl, 8, 0)
        layout.addLayout(self.subjectform,      9, 0, -1, 2)
        layout.addWidget(self.teacher_view,     6, 4, -1, -1)

        # configure widgets
        self.retranslateUi()

        # TODO: set background of tab to dark color
        self.biography_lbl.setPalette(style.white_text)
        self.biography_val.setAlignment(Qt.AlignTop)
        self.avgSubjExpHdrLbl.setPalette(style.white_text)
        for bar in self.subj_exp_bars:
            bar.setPalette(style.progress_bar)
            bar.setValue(60)
            bar.setTextVisible(False)
        self.teacher_view.setStyleSheet("background: transparent")

    def retranslateUi(self):
        tra = QApplication.translate
        self.applicants_lbl.setText(tra("JobsTab", "Available Applicants"))
        self.staff_lbl.setText(tra("JobsTab", "Hired Staff"))
        self.hire_btn.setText(tra("JobsTab", "Hire"))
        self.biography_lbl.setText(tra("JobsTab", "Biography:"))
        self.avgSubjExpHdrLbl.setText(tra("JobsTab",
                                          "Average Subject Family Experience"))
        # TODO: translate biography_val
        cmn.translate_form(self.balanceform, "JobsTab",
                           ("Monthly Income:", "Staff Salary:"))
        cmn.translate_form(self.subjectform, "JobsTab", subjectFamilies)


class TimeTableDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        combo.setEditable(False)
        combo.addItems(subjectName)
        model = parent.parent().model()
        displayed = model.data(index)
        combo.setCurrentText(displayed)
        return combo

#    def setEditorData(self, editor, index):
#        super().setEditorData(editor, index)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText(), Qt.DisplayRole)


class TimeTableModel(QEditableTableModel):
    def __init__(self, parent=None):
        super().__init__(world.schoolDays(), world.timeTablePeriods(), parent)

        # TODO: also add Qt.ToolTipRole and maybe Qt.WhatsThisRole to headers
        # add data
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                item = self.createItem()
#                item.setData(subjectName[0], Qt.DisplayRole)
#                item.setData(subjectName[0], Qt.EditRole)
                item.setData("Double-click to edit", Qt.ToolTipRole)
                self.datamap[(row, col)] = item


class ClassesTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#        self.daymap = OrderedDict()  # maps days to
        # create widgets
        self.active_class = QComboBox(self)
        self.timetable = QTableView(self)

        # create layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.active_class)
        layout.addWidget(self.timetable)

        # configure widgets
        self.active_class.addItems(world.classNames())
        self.timetable.setModel(TimeTableModel())
        self.timetable.setCornerButtonEnabled(False)
        self.timetable.setShowGrid(False)
        self.timetable.setSortingEnabled(False)

        # configure widgets
        self.timetable.setItemDelegate(TimeTableDelegate())
#        delegate = self.timetable.itemDelegate()
#        delegate.setItemEditorFactory(TimeTableEditorFactory())
#        factory = delegate.itemEditorFactory()
#        if factory is None:
#            factory = QItemEditorFactory.defaultFactory()
#        print("factory", factory)
#        factory.registerEditor()
#        delegate.setItemEditorFactory()


class StudentsTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.biography = OrderedDict()
        self.family = OrderedDict()
        # create widgets
        self.classes_lbl = QLabel(self)
        self.class_list = QListView(self)
        self.add_class_btn = QPushButton(self)
        self.students_lbl = QLabel(self)
        self.faves_only_chb = QCheckBox(self)
        self.student_list = QListView(self)
        self.name_lbl = QLabel("Jane Wayne", self)
        self.sex_icon = QLabel(self)
        self.age_lbl = QLabel(self)
        self.birthday_lbl = QLabel(self)
        self.personality_lbl = QLabel(self)
        self.club_lbl = QLabel(self)
        self.location_lbl = QLabel(self)
        for key in ("age", "birthday", "personality", "club", "location"):
            self.biography[key] = QLabel(self)
        for key in ("father", "mother", "siblings"):
            self.family[key] = QLabel(self)
        self.grades_lbl = QLabel(self)
        self.grades_list = cmn.QProgressList("StudentsTab", self)
        for name in subjectName:
            self.grades_list.addBar(name)
        self.student_view = QGraphicsView(self)

        # create layout
#        classesbox = QVBoxLayout()
#        classesbox.addWidget(self.classes_lbl)
#        classesbox.addWidget(self.class_list)
#        classesbox.addWidget(self.add_class_btn)

        self.bio_form = QFormLayout()
        for key, field in self.biography.items():
            self.bio_form.addRow(key, field)

        self.family_form = QFormLayout()
        for key, field in self.family.items():
            self.family_form.addRow(key, field)

        layout = QGridLayout(self)
        layout.addWidget(self.classes_lbl,      0, 0)
        layout.addWidget(self.class_list,       1, 0, 3, 1)
        layout.addWidget(self.add_class_btn,    4, 0)
#        layout.addLayout(classesbox, 0, 0, -1, 1)
        layout.addWidget(self.students_lbl,     0, 1)
        layout.addWidget(self.faves_only_chb,   0, 2)
        layout.addWidget(self.student_list,     1, 1, -1, 2)
        layout.addWidget(self.name_lbl,         0, 3)
        layout.addWidget(self.sex_icon,         0, 4)
        layout.addLayout(self.bio_form,         1, 3)
        layout.addLayout(self.family_form,      1, 4)
        layout.addWidget(self.grades_lbl,       2, 3)
        layout.addWidget(self.grades_list,      3, 3, -1, 2)
        layout.addWidget(self.student_view,     0, 5, -1, 1)

        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 2)
        layout.setColumnStretch(4, 2)
        layout.setColumnStretch(5, 4)

        # configure widgets
        self.retranslateUi()
        sizepol = self.add_class_btn.sizePolicy()
        sizepol.setHorizontalPolicy(QSizePolicy.Fixed)
        self.add_class_btn.setSizePolicy(sizepol)

    def retranslateUi(self):
        tra = QApplication.translate
        ctxt = "StudentsTab"
        self.classes_lbl.setText(tra(ctxt, "Classes"))
        self.add_class_btn.setText(tra(ctxt, "Add class"))
        self.students_lbl.setText(tra(ctxt, "Students"))
        self.faves_only_chb.setText(tra(ctxt, "Show only favorites"))
        bio_labels = [key.capitalize() + ":" for key in self.biography]
        family_labels = [key.capitalize() + ":" for key in self.family]
        cmn.translate_form(self.bio_form, ctxt, bio_labels)
        cmn.translate_form(self.family_form, ctxt, family_labels)
        self.grades_lbl.setText(tra(ctxt, "Subject Scoring"))
        self.grades_list.retranslateUi()


class SchoolManagement(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # create widgets
        self.mainTab = QTabWidget(self)
        self.studentsTab = StudentsTab()
        self.classesTab = ClassesTab()
        self.jobsTab = JobsTab()
        self.assnTab = AssignmentsTab()
        self.policyTab = PolicyTab()
        self.expansionsTab = ExpansionsTab()
        self.clubsTab = ClubsTab()
        self.accountingTab = AccountingTab()
        self.statsTab = StatsTab()
        self.exitBtn = QPushButton()

        # create layouts
        layout = QVBoxLayout(self)
#        geom.setHeight(geom.height()*0.98);
#        geom.setWidth(geom.width()*0.98);
#        exitBtn.setGeometry(geom.width()-70, geom.top(), 70, 25);
#        self.mainTab.setGeometry(geom)
        self.mainTab.setContentsMargins(0, 0, 0, 0)
        # TODO: translate
        self.mainTab.addTab(self.classesTab, "Classes")
        self.mainTab.addTab(self.studentsTab, "Students")
        self.mainTab.addTab(self.jobsTab, "Jobs")
        self.mainTab.addTab(self.assnTab, "Teacher Assignments")
        self.mainTab.addTab(self.policyTab, "School Policy")
        self.mainTab.addTab(self.expansionsTab, "Expansions")
        self.mainTab.addTab(self.clubsTab, "Clubs")
        self.mainTab.addTab(self.accountingTab, "Accounting")
        self.mainTab.addTab(self.statsTab, "Stats")
        layout.addWidget(self.mainTab)
        layout.addWidget(self.exitBtn)

        fixedsize = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.exitBtn.setSizePolicy(fixedsize)

        # configure widgets
        self.mainTab.setStyleSheet(
                "QTabWidget { background-color: rgb(25, 45, 52);}")


        # connect signals
        self.exitBtn.clicked.connect(self.parent().toggle_school_management)

        # TODO: check if top part of tab handle reacts to interaction

        self.retranslateUi()

    def retranslateUi(self):
        tra = QApplication.translate
        self.exitBtn.setText(tra("SchoolManagement", "Exit"))
        # TODO: translate tab headers


# --------------------------------------------------------------------------- #
# Define module globals
# --------------------------------------------------------------------------- #
world = cmn.world
# TODO: fetch data from scenario
teacher = ("April Raymund", "Beth Manili", "Carl Walker", "Carmen Smith",
           "Claire Fuzushi", "Jessica Underwood", "Nina Parker",
           "Ronda Bells", "Samantha Keller")
subjectName = ("Anatomy Class", "Art", "Biology", "Bondage Class",
               "Chemistry", "Computer Science", "Economics", "English",
               "Geography", "History", "Math", "Music", "Philosophy",
               "Physics", "Practical Sex Education", "Religion",
               "School Sport", "Swimming", "Theoretical Sex Education"
               )
subjectFamilies = ("Mathematics", "Language Arts", "Natural Science",
                   "Life Science", "Computer Studies", "Social Science",
                   "Humanities", "Fine Arts", "Physical Education",
                   "Sexual Education")
balance = ["Monthly Loan:", "Staff Salary:"]
balanceExample = ["-$16,188", "$2,811"]
clubInfo = ["Members:", "time:", "Club President:", "Location:",
            "Weekly Balance:"]
clubInfoExample = ["12", "16:00-18:00", "Anette", "Sports Area", "-$50"]
balanceItem = ["State Funding",
    "Principal Salary",
    "Staff Salary",
    "Investigator",
    "Building Maintenance",
    "Cabaret Rental",
    "Bathroom Spycam Pics",
    "Changing Room Spycam Pics",
    "Cheerleading Club Spycam Pics",
    "Swim Club Spycam Pics",
    "Secret Panty Exchange sales",
    "Your Sister's rent"]
balanceItemExample = [18945, 2585, -34563, -3000, -1684, -600, 252, 504,
                      504, 352, 384, 400]