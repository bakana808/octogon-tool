import traceback
from typing import TYPE_CHECKING

# from server import start_server, create_server
from octogon.utils.data import NestedDict
from octogon.utils.logger import get_print_fn
from octogon.utils.lookup import characters
from octogon.gui.gui import SBTextWidget, SBDropdownWidget, SBWinsWidget, SBPortWidget
from octogon.gui.listener import WindowListener

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QAction,
    qApp,
    QLabel,
    QGridLayout,
    QLineEdit,
    QWidget,
    QPushButton,
)

if TYPE_CHECKING:
    from octogon import Octogon

WINDOW_SIZE = (750, 0)

print = get_print_fn("qt")


class OctogonWidget(QMainWindow):
    def __init__(self, octogon: "Octogon"):
        # configure QT window
        self.app = QApplication([])
        # self.app.setStyle(QStyleFactory.create("GTK+"))

        super().__init__()

        self.octogon = octogon
        self.widgets = NestedDict({})
        self.listener = WindowListener(self)

        # layout
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # player names
        self.sb_p1_name = SBTextWidget(self, "P1 Name", key="p1.name")
        self.sb_p2_name = SBTextWidget(self, "P2 Name", key="p2.name")

        # characters chosen
        character_names = list(characters.values())

        self.sb_p1_char = SBDropdownWidget(
            self, "Character", key="p1.character", items=character_names
        )

        self.sb_p2_char = SBDropdownWidget(
            self, "Character", key="p2.character", items=character_names
        )

        # number of wins per player
        # self.sb_p1_wins = QButtonGroup(self)
        self.sb_p1_wins = SBWinsWidget(self, "Wins", "p1.wins")
        self.sb_p2_wins = SBWinsWidget(self, "Wins", "p2.wins")

        # controller port per player
        self.sb_p1_port = SBPortWidget(self, "p1.port", 0)
        self.sb_p2_port = SBPortWidget(self, "p1.port", 1)

        # round title
        self.sb_round_title = SBTextWidget(self, "Round Title", "round_title")

        # best of 3/5
        self.sb_round_games = SBDropdownWidget(
            self, "Best of", "round_games", ["3", "5"]
        )

        self.sb_update_bt = QPushButton("Update")
        self.sb_update_bt.clicked.connect(self.listener.update_scoreboard)

        self.sb_bt_swap = QPushButton("Swap P1/P2")
        self.sb_bt_swap.clicked.connect(self.listener.swap)

        # sub-layout for scoreboard options
        sb_group = QGridLayout(wid)
        sb_group.setSpacing(12)

        sb_group.addWidget(self.sb_p1_name.label, 0, 0, 1, 2)
        sb_group.addWidget(self.sb_p1_name.edit, 0, 2, 1, 4)
        for i, btn in enumerate(self.sb_p1_port.btns):
            sb_group.addWidget(btn, 0, 6 + i)

        sb_group.addWidget(self.sb_p2_name.label, 0, 10, 1, 2)
        sb_group.addWidget(self.sb_p2_name.edit, 0, 12, 1, 4)
        for i, btn in enumerate(self.sb_p2_port.btns):
            sb_group.addWidget(btn, 0, 16 + i)

        sb_group.addWidget(self.sb_p1_char.label, 1, 0, 1, 2)
        sb_group.addWidget(self.sb_p1_char.edit, 1, 2, 1, 4)
        sb_group.addWidget(self.sb_p2_char.label, 1, 10, 1, 2)
        sb_group.addWidget(self.sb_p2_char.edit, 1, 12, 1, 4)

        sb_group.addWidget(self.sb_p1_wins.label, 2, 0, 1, 2)
        for i, btn in enumerate(self.sb_p1_wins.btns):
            sb_group.addWidget(btn, 2, 2 + i)

        sb_group.addWidget(self.sb_p2_wins.label, 2, 10, 1, 2)
        for i, btn in enumerate(self.sb_p2_wins.btns):
            sb_group.addWidget(btn, 2, 12 + i)

        sb_group.addWidget(self.sb_round_title.label, 3, 0, 1, 2)
        sb_group.addWidget(self.sb_round_title.edit, 3, 2, 1, 4)
        sb_group.addWidget(self.sb_round_games.label, 3, 6, 1, 2)
        sb_group.addWidget(self.sb_round_games.edit, 3, 8, 1, 2)
        sb_group.addWidget(self.sb_bt_swap, 3, 10, 1, 10)

        sb_group.addWidget(self.sb_update_bt, 4, 0, 1, 20)

        # grid.addLayout(sb_group, 0, 0)

        wid.setLayout(sb_group)

        # menubar
        # -------
        # action = QAction("&Exit", self)
        # action.setShortcut("Ctrl+C")
        # action.setStatusTip("Close the panel")
        # action.triggered.connect(qApp.quit)
        # menubar = self.menuBar()
        # fileMenu = menubar.addMenu("&File")
        # fileMenu.addAction(action)

        self.update_css()
        self.setFixedSize(*WINDOW_SIZE)
        self.setGeometry(300, 300, *WINDOW_SIZE)
        self.setWindowTitle("Octogon")
        self.show()

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_C:
            self.close()

    def update_css(self):
        """Re-read the stylesheet for the window."""
        with open("site/style/window.css", "r") as f:
            self.setStyleSheet(f.read())
            print("updated window stylesheet")

    def start(self):
        """Start the QT application. The process will loop on this function."""
        try:
            timer = QTimer()
            timer.start(500)
            timer.timeout.connect(lambda: None)
            self.app.exec_()

        except KeyboardInterrupt:
            pass

        except Exception:
            print(traceback.format_exc())

        finally:
            self.close()
