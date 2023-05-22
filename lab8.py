import psycopg2
import sys

from PyQt5.QtWidgets import (QApplication, QWidget,
                             QTabWidget, QAbstractScrollArea,
                             QVBoxLayout, QHBoxLayout,
                             QTableWidget, QGroupBox,
                             QTableWidgetItem, QPushButton, QMessageBox)
from PyQt5 import QtCore


class MainWindow(QWidget):
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads, True)

    def __init__(self):

        super(MainWindow, self).__init__()

        self._mutex = QtCore.QMutex()

        self._connect_to_db()

        self.setWindowTitle("Timetable")
        self.setWindowTitle("Subjects")
        self.setWindowTitle("Teachers")

        self.vbox = QVBoxLayout(self)

        self.tabs = QTabWidget(self)
        self.vbox.addWidget(self.tabs)

        self._create_shedule_tab()
        self._create_subjects_tab()
        self._create_teachers_tab()

    def _connect_to_db(self):
        self.conn = psycopg2.connect(database="timetable_mtuci",
                                     user="postgres",
                                     password="Awe6ve2056E",
                                     host="localhost",
                                     port="5432")

        self.cursor = self.conn.cursor()

    def _create_teachers_tab(self):
        self.teachers_tab = QWidget()
        self.tabs.addTab(self.teachers_tab, "Teachers")

        self.teachers_gbox = QGroupBox("Teachers")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.teachers_gbox)

        self._get_teachers()
        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_teachers)

        self.teachers_tab.setLayout(self.svbox)

        self.teachers_tab.setLayout(self.svbox)

    def _create_subjects_tab(self):
        self.subjects_tab = QWidget()
        self.tabs.addTab(self.subjects_tab, "Subjects")

        self.subjects_gbox = QGroupBox("Subjects")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.subjects_gbox)

        self._get_subjects()
        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_subject_table)

        self.subjects_tab.setLayout(self.svbox)

        self.subjects_tab.setLayout(self.svbox)

    def _create_shedule_tab(self):
        self.shedule_tab = QTabWidget()
        self.tabs.addTab(self.shedule_tab, "Timetable")



        self.monday_gbox = QGroupBox("Monday")
        self.tuesday_gbox = QGroupBox("Tuesday")
        self.wednesday_gbox = QGroupBox("Wednesday")

        self.svbox = QVBoxLayout()
        self.shbox1 = QHBoxLayout()
        self.shbox2 = QHBoxLayout()

        self.svbox.addLayout(self.shbox1)
        self.svbox.addLayout(self.shbox2)

        self.shbox1.addWidget(self.monday_gbox)
        self.shbox1.addWidget(self.tuesday_gbox)
        self.shbox1.addWidget(self.wednesday_gbox)

        self._create_monday_table()
        self._create_tuesday_table()
        self._create_wednesday_table()

        self.update_shedule_button = QPushButton("Update")
        self.shbox2.addWidget(self.update_shedule_button)
        self.update_shedule_button.clicked.connect(self._update_shedule)

        self.shedule_tab.setLayout(self.svbox)

    def _create_monday_table(self):
        self.monday_table = QTableWidget()
        self.monday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.monday_table.setColumnCount(6)
        self.monday_table.setHorizontalHeaderLabels(["Subject", "Auditory", "Teacher", "Time", "", ""])

        self._update_monday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.monday_table)
        self.monday_gbox.setLayout(self.mvbox)

    def _get_teachers(self):
        self.teachers_table = QTableWidget()
        self.teachers_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.teachers_table.setColumnCount(4)
        self.teachers_table.setHorizontalHeaderLabels(["ID", "NAME", "", ""])

        self._update_teachers()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.teachers_table)
        self.teachers_gbox.setLayout(self.mvbox)

    def _get_subjects(self):
        self.subjects_table = QTableWidget()
        self.subjects_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.subjects_table.setColumnCount(4)
        self.subjects_table.setHorizontalHeaderLabels(["ID", "NAME", "", ""])

        self._update_subject_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.subjects_table)
        self.subjects_gbox.setLayout(self.mvbox)

    def _create_tuesday_table(self):
        self.tuesday_table = QTableWidget()
        self.tuesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.tuesday_table.setColumnCount(5)
        self.tuesday_table.setHorizontalHeaderLabels(["Subject", "Auditory", "Teacher", "Time", ""])

        self._update_tuesday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.tuesday_table)
        self.tuesday_gbox.setLayout(self.mvbox)

    def _create_wednesday_table(self):
        self.wednesday_table = QTableWidget()
        self.wednesday_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        self.wednesday_table.setColumnCount(5)
        self.wednesday_table.setHorizontalHeaderLabels(["Subject", "Auditory", "Teacher", "Time", ""])

        self._update_wednesday_table()

        self.mvbox = QVBoxLayout()
        self.mvbox.addWidget(self.wednesday_table)
        self.wednesday_gbox.setLayout(self.mvbox)

    def _update_teachers(self):
        self.cursor.execute("SELECT * FROM teacher ORDER BY id")
        teachers = list(self.cursor.fetchall())

        self.teachers_table.setRowCount(len(teachers) + 1)

        for i, r in enumerate(teachers):
            r = list(r)
            joinButton = QPushButton("Join")
            delButton = QPushButton("Delete")

            self.teachers_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))

            self.teachers_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[1])))

            self.teachers_table.setCellWidget(i, 2, joinButton)

            self.teachers_table.setCellWidget(i, 3, delButton)

            joinButton.clicked.connect(lambda ch, num=i: self._change_teacher(num))
            delButton.clicked.connect(lambda ch, num=i: self._del_teacher(num))

        self.teachers_table.resizeRowsToContents()

    def _update_subject_table(self):
        self.cursor.execute("SELECT * FROM subject ORDER BY id")
        subjects = list(self.cursor.fetchall())

        self.subjects_table.setRowCount(len(subjects) + 1)

        for i, r in enumerate(subjects):
            r = list(r)
            joinButton = QPushButton("Join")
            delButton = QPushButton("Delete")

            self.subjects_table.setItem(i, 0,
                                        QTableWidgetItem(str(r[0])))

            self.subjects_table.setItem(i, 1,
                                        QTableWidgetItem(str(r[1])))

            self.subjects_table.setCellWidget(i, 2, joinButton)

            self.subjects_table.setCellWidget(i, 3, delButton)

            joinButton.clicked.connect(lambda ch, num=i: self.change_subject(num))
            delButton.clicked.connect(lambda ch, num=i: self._del_subject(num))

        self.subjects_table.resizeRowsToContents()

    def _update_monday_table(self):
        self.cursor.execute("SELECT * FROM choose_day('monday1')")
        records = list(self.cursor.fetchall())

        self.monday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            delButton = QPushButton("Delete")

            self.monday_table.setItem(i, 0,
                                      QTableWidgetItem(str(r[0])))
            self.monday_table.setItem(i, 1,
                                      QTableWidgetItem(str(r[1])))
            self.monday_table.setItem(i, 2,
                                      QTableWidgetItem(str(r[2])))
            self.monday_table.setItem(i, 3,
                                      QTableWidgetItem(str(r[3])))

            self.monday_table.setCellWidget(i, 4, joinButton)

            self.monday_table.setCellWidget(i, 5, delButton)

            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num, records))
            delButton.clicked.connect(lambda ch, num=i: self._del_lesson(num, records))

        self.monday_table.resizeRowsToContents()

    def _del_lesson(self, rowNum, records):
        row = list()
        day: int
        for i in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(rowNum, i).text())
            except:
                row.append(None)
        for record in records:
            if row[3] == record[3]:
                day = record[4]
                break
        self.cursor.execute("CALL update_day(%s, %s, %s)", (10, '', day))

    def _del_teacher(self, rowNum):
        row = list()
        for i in range(self.teachers_table.columnCount()):
            try:
                row.append(self.teachers_table.item(rowNum, i).text())
            except:
                row.append(None)
        print(row)
        self.cursor.execute("DELETE FROM teacher WHERE id=%s", (row[0],))
        self.conn.commit()

    def _del_subject(self, rowNum):
        row = list()
        for i in range(self.subjects_table.columnCount()):
            try:
                row.append(self.subjects_table.item(rowNum, i).text())
            except:
                row.append(None)
        print(row)
        self.cursor.execute("DELETE FROM subject WHERE id=%s", (row[0],))
        self.conn.commit()

    def _update_tuesday_table(self):
        self.cursor.execute("SELECT * FROM choose_day('tuesday1')")
        records = list(self.cursor.fetchall())

        self.tuesday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            # delButton = QPushButton("Delete")

            self.tuesday_table.setItem(i, 0,
                                       QTableWidgetItem(str(r[0])))
            self.tuesday_table.setItem(i, 1,
                                       QTableWidgetItem(str(r[1])))
            self.tuesday_table.setItem(i, 2,
                                       QTableWidgetItem(str(r[2])))
            self.tuesday_table.setItem(i, 3,
                                       QTableWidgetItem(str(r[3])))

            self.tuesday_table.setCellWidget(i, 4, joinButton)

            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num, records))

        self.tuesday_table.resizeRowsToContents()

    def _update_wednesday_table(self):
        self.cursor.execute("SELECT * FROM choose_day('wednesday1')")
        records = list(self.cursor.fetchall())

        self.wednesday_table.setRowCount(len(records) + 1)

        for i, r in enumerate(records):
            r = list(r)
            joinButton = QPushButton("Join")
            # delButton = QPushButton("Delete")

            self.wednesday_table.setItem(i, 0,
                                         QTableWidgetItem(str(r[0])))
            self.wednesday_table.setItem(i, 1,
                                         QTableWidgetItem(str(r[1])))
            self.wednesday_table.setItem(i, 2,
                                         QTableWidgetItem(str(r[2])))
            self.wednesday_table.setItem(i, 3,
                                         QTableWidgetItem(str(r[3])))

            self.wednesday_table.setCellWidget(i, 4, joinButton)

            joinButton.clicked.connect(lambda ch, num=i: self._change_day_from_table(num, records))

        self.wednesday_table.resizeRowsToContents()

    def _change_teacher(self, rowNum):
        row = list()
        for i in range(self.teachers_table.columnCount()):
            try:
                row.append(self.teachers_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("CALL update_teacher(%s, %s)", (row[0], row[1]))
            self.conn.commit()
            QMessageBox.about(self, "Success", "Fields are transformed")
        except:
            self.conn.commit()
            QMessageBox.about(self, "Error", "Enter all fields")

    def change_subject(self, rowNum):
        row = list()
        for i in range(self.subjects_table.columnCount()):
            try:
                row.append(self.subjects_table.item(rowNum, i).text())
            except:
                row.append(None)
        try:
            self.cursor.execute("CALL update_subject(%s, %s)", (row[0], row[1]))
            self.conn.commit()
            QMessageBox.about(self, "Success", "Fields are transformed")
        except:
            self.conn.commit()
            QMessageBox.about(self, "Error", "Enter all fields")

    def _change_day_from_table(self, rowNum, records):
        row = list()
        day: int
        for i in range(self.monday_table.columnCount()):
            try:
                row.append(self.monday_table.item(rowNum, i).text())
            except:
                row.append(None)
        for record in records:

            if row[3] == record[3]:
                day = record[4]
                break
        sub_id: int
        self.cursor.execute("SELECT * FROM subject")
        check = list(self.cursor.fetchall())
        subject = []
        for _, sub in check:
            subject.append(sub)  # заполнение списка с предметами
        if row[0] not in subject:
            QMessageBox.about(self, "ERROR", "Нет такого предмета")
            return
        elif row[0] in subject:  # проверка на наличие предмета
            for num, sub in check:  # сравнение предмета с его id
                if sub == row[0]:
                    sub_id = num
                    break
        try:
            self.cursor.execute("CALL update_day(%s, %s, %s)", (sub_id, row[1], day))
            self.conn.commit()
            QMessageBox.about(self, "Success", "Fields are transformed")
        except:
            self.conn.commit()
            QMessageBox.about(self, "Error", "Enter all fields")

    def _update_shedule(self):
        self._update_monday_table()
        self._update_tuesday_table()
        self._update_wednesday_table()
        self._update_subject_table()
        self._update_teachers()


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
