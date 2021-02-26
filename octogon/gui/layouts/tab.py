from PyQt5.QtWidgets import (
    QGridLayout,
    QPushButton,
    QStackedWidget,
    QWidget,
    QSizePolicy,
)
from PyQt5.QtCore import QMargins

import typing
from octogon.utils.logger import get_print_fn
from octogon.gui.layouts.scoreboard import ScoreboardLayout
from octogon.gui.layouts.overlays import OverlaysLayout

if typing.TYPE_CHECKING:
    from octogon.gui.window import OctogonWindow

print = get_print_fn("qt")


class TabLayout(QGridLayout):
    """The QT layout that displays tabs."""

    def __init__(self, window: "OctogonWindow"):
        super().__init__()

        self.setContentsMargins(QMargins(0, 0, 0, 0))
        self.setSpacing(0)

        self.btn_scoreboard = QPushButton("scoreboard", parent=window)
        self.btn_scoreboard.clicked.connect(lambda: self.set_tab(0))
        self.btn_overlays = QPushButton("overlays", parent=window)
        self.btn_overlays.clicked.connect(lambda: self.set_tab(1))

        # the pages
        self.widget_scoreboard = QWidget(window)
        self.widget_scoreboard.setLayout(ScoreboardLayout(window))
        self.widget_overlays = QWidget(window)
        self.widget_overlays.setLayout(OverlaysLayout(window))

        # the stackedlayout containing the pages
        self.widget_stack = QStackedWidget(window)
        self.widget_stack.addWidget(self.widget_scoreboard)
        self.widget_stack.addWidget(self.widget_overlays)

        self.addWidget(self.btn_scoreboard, 0, 0)
        self.addWidget(self.btn_overlays, 0, 1)

        self.addWidget(self.widget_stack, 1, 0, 1, 2)

        self.set_tab(0)

    def set_tab(self, n: int):

        # print("tab changed")
        IGNORE, EXPAND = QSizePolicy.Ignored, QSizePolicy.Expanding

        if n == 0:
            self.btn_scoreboard.setProperty("tab_selected", True)
            self.btn_overlays.setProperty("tab_selected", False)
            self.widget_scoreboard.setSizePolicy(EXPAND, EXPAND)
            self.widget_overlays.setSizePolicy(IGNORE, IGNORE)
        elif n == 1:
            self.btn_scoreboard.setProperty("tab_selected", False)
            self.btn_overlays.setProperty("tab_selected", True)
            self.widget_scoreboard.setSizePolicy(IGNORE, IGNORE)
            self.widget_overlays.setSizePolicy(EXPAND, EXPAND)

        self.widget_stack.setCurrentIndex(n)
        # update stylesheets
        self.btn_scoreboard.setStyle(self.btn_scoreboard.style())
        self.btn_overlays.setStyle(self.btn_scoreboard.style())
