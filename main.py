from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QLabel, QWidget, QApplication, QPushButton, QComboBox, QMainWindow, QGridLayout, \
    QTableWidget, QTableWidgetItem
import sqlite3
import sys



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management App")

        menu_bar = self.menuBar().addMenu("&Help")
        file_bar = self.menuBar().addMenu("&File")

        student_action = QAction("Add Student", self)
        file_bar.addAction(student_action)

        about_action = QAction("About", self)
        menu_bar.addAction(about_action)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Student Name", "Student ID", "Course", "Phone Number"))
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





app = QApplication(sys.argv)
window = MainWindow()
window.load_data()
window.show()
sys.exit(app.exec())