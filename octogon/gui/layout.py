"""
Handles setting up the layout for the main QT
"""

from PyQt5.QtWidgets import (
    QGridLayout,
    QWidget,
    QPushButton,
)

import typing
from octogon.gui.gui import SBTextWidget, SBDropdownWidget, SBWinsWidget, SBPortWidget
from octogon.utils.lookup import characters

if typing.TYPE_CHECKING:
    from octogon.gui.window import OctogonWidget


def create_layout(window: "OctogonWidget") -> QWidget:

    wid = QWidget(window)
    window.setCentralWidget(wid)

    # player names
    sb_p1_name = window.sb_text("P1 Name", "p1.name")
    sb_p2_name = window.sb_text("P2 Name", "p2.name")

    # characters chosen
    character_names = list(characters.values())

    sb_p1_char = window.sb_dropdown(
        "Character", key="p1.character", items=character_names
    )

    sb_p2_char = window.sb_dropdown(
        "Character", key="p2.character", items=character_names
    )

    # number of wins per player
    # sb_p1_wins = QButtonGroup(window)
    sb_p1_wins = window.sb_wins("Wins", "p1.wins")
    sb_p2_wins = window.sb_wins("Wins", "p2.wins")

    # controller port per player
    sb_p1_port = window.sb_port("p1.port", 0)
    sb_p2_port = window.sb_port("p2.port", 1)

    # round title
    sb_round_title = window.sb_text("Round Title", "round_title")

    # best of 3/5
    sb_round_games = window.sb_dropdown("Best of", "round_games", ["3", "5"])

    sb_update_bt = window._button("Update", "update_btn")
    sb_update_bt.clicked.connect(window.listener.update_scoreboard)

    sb_bt_swap = window._button("Swap P1/P2", "swap_btn")
    sb_bt_swap.clicked.connect(window.listener.swap)

    # sub-layout for scoreboard options
    sb_group = QGridLayout(wid)
    sb_group.setSpacing(12)

    sb_group.addWidget(sb_p1_name.label, 0, 0, 1, 2)
    sb_group.addWidget(sb_p1_name.edit, 0, 2, 1, 4)
    for i, btn in enumerate(sb_p1_port.btns):
        sb_group.addWidget(btn, 0, 6 + i)

    sb_group.addWidget(sb_p2_name.label, 0, 10, 1, 2)
    sb_group.addWidget(sb_p2_name.edit, 0, 12, 1, 4)
    for i, btn in enumerate(sb_p2_port.btns):
        sb_group.addWidget(btn, 0, 16 + i)

    sb_group.addWidget(sb_p1_char.label, 1, 0, 1, 2)
    sb_group.addWidget(sb_p1_char.edit, 1, 2, 1, 4)
    sb_group.addWidget(sb_p2_char.label, 1, 10, 1, 2)
    sb_group.addWidget(sb_p2_char.edit, 1, 12, 1, 4)

    sb_group.addWidget(sb_p1_wins.label, 2, 0, 1, 2)
    for i, btn in enumerate(sb_p1_wins.btns):
        sb_group.addWidget(btn, 2, 2 + i)

    sb_group.addWidget(sb_p2_wins.label, 2, 10, 1, 2)
    for i, btn in enumerate(sb_p2_wins.btns):
        sb_group.addWidget(btn, 2, 12 + i)

    sb_group.addWidget(sb_round_title.label, 3, 0, 1, 2)
    sb_group.addWidget(sb_round_title.edit, 3, 2, 1, 4)
    sb_group.addWidget(sb_round_games.label, 3, 6, 1, 2)
    sb_group.addWidget(sb_round_games.edit, 3, 8, 1, 2)
    sb_group.addWidget(sb_bt_swap, 3, 10, 1, 10)

    sb_group.addWidget(sb_update_bt, 4, 0, 1, 20)

    # grid.addLayout(sb_group, 0, 0)

    wid.setLayout(sb_group)

    return wid
