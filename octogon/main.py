import traceback

# from server import start_server, create_server
import octogon.config
from octogon.lookup import characters
from octogon.gui import SBTextWidget, SBDropdownWidget, SBWinsWidget

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QAction,
    qApp,
    QStyleFactory,
)
from PyQt5.QtWidgets import (
    QLabel,
    QGridLayout,
    QLineEdit,
    QWidget,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QPushButton,
    QButtonGroup,
    QCheckBox,
)

print = octogon.config.get_print_fn("qt")


class OctogonWidget(QMainWindow):
    def __init__(self, octogon):
        super().__init__()

        self.octogon = octogon
        scoreboard = octogon.scoreboard

        # layout
        wid = QWidget(self)
        self.setCentralWidget(wid)

        smash_title_label = QLabel("Smash.gg Settings")
        smash_title_label.setAlignment(Qt.AlignBottom)
        # smash_title_label.setStyleSheet("QLabel {background-color: red;}")
        smash_tourny_label = QLabel("Tournament Slug")
        smash_event_label = QLabel("Event ID")

        smash_tourny_edit = QLineEdit()
        smash_event_edit = QLineEdit()

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

        # round title
        self.sb_round_title = SBTextWidget(self, "Round Title", "round_title")

        # best of 3/5
        self.sb_round_games = SBDropdownWidget(
            self, "Best of", "round_games", ["3", "5"]
        )

        self.sb_update_bt = QPushButton("Update")
        self.sb_update_bt.clicked.connect(scoreboard.save)

        self.sb_bt_swap = QPushButton("Swap P1/P2")
        self.sb_bt_swap.clicked.connect(self.swap)

        grid = QGridLayout(wid)
        grid.setSpacing(10)

        # sub-layout for scoreboard options
        sb_group = QGridLayout(wid)
        sb_group.addWidget(self.sb_p1_name.label, 0, 0)
        sb_group.addWidget(self.sb_p1_name.edit, 0, 1, 1, 3)
        sb_group.addWidget(self.sb_p2_name.label, 0, 4)
        sb_group.addWidget(self.sb_p2_name.edit, 0, 5, 1, 3)
        sb_group.addWidget(self.sb_p1_char.label, 1, 0)
        sb_group.addWidget(self.sb_p1_char.edit, 1, 1, 1, 3)
        sb_group.addWidget(self.sb_p2_char.label, 1, 4)
        sb_group.addWidget(self.sb_p2_char.edit, 1, 5, 1, 3)

        sb_group.addWidget(self.sb_p1_wins.label, 2, 0)
        for i, btn in enumerate(self.sb_p1_wins.btns):
            sb_group.addWidget(btn, 2, i + 1)

        sb_group.addWidget(self.sb_p2_wins.label, 2, 4)
        for i, btn in enumerate(self.sb_p2_wins.btns):
            sb_group.addWidget(btn, 2, i + 5)

        sb_group.addWidget(self.sb_round_title.label, 3, 0)
        sb_group.addWidget(self.sb_round_title.edit, 3, 1, 1, 3)
        sb_group.addWidget(self.sb_round_games.label, 3, 4)
        sb_group.addWidget(self.sb_round_games.edit, 3, 5, 1, 3)

        sb_group.addWidget(self.sb_update_bt, 4, 0, 1, 8)
        sb_group.addWidget(self.sb_bt_swap, 5, 0, 1, 8)

        # sub-layout for smash.gg related options
        smash_group = QGridLayout(wid)
        smash_group.addWidget(smash_title_label, 0, 0)
        smash_group.addWidget(smash_tourny_label, 1, 0)
        smash_group.addWidget(smash_tourny_edit, 1, 1)
        smash_group.addWidget(smash_event_label, 2, 0)
        smash_group.addWidget(smash_event_edit, 2, 1)

        grid.addLayout(sb_group, 0, 0)
        grid.addLayout(smash_group, 1, 0)

        wid.setLayout(grid)

        # menubar

        action = QAction("&Exit", self)
        action.setShortcut("Ctrl+C")
        action.setStatusTip("Close the panel")
        action.triggered.connect(qApp.quit)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(action)

        self.statusBar().showMessage("Ready")

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("Octogon Panel")
        self.show()

    def swap(self):
        """Swap P1 and P2's information."""

        # swap names
        p1_name = self.sb_p1_name.edit.text()
        p2_name = self.sb_p2_name.edit.text()
        self.sb_p1_name.edit.setText(p2_name)
        self.sb_p2_name.edit.setText(p1_name)

        # swap characters
        p1_char = self.sb_p1_char.edit.currentIndex()
        p2_char = self.sb_p2_char.edit.currentIndex()
        self.sb_p1_char.edit.setCurrentIndex(p2_char)
        self.sb_p2_char.edit.setCurrentIndex(p1_char)

        # swap wins
        p1_wins = [btn.isChecked() for btn in self.sb_p1_wins.btns]
        p2_wins = [btn.isChecked() for btn in self.sb_p2_wins.btns]
        [self.sb_p1_wins.btns[i].setChecked(p2_wins[i]) for i in range(len(p1_wins))]
        [self.sb_p2_wins.btns[i].setChecked(p1_wins[i]) for i in range(len(p2_wins))]

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Q:
            self.close()


def start_gui_loop(octogon):
    """Start the QT application. The process will loop on this function."""

    try:
        # configure QT window
        app = QApplication([])
        # app.setStyle(QStyleFactory.create("GTK+"))

        # create main window
        window = OctogonWidget(octogon)  # NOQA

        app.exec_()

    except KeyboardInterrupt:
        raise KeyboardInterrupt()

    except Exception:
        print(traceback.format_exc())

    finally:
        octogon.on_close()
