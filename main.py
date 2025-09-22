from idlelib.help_about import AboutDialog
from PyQt6.QtWidgets import QLabel, QWidget, QApplication, QPushButton, QComboBox, QMainWindow, QGridLayout, \
    QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QVBoxLayout, QToolBar, QTextEdit, QStatusBar
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import sqlite3
import sys



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management App")
        self.setMinimumSize(500, 400)
        student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        student_action.triggered.connect(self.insertdialog)
        search_bar = QAction(QIcon("icons/search.png"), "Search", self)
        search_bar.triggered.connect(self.search)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.about)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Student ID", "Student Name", "Course", "Phone Number"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Create a Toolbar
        toolbar = QToolBar(self)
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(student_action)
        toolbar.addAction(search_bar)
        toolbar.addAction(about_action)

        # Create a Statusbar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Detect Cell Click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        children = self.findChildren(QPushButton)
        if children:
            for adult in children:
                self.status.removeWidget(adult)

        self.status.addWidget(delete_button)
        self.status.addWidget(edit_button)


    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insertdialog(self):
        dialog = InsertDialog()
        dialog.setWindowTitle("Add Student")
        dialog.setGeometry(300, 300, 500, 200)
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog("Student Management App")

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(400)
        self.setFixedHeight(100)

        #Grid Layout
        layout = QGridLayout()
        # Input Fields
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student Name")

        self.student_number = QLineEdit()
        self.student_number.setPlaceholderText("Student Number")

        self.courses = QComboBox()
        classes = ["Math", "Science", "History", "Engineering"]
        self.courses.addItems(classes)


        # Submit Button
        add = QPushButton("Add Student")
        add.clicked.connect(self.update)

        # Displaying Widgets
        layout.addWidget(self.student_name, 0, 0)
        layout.addWidget(self.student_number, 0, 1)
        layout.addWidget(self.courses, 0, 2)
        layout.addWidget(add, 1, 0, 1, 2)
        self.setLayout(layout)


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Students")
        self.setFixedWidth(400)
        self.setFixedHeight(100)

        # Grid Layout
        layout = QGridLayout()

        # Search Bar
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Student Name")

        self.submit = QPushButton("Search")
        self.submit.clicked.connect(self.search)

        # Display Search
        layout.addWidget(self.student_name, 0, 0)
        layout.addWidget(self.submit, 0, 1)

        self.setLayout(layout)


    def search(self):
        name = self.student_name.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        rows = list(result)
        print(rows)
        items = window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            window.table.item(item.row(), 1).setSelected(True)

        cursor.close()
        connection.close()


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(400)
        self.setFixedHeight(100)

        # Grid Layout
        layout = QGridLayout()

        # Index Value
        index = window.table.currentRow()

        # Get Student ID
        self.student_id = window.table.item(index, 0).text()

        # Get Student Name
        name = window.table.item(index, 1).text()

        # Student Name
        self.student_name = QLineEdit(name)
        self.student_name.setPlaceholderText("Name")

        # Get Courses
        courses = window.table.item(index, 2).text()

        # Student Course
        self.courses = QComboBox()
        classes = ["Math", "Science", "History", "Engineering", "Biology", "Astronomy"]
        self.courses.addItems(classes)
        self.courses.setCurrentText(courses)

        # Get Student Number
        number = window.table.item(index, 3).text()

        # Student Number
        self.student_number = QLineEdit(number)
        self.student_number.setPlaceholderText("Student Number")

        # Submit Button
        add = QPushButton("Update Information")
        add.clicked.connect(self.update_student)

        # Displaying Widgets
        layout.addWidget(self.student_name, 0, 0)
        layout.addWidget(self.student_number, 0, 1)
        layout.addWidget(add, 1, 0, 1, 2)
        layout.addWidget(self.courses, 0, 2)
        self.setLayout(layout)


    def update_student(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?", (
                self.student_name.text(),
                self.courses.itemText(self.courses.currentIndex()),
                self.student_number.text(),
                self.student_id))
        connection.commit()
        cursor.close()
        connection.close()
        window.load_data()


class DeleteDialog(QDialog):
    pass

app = QApplication(sys.argv)
window = MainWindow()
window.load_data()
window.show()
sys.exit(app.exec())