from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QCheckBox

from octogon.utils.logger import get_print_fn
from octogon.utils.lookup import characters
from octogon.utils import list_file_basenames

print = get_print_fn("qt")


class SBWidgetPair:
    def __init__(self, parent, name: str, key: str):

        self.key = key
        self.label = QLabel(name, parent)
        self.scoreboard = parent.octogon.scoreboard

    def on_edited(self):
        pass


class SBTextWidget(SBWidgetPair):
    def __init__(self, parent, name: str, key: str):
        super().__init__(parent, name, key)

        self.edit = QLineEdit(parent)
        self.edit.setText(self.scoreboard[key])
        self.edit.textChanged.connect(self.on_edited)

    def on_edited(self):
        self.scoreboard[self.key] = self.edit.text()


class SBDropdownWidget(SBWidgetPair):
    def __init__(self, parent, name: str, key: str, items: list):
        super().__init__(parent, name, key)

        self.edit = QComboBox(parent)
        self.edit.addItems(items)
        self.edit.setCurrentText(self.scoreboard[self.key])
        self.edit.currentIndexChanged.connect(self.on_edited)

    def on_edited(self):
        self.scoreboard[self.key] = self.edit.currentText()


class SBCharacterWidget:
    def __init__(self, window, char_key: str, color_key: str):

        self.char_key = char_key
        self.color_key = color_key
        self.scoreboard = window.octogon.scoreboard

        self.label = QLabel("Character")
        self.cb_char = QComboBox(window)
        self.cb_color = QComboBox(window)

        char_names = list(characters.values())
        self.cb_char.addItems(char_names)

        self.cb_char.setCurrentText(self.scoreboard[self.char_key])
        self.update_colors()
        self.cb_char.setCurrentText(self.scoreboard[self.color_key])

        self.cb_char.currentIndexChanged.connect(self.on_character_changed)
        self.cb_color.currentIndexChanged.connect(self.on_color_changed)

    def update_colors(self):
        """
        Update the items in the colors combo box according
        to the selected character.
        """
        print("updating colors")

        char = self.cb_char.currentText()

        colors = list_file_basenames("assets/portraits/%s" % char)
        self.cb_color.clear()
        self.cb_color.addItems(colors)

    def on_character_changed(self):
        self.scoreboard[self.char_key] = self.cb_char.currentText()
        self.update_colors()

    def on_color_changed(self):
        self.scoreboard[self.color_key] = self.cb_color.currentText()


class SBWinsWidget(SBWidgetPair):
    def __init__(self, parent, name: str, key: str):
        super().__init__(parent, name, key)

        self.btns = [
            QCheckBox(""),
            QCheckBox(""),
            QCheckBox(""),
        ]

        if self.scoreboard[self.key] >= 1:
            self.btns[0].setChecked(True)
        if self.scoreboard[self.key] >= 2:
            self.btns[1].setChecked(True)
        if self.scoreboard[self.key] >= 3:
            self.btns[2].setChecked(True)

        for btn in self.btns:
            btn.toggled.connect(self.on_edited)

    def on_edited(self):
        wins = 0
        for btn in self.btns:
            if btn.isChecked():
                wins += 1

        self.scoreboard[self.key] = wins


class SBPortWidget:
    """Set the port number of a player."""

    def __init__(self, parent, key: str, port: int):

        self.key = key
        self.scoreboard = parent.octogon.scoreboard

        self.btns = [
            QCheckBox(""),
            QCheckBox(""),
            QCheckBox(""),
            QCheckBox(""),
        ]

        self.btns[0].setObjectName("port1")
        self.btns[0].toggled.connect(self.on_port_1)
        self.btns[1].setObjectName("port2")
        self.btns[1].toggled.connect(self.on_port_2)
        self.btns[2].setObjectName("port3")
        self.btns[2].toggled.connect(self.on_port_3)
        self.btns[3].setObjectName("port4")
        self.btns[3].toggled.connect(self.on_port_4)

        self.current_port = 0
        self.set_port(port)

    def on_port_1(self):
        self.set_port(0, self.btns[0].isChecked())

    def on_port_2(self):
        self.set_port(1, self.btns[1].isChecked())

    def on_port_3(self):
        self.set_port(2, self.btns[2].isChecked())

    def on_port_4(self):
        self.set_port(3, self.btns[3].isChecked())

    def set_port(self, n: int, state: bool = True):
        """Set the controller port."""
        for i, btn in enumerate(self.btns):
            btn.blockSignals(True)
            if i != n:
                btn.setChecked(False)
            else:
                btn.setChecked(True)
            btn.blockSignals(False)

        self.current_port = n
        self.scoreboard[self.key] = self.current_port
