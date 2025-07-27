from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QLabel, QWidget, QApplication, QPushButton, QComboBox, QMainWindow, QGridLayout, \
    QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QVBoxLayout, QToolBar, QTextEdit
import sqlite3
import sys



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management App")
        self.setGeometry(500, 500, 550, 400)

        menu_bar = self.menuBar().addMenu("&Help")
        file_bar = self.menuBar().addMenu("&File")

        student_action = QAction("Add Student", self)
        student_action.triggered.connect(self.insert)
        self.search = QAction("Search", self)
        file_bar.addAction(self.search)
        file_bar.addAction(student_action)

        about_action = QAction("About", self)
        menu_bar.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Student ID", "Student Name", "Course", "Phone Number"))
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def insert(self):
        dialog = InsertDialog()
        dialog.setWindowTitle("Add Student")
        dialog.setGeometry(300, 300, 500, 200)
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
        add.clicked.connect(self.add_student)

        # Displaying Widgets
        layout.addWidget(self.student_name, 0, 0)
        layout.addWidget(self.student_number, 0, 1)
        layout.addWidget(self.courses, 0, 2)
        layout.addWidget(add, 1, 0, 1, 2)
        self.setLayout(layout)


    def add_student(self):
        name = self.student_name.text()
        course = self.courses.itemText(self.courses.currentIndex())
        mobile = self.student_number.text()
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
            (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        window.load_data()




app = QApplication(sys.argv)
window = MainWindow()
window.load_data()
window.show()
sys.exit(app.exec())