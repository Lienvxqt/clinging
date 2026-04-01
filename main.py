import sys, random, time
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Цепляясь")
        self.setGeometry(300, 300, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.vbox = QVBoxLayout(self.central_widget)
        
        self.gui_main_window()
    
    def gui_main_window(self): 

        self.clear_window()

        label = QLabel("Цепляясь", self)
        
        Start_Button = QPushButton("Начать новую игру", self)
        Start_Button.clicked.connect(self.start_eve)

        Load_Button = QPushButton("Загрузить", self)
        Load_Button.clicked.connect(self.load_eve)

        Settings_Button = QPushButton("Настройки", self)
        Settings_Button.clicked.connect(self.gui_screen_Settings) 

        Exit_Button = QPushButton("Выйти", self)
        Exit_Button.clicked.connect(self.Exit_Button_eve)
        
        self.vbox.addWidget(Start_Button)
        self.vbox.addWidget(Load_Button)
        self.vbox.addWidget(Settings_Button)
        self.vbox.addWidget(Exit_Button)

    def clear_window(self):
        while self.vbox.count():
            item = self.vbox.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def gui_screen_Settings(self):
        self.clear_window()
        ToMain_Button = QPushButton("Назад")
        ToMain_Button.clicked.connect(self.gui_main_window)
        self.vbox.addWidget(ToMain_Button)
        
    def start_eve(self):
        pass

    def load_eve(self):
        self.close()
    
    def Settings(self):
        pass

    def Exit_Button_eve(self):
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
