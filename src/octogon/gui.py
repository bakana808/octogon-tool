from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QCheckBox

from data import scoreboard
from octogon.config import get_print_fn

print = get_print_fn("qt")


class SBWidgetPair:
    def __init__(self, parent, name: str, key: str):

        self.key = key
        self.label = QLabel(name, parent)

    def on_edited(self):
        pass


class SBTextWidget(SBWidgetPair):
    def __init__(self, parent, name: str, key: str):
        super().__init__(parent, name, key)

        self.edit = QLineEdit(parent)
        self.edit.setText(scoreboard[key])
        self.edit.textChanged.connect(self.on_edited)

    def on_edited(self):
        print("updating sb data")
        scoreboard[self.key] = self.edit.text()


class SBDropdownWidget(SBWidgetPair):
    def __init__(self, parent, name: str, key: str):
        super().__init__(parent, name, key)

        self.edit = QComboBox(parent)
        self.edit.currentIndexChanged.connect(self.on_edited)

    def on_edited(self):
        print("updating sb data")
        scoreboard[self.key] = self.edit.currentText()


class SBWinsWidget(SBWidgetPair):
    def __init__(self, parent, name: str, key: str):
        super().__init__(parent, name, key)

        self.btns = [
            QCheckBox(""),
            QCheckBox(""),
            QCheckBox(""),
        ]
        for btn in self.btns:
            btn.toggled.connect(self.on_edited)

    def on_edited(self):
        print("updating sb data")
        wins = 0
        for btn in self.btns:
            if btn.isChecked():
                wins += 1

        scoreboard[self.key] = wins
