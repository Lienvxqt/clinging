import sys, random, json, keyboard
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

def save_settings(settings):
    with open(Settings, "w") as f:
        json.dump(settings, f)

def load_settings():
    Base_Font_Settings = {"font_type": "Arial", "font_size": 14}
    try:
        with open("Settings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        with open("Settings.json", "w") as f:
            json.dump(Base_Font_Settings, f)
            return Base_Font_Settings

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Цепляясь")
        self.setGeometry(0, 0, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.vbox = QVBoxLayout(self.central_widget)
        self.gui_main_window()

        self.in_game = False
        self.all_lines = []
        self.current_line_pos = 0
        self.inventory = []
        self.Text_Window = None
        self.question = False

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
        self.in_game = False
        self.Text_Window = None
        while self.vbox.count():
            item = self.vbox.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                layout = item.layout()
                if layout is not None:
                    self.clear_layout(layout)
    
    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                sublayout = item.layout()
                if sublayout is not None:
                    self.clear_layout(sublayout)

    def ui_Start(self):
        self.clear_window()
        label = QLabel("Выберите начальный предмет")
        Item_Pick_List = QComboBox()
        Item_Pick_List.setPlaceholderText("Выбери начальный предмет")
        Item_Pick_List.addItems(["Ничего", "Броня", "Оружие", "Хлеб"])
        Item_Pick_Button = QPushButton("Выбрать предмет")
        current_item_index = Item_Pick_List.currentIndex()
        current_item = "Ничего"
        self.inventory = []
        def start():
                self.inventory.append(Item_Pick_List.itemText(Item_Pick_List.currentIndex()))
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
        FontTypeLabel = QLabel(f"Шрифт")
        FontTypeSetting = QFontComboBox()
        FontSizeLabel = QLabel(f"Размер шрифта")
        FontSizeSetting = QSpinBox()
        with open("Settings.json", "r") as f:
            BaseFontSize = json.load(f)
            BaseFontSize = BaseFontSize['font_size']
        FontSizeSetting.setValue(BaseFontSize)
        Save_Font_Settings_Button = QPushButton("Сохранить настройки")
        Settings_Caution = QLabel("*После сохранения настроек для их применения требуется перезапустить игру")
        FontTypeSetting.setFontFilters(QFontComboBox.FontFilter.ProportionalFonts)
        ToMain_Button.clicked.connect(self.gui_main_window)
        FontTypeSetting.currentFontChanged.connect(lambda font: print(f"Выбран шрифт: {font.family()}"))
        def save_settings_button():
            a=FontTypeSetting.currentFont().family()
            b=FontSizeSetting.value()
            settings = {"font_type": a, "font_size": b}
            with open("Settings.json", "w") as f:
                json.dump(settings, f)
            print(settings)
        Save_Font_Settings_Button.clicked.connect(save_settings_button)
        self.vbox.addWidget(FontTypeLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(FontTypeSetting, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(FontSizeLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(FontSizeSetting, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(Save_Font_Settings_Button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(ToMain_Button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.vbox.addWidget(Settings_Caution, alignment=Qt.AlignmentFlag.AlignCenter)

    def Exit_Button_event(self):
        self.close()

    def ui_Game(self):
        self.clear_window()
        hbox = QHBoxLayout()
        Inventory_Button = QPushButton()
        Map_Button = QPushButton()
        self.Text_Window = QTextEdit()
        self.Text_Window.setReadOnly(True)
        Inventory_Button.setIcon(QIcon('resources/Backpack_Icon.png'))
        Map_Button.setIcon(QIcon('resources/Map_Icon.png'))
        Inventory_Button.setMinimumSize(150, 150)
        Inventory_Button.setIconSize(QSize(150, 150))
        Map_Button.setMinimumSize(150, 150)
        Map_Button.setIconSize(QSize(150, 150))
        hbox.addWidget(Inventory_Button, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft)
        hbox.addWidget(self.Text_Window, alignment=Qt.AlignmentFlag.AlignBottom)
        hbox.addWidget(Map_Button, alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight)
        with open("resources/main_text.txt", "r", encoding="UTF-8") as f:
            self.all_lines = f.readlines()
        self.current_line_pos = 0
        self.current_line = self.all_lines[self.current_line_pos]
        #if "<Q>" in self.current_line[0]:
        #    self.Text_Window.setText(self.current_line)
        #    self.question == True
        #else:
        #    self.Text_Window.setText(self.current_line)
        self.Text_Window.setText(self.current_line)
        self.vbox.addLayout(hbox)
        self.in_game = True 
        self.setFocus()
         
    def next_line(self):
        if (self.question == False) and (self.current_line_pos < len(self.all_lines) - 1):
            self.current_line_pos += 1
            self.Text_Window.setText(self.all_lines[self.current_line_pos])
        else:
            self.Text_Window.setText("Конец")
            self.in_game = False

    def keyPressEvent(self, event):
        if self.in_game and self.Text_Window is not None and event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter, Qt.Key.Key_Space):
            self.next_line()
        else:
            super().keyPressEvent(event) 
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Settings = load_settings()
    app.setFont(QFont(Settings['font_type'], Settings['font_size']))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())