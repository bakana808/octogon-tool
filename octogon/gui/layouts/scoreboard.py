from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore import QMargins

import typing
from octogon.utils.lookup import characters

if typing.TYPE_CHECKING:
    from octogon.gui.window import OctogonWidget


class ScoreboardLayout(QGridLayout):
    """The QT layout that displays the scoreboard controls."""

    def __init__(self, window: "OctogonWidget"):
        super().__init__(window)

        self.setContentsMargins(QMargins(20, 20, 20, 20))
        self.setSpacing(10)

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

        self.addWidget(sb_p1_name.label, 1, 0, 1, 2)
        self.addWidget(sb_p1_name.edit, 1, 2, 1, 4)
        for i, btn in enumerate(sb_p1_port.btns):
            self.addWidget(btn, 1, 6 + i)

        self.addWidget(sb_p2_name.label, 1, 10, 1, 2)
        self.addWidget(sb_p2_name.edit, 1, 12, 1, 4)
        for i, btn in enumerate(sb_p2_port.btns):
            self.addWidget(btn, 1, 16 + i)

        self.addWidget(sb_p1_char.label, 2, 0, 1, 2)
        self.addWidget(sb_p1_char.edit, 2, 2, 1, 4)
        self.addWidget(sb_p2_char.label, 2, 10, 1, 2)
        self.addWidget(sb_p2_char.edit, 2, 12, 1, 4)

        self.addWidget(sb_p1_wins.label, 3, 0, 1, 2)
        for i, btn in enumerate(sb_p1_wins.btns):
            self.addWidget(btn, 3, 2 + i)

        self.addWidget(sb_p2_wins.label, 3, 10, 1, 2)
        for i, btn in enumerate(sb_p2_wins.btns):
            self.addWidget(btn, 3, 12 + i)

        self.addWidget(sb_round_title.label, 4, 0, 1, 2)
        self.addWidget(sb_round_title.edit, 4, 2, 1, 4)
        self.addWidget(sb_round_games.label, 4, 6, 1, 2)
        self.addWidget(sb_round_games.edit, 4, 8, 1, 2)
        self.addWidget(sb_bt_swap, 4, 10, 1, 10)

        self.addWidget(sb_update_bt, 5, 0, 1, 20)
