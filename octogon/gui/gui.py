from PyQt5.QtWidgets import QLabel, QLineEdit, QComboBox, QCheckBox

from octogon.utils.logger import get_print_fn

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
        wins = 0
        for btn in self.btns:
            if btn.isChecked():
                wins += 1

        self.scoreboard[self.key] = wins
