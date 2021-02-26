"""
Handles setting up the layout for the main QT
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QLabel,
    QGridLayout,
    QWidget,
    QPushButton,
)

from PyQt5.QtCore import QMargins

import typing
from octogon.gui.gui import SBTextWidget, SBDropdownWidget, SBWinsWidget, SBPortWidget
from octogon.gui.layouts.tab import TabLayout
from octogon.gui.layouts.scoreboard import ScoreboardLayout

if typing.TYPE_CHECKING:
    from octogon.gui.window import OctogonWindow


def create_layout(window: "OctogonWindow") -> QWidget:

    widget = QWidget(window)
    window.setCentralWidget(widget)

    layout = QGridLayout(window)
    layout.setSpacing(0)
    layout.setContentsMargins(QMargins(0, 0, 0, 0))

    widget.setLayout(layout)

    # title bar
    # -------------------------------------------------

    title_widget = QWidget(widget)
    title_widget.setObjectName("title_layout")
    title_layout = QGridLayout(title_widget)
    title_widget.setLayout(title_layout)

    sb_title = QLabel("Octogon Tool")
    sb_title.setObjectName("title")
    sb_title.setAlignment(Qt.AlignLeft | Qt.AlignBottom)

    sb_exit = QPushButton("✖")
    sb_exit.setObjectName("exit_btn")
    sb_exit.setFixedSize(20, 20)
    sb_exit.clicked.connect(window.close)

    title_layout.addWidget(sb_title, 0, 0)
    title_layout.addWidget(sb_exit, 0, 1)

    # scoreboard controls
    # -------------------------------------------------

    body_layout = TabLayout(window)

    layout.addWidget(title_widget, 0, 0)
    layout.addLayout(body_layout, 1, 0)

    return widget
