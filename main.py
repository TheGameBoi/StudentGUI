from PyQt6.QtWidgets import QLabel, QWidget, QApplication, QPushButton, QComboBox, QMainWindow, QGridLayout
import sys



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management App")

        menu_bar = self.menuBar().addMenu("&File")
        file_bar = self.menuBar().addMenu("&Help")





app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())