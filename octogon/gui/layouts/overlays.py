from PyQt5.QtWidgets import QGridLayout, QLineEdit, QPushButton
from PyQt5.QtCore import QMargins
from threading import Timer

import typing
from octogon.gui.gui import SBCharacterWidget

if typing.TYPE_CHECKING:
    from octogon.gui.window import OctogonWindow


class OverlaysLayout(QGridLayout):
    """The QT layout that displays a list of overlays to copy."""

    def __init__(self, window: "OctogonWindow"):
        super().__init__()

        self.setContentsMargins(QMargins(20, 20, 20, 20))
        self.setSpacing(10)

        for i, route in enumerate(
            ["scoreboard", "background", "standings", "countdown", "bracket", "spotify"]
        ):
            url = "localhost:8000/%s" % route
            text_url = QLineEdit(url)
            text_url.setProperty("code", True)
            text_url.setReadOnly(True)

            btn_url = QPushButton("⧉")
            btn_url.clicked.connect(text_url.copy)

            self.addWidget(text_url, i, 0)
            self.addWidget(btn_url, i, 1)
