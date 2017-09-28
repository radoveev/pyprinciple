# -*- coding: utf-8 -*-
"""This module contains the school management window of pyprinciple

Copyright (C) 2017 Radomir Matveev GPL 3.0+
"""

# --------------------------------------------------------------------------- #
# Import libraries
# --------------------------------------------------------------------------- #
from collections import OrderedDict

from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QListView, QListWidget, QListWidgetItem,
                             QSizePolicy, QGraphicsView, QTabWidget,
                             QTableWidget, QTableWidgetItem, QColumnView,
                             QPlainTextEdit, QCheckBox, QComboBox,
                             QStyledItemDelegate, QTableView, QHeaderView,
                             QHBoxLayout, QVBoxLayout, QGridLayout,
                             QFormLayout)
from PyQt5.QtCore import Qt, pyqtSlot, QLocale
from PyQt5.QtGui import QBrush, QColor, QPainter
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
        self.seriesmap = {}  # map items to series
        # create widgets
        self.stat_list = QListWidget(self)
        chart = QChart()
        self.chart_view = QChartView(chart, self)

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
            self.stat_list.addItem(item)
            self.seriesmap[i] = series

        # create layout
        layout = QHBoxLayout(self)
        layout.addWidget(self.stat_list)
        layout.addWidget(self.chart_view)
        layout.setStretchFactor(self.chart_view, 3)

        # configure widgets
        chart.legend().hide()
        chart.createDefaultAxes()
        chart.setTitle("Daily aggregated stats of your school")
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.retranslateUi()

        # connect signals
        self.stat_list.itemClicked.connect(self.on_stat_clicked)

    def retranslateUi(self):
        chart = self.chart_view.chart()
        chart.setTitle(QApplication.translate(
                "StatsTab", "Daily aggregated stats of your school"))

    @pyqtSlot(QListWidgetItem)
    def on_stat_clicked(self, item):
        key = item.data(Qt.UserRole)
        series = self.seriesmap[key]
        series.setVisible(not series.isVisible())


