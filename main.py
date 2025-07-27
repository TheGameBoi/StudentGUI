from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QLabel, QWidget, QApplication, QPushButton, QComboBox, QMainWindow, QGridLayout
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






app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())