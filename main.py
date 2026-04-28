import sys, random, json
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Цепляясь")
        self.setGeometry(0, 0, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.vbox = QVBoxLayout(self.central_widget)
        self.gui_main_window()

    def gui_main_window(self): 
        self.clear_window()
        label = QLabel("Цепляясь", self)
        Start_Menu_Button = QPushButton("Начать новую игру", self)
        Start_Menu_Button.clicked.connect(self.ui_Start)
        Load_Menu_Button = QPushButton("Загрузить", self)
        Load_Menu_Button.clicked.connect(self.ui_Load)
        Settings_Menu_Button = QPushButton("Настройки", self)
        Settings_Menu_Button.clicked.connect(self.ui_Settings) 
        Exit_Button = QPushButton("Выйти", self)
        Exit_Button.clicked.connect(self.Exit_Button_event)
        self.vbox.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(Start_Menu_Button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(Load_Menu_Button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(Settings_Menu_Button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(Exit_Button, alignment=Qt.AlignmentFlag.AlignCenter)

    def clear_window(self):
        while self.vbox.count():
            item = self.vbox.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def ui_Start(self):
        self.clear_window()
        label = QLabel("Выберите начальный предмет")
        Item_Pick_List = QComboBox()
        Item_Pick_List.setPlaceholderText("Выбери начальный предмет")
        Item_Pick_List.addItems(["Ничего", "Броня", "Оружие", "Хлеб"])
        Item_Pick_Button = QPushButton("Выбрать предмет")
        current_item_index = Item_Pick_List.currentIndex()
        current_item = "Ничего"
        inventory = []
        def start():
                inventory.append(Item_Pick_List.itemText(Item_Pick_List.currentIndex()))
                self.ui_Game()
        Item_Pick_Button.clicked.connect(start)
        ToMain_Button = QPushButton("Назад")
        ToMain_Button.clicked.connect(self.gui_main_window)
        self.vbox.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(Item_Pick_List, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(Item_Pick_Button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(ToMain_Button, alignment=Qt.AlignmentFlag.AlignCenter)

    def ui_Load(self):
        self.clear_window()
        label = QLabel("Выберите сохранение (В разработке)")
        ToMain_Button = QPushButton("Назад")
        ToMain_Button.clicked.connect(self.gui_main_window)
        self.vbox.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(ToMain_Button, alignment=Qt.AlignmentFlag.AlignCenter)

    def ui_Settings(self):
        self.clear_window()
        ToMain_Button = QPushButton("Назад")
        FontTypeSetting = QFontComboBox()
        ToMain_Button.clicked.connect(self.gui_main_window)
        FontTypeSetting.currentFontChanged.connect(lambda : print(">>"))
        self.vbox.addWidget(FontTypeSetting, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(ToMain_Button, alignment=Qt.AlignmentFlag.AlignCenter)

    def Exit_Button_event(self):
        self.close()

    def ui_Game(self):
        self.clear_window()
        hbox = QHBoxLayout()
        Inventory_Button = QPushButton()
        Map_Button = QPushButton()
        Inventory_Button.setIcon(QIcon('resources/Backpack_Icon.png'))
        Map_Button.setIcon(QIcon('resources/Map_Icon.png'))
        Inventory_Button.setMinimumSize(150, 150)
        Inventory_Button.setIconSize(QSize(150, 150))
        Map_Button.setMinimumSize(150, 150)
        Map_Button.setIconSize(QSize(150, 150))
        hbox.addWidget(Inventory_Button, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        hbox.addWidget(Map_Button, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        self.vbox.addLayout(hbox)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    with open("Settings.json", "r") as f:
        Settings = json.load(f)
    app.setFont(QFont(Settings['font_type'], Settings['font_size']))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())