class AccountingTab(QWidget):
    """

    TODO: style

    balanceLbl.setPalette(HHStyle::white_text);
    balanceVal.setPalette(HHStyle::white_text);

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # create widgets
        self.table = QTableWidget(len(world.balanceItems()), 4, self)
        self.balance_lbl = QLabel(self)
        self.balance_val = QLabel(self)

        # create layouts
        layout = QGridLayout(self)
        layout.addWidget(self.balance_lbl, 0, 0, 1, 1)
        layout.addWidget(self.balance_val, 0, 1, 1, 1)
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
        self.balance_lbl.setText(tra("AccountingTab", "Monthly Loss:"))
        self.balance_val.setText(tra("AccountingTab", "-$10,000"))
        red = QColor(200, 0, 0)
        black = QColor(0, 0, 0)
        for i, data in enumerate(world.balanceItems()):
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

        self.cost_form = QFormLayout()
        # create widgets
        self.upgrade_btn = QPushButton(self)
        self.expansion_img = QPixmapLabel(self)
        self.upgrade_cost_lbl = QLabel(self)
        self.maintenance_cost_lbl = QLabel(self)
        self.expansion_list = QListView(self)
        self.expansion_text = QPlainTextEdit(self)

        # create layout
        self.cost_form.addRow("Upgrade cost", self.upgrade_cost_lbl)
        self.cost_form.addRow("Maintenance cost", self.maintenance_cost_lbl)

        btnbox = QHBoxLayout()
        btnbox.addWidget(self.upgrade_btn)
        btnbox.addLayout(self.cost_form)

        leftbox = QVBoxLayout()
        leftbox.addLayout(btnbox)
        leftbox.addWidget(self.expansion_list)
        leftbox.addWidget(self.expansion_text)

        layout = QHBoxLayout(self)
        layout.addLayout(leftbox)
        layout.addWidget(self.expansion_img)

        # configure widgets
        self.retranslateUi()
        # TODO: load image

    def retranslateUi(self):
        tra = QApplication.translate
        ctxt = "ExpansionsTab"  # the translation context
        self.upgrade_btn.setText(tra(ctxt, "Upgrade"))
        cmn.translate_form(self.cost_form, ctxt,
                           ("Upgrade cost", "Maintenance cost")
                           )
        self.expansion_text.setPlainText(tra("SchoolManagement",
                                             "No description available"))


class PolicyTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # create widgets
        self.explanation_lbl = QLabel(self)
#        self.topic_lbl = QLabel(self)
#        self.rule_lbl = QLabel(self)
        self.policy_view = QColumnView(self)
        self.policy_text = QPlainTextEdit(self)

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
        self.policy_text.setPlainText(tra("SchoolManagement",
                                          "No description available"))


class AssignmentsTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.chbmap = {}  # maps checkbox ids to teacher, subject tuples
        # create widgets
        self.explanation_lbl = QLabel(self)
        # TODO maybe a simple grid layout would be better?
        teachers = world.teachers()
        subjects = world.subjects()
        self.table = QTableWidget(len(subjects),
                                  len(teachers),
                                  self)
        for r in range(len(subjects)):
            for c in range(len(teachers)):
                chb = QCheckBox(self.table)
                self.table.setCellWidget(r, c, chb)
                self.chbmap[chb] = (teachers[c], subjects[r])
        self.qualification_lbl = QLabel(self)
        self.qualification_list = cmn.QProgressList(
                translation_context="AssignmentsTab",
                parent=self
                )
        self.qualification_list.addBar("Subject experience")
        self.qualification_list.addBar("General qualification")

        # create layout
        subjectgrid = QGridLayout()
        subjectgrid.addWidget(self.qualification_lbl,     0, 0, 1, 2)
        layout = QVBoxLayout(self)
        layout.addWidget(self.explanation_lbl)
        layout.addWidget(self.table, 2)  # set stretch factor to 2
        layout.addLayout(subjectgrid)
        layout.addWidget(self.qualification_lbl)
        layout.addWidget(self.qualification_list)

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
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.table.setHorizontalHeaderLabels(teachers)
        self.table.setVerticalHeaderLabels(subjects)
        # TODO: icons

#        self.qualification_lbl.setPalette(style.white_text)
#        self.subjNameLbl.setPalette(style.white_text)
#        self.subjExpLbl.setPalette(style.white_text)
#        self.subjExpPB.setPalette(style.progress_bar)
#        self.subjExpPB.setValue(60)
#        self.subjExpPB.setTextVisible(False)
#        self.genQualfLbl.setPalette(style.white_text)
#        self.genQualfPB.setPalette(style.progress_bar)
#        self.genQualfPB.setValue(60)
#        self.genQualfPB.setTextVisible(False)

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
        self.qualification_lbl.setText(tra(ctxt, "Teaching experience"))
        self.qualification_list.retranslateUi()


class JobsTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create widgets
        self.applicants_lbl = QLabel(self)
        self.applicants_list = QListView(self)
        self.staff_lbl = QLabel(self)
        self.staff_list = QListView(self)
        self.hire_btn = QPushButton(self)
        self.income_lbl = QLabel(self)
        self.salary_lbl = QLabel(self)
        self.biography_lbl = QLabel(self)
        self.biography_text = QPlainTextEdit(self)
        self.subj_exp_lbl = QLabel(self)
        self.subj_exp_list = cmn.QProgressList(
                translation_context="school subject families", parent=self)
        for name in world.subjectFamilies():
            self.subj_exp_list.addBar(name)
        self.teacher_view = QGraphicsView(self)

        # create layout
        self.balanceform = QFormLayout()
        self.balanceform.addRow("Monthly Income:", self.income_lbl)
        self.balanceform.addRow("Staff Salary:", self.salary_lbl)

        layout = QGridLayout(self)
        layout.addWidget(self.applicants_lbl,   0, 0, 1, 1)
        layout.addWidget(self.applicants_list,  1, 0, 5, 1)
        layout.addLayout(self.balanceform,      1, 2)
        layout.addWidget(self.staff_lbl,        0, 4, 1, 1)
        layout.addWidget(self.staff_list,       1, 4, 5, 1)
        layout.addWidget(self.hire_btn,         3, 2, 1, 1)
        layout.addWidget(self.biography_lbl,    6, 0)
        layout.addWidget(self.biography_text,   7, 0, 1, 3)
        layout.addWidget(self.subj_exp_lbl,     8, 0)
        layout.addWidget(self.subj_exp_list,    9, 0, -1, 2)
        layout.addWidget(self.teacher_view,     6, 4, -1, -1)

        # configure widgets
        self.retranslateUi()

        # TODO: set background of tab to dark color
        self.biography_lbl.setPalette(style.white_text)
#        self.biography_text.setAlignment(Qt.AlignTop)
        self.subj_exp_lbl.setPalette(style.white_text)
#        for bar in self.subj_exp_bars:
#            bar.setPalette(style.progress_bar)
#            bar.setValue(60)
#            bar.setTextVisible(False)
        self.teacher_view.setStyleSheet("background: transparent")

    def retranslateUi(self):
        tra = QApplication.translate
        self.applicants_lbl.setText(tra("JobsTab", "Available Applicants"))
        self.staff_lbl.setText(tra("JobsTab", "Hired Staff"))
        self.hire_btn.setText(tra("JobsTab", "Hire"))
        self.biography_lbl.setText(tra("JobsTab", "Biography:"))
        self.biography_text.setPlainText(
                tra("JobsTab", "No biography available")
                )
        self.subj_exp_lbl.setText(
                tra("JobsTab", "Average Subject Family Experience")
                )
        cmn.translate_form(self.balanceform, "JobsTab",
                           ("Monthly Income:", "Staff Salary:"))
        self.subj_exp_list.retranslateUi()


class TimeTableDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        combo.setEditable(False)
        combo.addItems(world.subjects())
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
#                item.setData(world.subjects()[0], Qt.DisplayRole)
#                item.setData(world.subjects()[0], Qt.EditRole)
                item.setData("Double-click to edit", Qt.ToolTipRole)
                self.datamap[(row, col)] = item


class ClassesTab(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
#        self.daymap = OrderedDict()  # maps days to
        # create widgets
        self.active_class = QComboBox(self)
        self.tabs = QTabWidget(self)
        self.timetable = QTableView()
        self.grades_list = cmn.QProgressList(
                translation_context="school subjects")
        for name in world.subjects():
            self.grades_list.addBar(name)

        # create layout
        self.tabs.addTab(self.timetable, "Timetable")
        self.tabs.addTab(self.grades_list, "Summary")
        layout = QVBoxLayout(self)
        layout.addWidget(self.active_class)
        layout.addWidget(self.tabs)

        # configure widgets
        self.active_class.addItems(world.classes())
        self.tabs.setTabPosition(QTabWidget.West)
        self.timetable.setModel(TimeTableModel())
        self.timetable.setCornerButtonEnabled(False)
        self.timetable.setShowGrid(False)
        self.timetable.setSortingEnabled(False)

        # configure widgets
        self.retranslateUi()
        self.timetable.setItemDelegate(TimeTableDelegate())
#        delegate = self.timetable.itemDelegate()
#        delegate.setItemEditorFactory(TimeTableEditorFactory())
#        factory = delegate.itemEditorFactory()
#        if factory is None:
#            factory = QItemEditorFactory.defaultFactory()
#        factory.registerEditor()
#        delegate.setItemEditorFactory()

    def retranslateUi(self):
        tra = QApplication.translate
        ctxt = "ClassesTab"
        self.tabs.setTabText(0, tra(ctxt, "Timetable"))
        self.tabs.setTabText(1, tra(ctxt, "Summary"))
        self.grades_list.retranslateUi()


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
        self.grades_list = cmn.QProgressList(
                translation_context="school subjects", parent=self)
        for name in world.subjects():
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
        self.tabs = QTabWidget(self)
        self.students_tab = StudentsTab()
        self.classes_tab = ClassesTab()
        self.jobs_tab = JobsTab()
        self.assign_tab = AssignmentsTab()
        self.policy_tab = PolicyTab()
        self.expansions_tab = ExpansionsTab()
        self.clubs_tab = ClubsTab()
        self.accounting_tab = AccountingTab()
        self.stats_tab = StatsTab()
        self.exit_btn = QPushButton()

        # create layouts
        layout = QVBoxLayout(self)
        self.tabs.setContentsMargins(0, 0, 0, 0)
        # TODO: translate
        self.tabs.addTab(self.classes_tab, "Classes")
        self.tabs.addTab(self.students_tab, "Students")
        self.tabs.addTab(self.jobs_tab, "Jobs")
        self.tabs.addTab(self.assign_tab, "Teacher Assignments")
        self.tabs.addTab(self.policy_tab, "School Policy")
        self.tabs.addTab(self.expansions_tab, "Expansions")
        self.tabs.addTab(self.clubs_tab, "Clubs")
        self.tabs.addTab(self.accounting_tab, "Accounting")
        self.tabs.addTab(self.stats_tab, "Stats")
        layout.addWidget(self.tabs)
        layout.addWidget(self.exit_btn)

        fixedsize = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.exit_btn.setSizePolicy(fixedsize)

        # configure widgets
        self.tabs.setStyleSheet(
                "QTabWidget { background-color: rgb(25, 45, 52);}")

        # connect signals
        self.exit_btn.clicked.connect(self.parent().toggle_school_management)

        # TODO: check if top part of tab handle reacts to interaction

        self.retranslateUi()

    def retranslateUi(self):
        tra = QApplication.translate
        ctxt = "SchoolManagement"
        self.exit_btn.setText(tra(ctxt, "Exit"))
        for idx, name in enumerate((
                "Classes", "Students", "Jobs", "Teacher Assignments",
                "School Policy", "Expansions", "Clubs", "Accounting",
                "Stats")):
            self.tabs.setTabText(idx, tra(ctxt, name))


# --------------------------------------------------------------------------- #
# Define module globals
# --------------------------------------------------------------------------- #
world = cmn.world
# TODO: fetch data from scenario
#balance = ["Monthly Loan:", "Staff Salary:"]
#balanceExample = ["-$16,188", "$2,811"]
#clubInfo = ["Members:", "time:", "Club President:", "Location:",
#            "Weekly Balance:"]
#clubInfoExample = ["12", "16:00-18:00", "Anette", "Sports Area", "-$50"]
