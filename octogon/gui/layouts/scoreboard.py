from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtCore import QMargins, Qt

import typing
from octogon.gui.gui import SBCharacterWidget

if typing.TYPE_CHECKING:
    from octogon.gui.window import OctogonWindow


class ScoreboardLayout(QGridLayout):
    """The QT layout that displays the scoreboard controls."""

    def __init__(self, window: "OctogonWindow"):
        super().__init__(window)

        self.setContentsMargins(QMargins(20, 20, 20, 20))
        self.setAlignment(Qt.AlignBottom)
        self.setSpacing(10)

        # player names
        p1_name = window.sb_text("P1 Name", "p1.name")
        p2_name = window.sb_text("P2 Name", "p2.name")

        # characters chosen
        p1_char = SBCharacterWidget(window, "p1.character", "p1.color")
        window.widgets["p1.character"] = p1_char
        p2_char = SBCharacterWidget(window, "p2.character", "p2.color")
        window.widgets["p2.character"] = p2_char

        # number of wins per player
        # p1_wins = QButtonGroup(window)
        p1_wins = window.sb_wins("Wins", "p1.wins")
        p2_wins = window.sb_wins("Wins", "p2.wins")

        # controller port per player
        p1_port = window.sb_port("p1.port", 0)
        p2_port = window.sb_port("p2.port", 1)

        # round title
        round_title = window.sb_text("Round Title", "round_title")

        # best of 3/5
        round_games = window.sb_dropdown("Best of", "round_games", ["3", "5"])

        update_bt = window._button("Update", "update_btn")
        update_bt.clicked.connect(window.listener.update_scoreboard)

        bt_swap = window._button("Swap P1/P2", "swap_btn")
        bt_swap.clicked.connect(window.listener.swap)

        self.addWidget(p1_name.label, 1, 0, 1, 2)
        self.addWidget(p1_name.edit, 1, 2, 1, 4)
        for i, btn in enumerate(p1_port.btns):
            self.addWidget(btn, 1, 6 + i)

        self.addWidget(p2_name.label, 1, 10, 1, 2)
        self.addWidget(p2_name.edit, 1, 12, 1, 4)
        for i, btn in enumerate(p2_port.btns):
            self.addWidget(btn, 1, 16 + i)

        self.addWidget(p1_char.label, 2, 0, 1, 2)
        self.addWidget(p1_char.cb_char, 2, 2, 1, 4)
        self.addWidget(p1_char.cb_color, 2, 6, 1, 4)
        self.addWidget(p2_char.label, 2, 10, 1, 2)
        self.addWidget(p2_char.cb_char, 2, 12, 1, 4)
        self.addWidget(p2_char.cb_color, 2, 16, 1, 4)

        self.addWidget(p1_wins.label, 3, 0, 1, 2)
        for i, btn in enumerate(p1_wins.btns):
            self.addWidget(btn, 3, 2 + i)

        self.addWidget(p2_wins.label, 3, 10, 1, 2)
        for i, btn in enumerate(p2_wins.btns):
            self.addWidget(btn, 3, 12 + i)

        self.addWidget(round_title.label, 4, 0, 1, 2)
        self.addWidget(round_title.edit, 4, 2, 1, 4)
        self.addWidget(round_games.label, 4, 6, 1, 2)
        self.addWidget(round_games.edit, 4, 8, 1, 2)
        self.addWidget(bt_swap, 4, 10, 1, 10)

        self.addWidget(update_bt, 5, 0, 1, 20)
