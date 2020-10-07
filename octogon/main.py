import sys
import signal
import traceback

sys.path.append("./src/")

# from server import start_server, create_server
from octogon.config import print
from octogon.daemon.server import start_server, stop_server
from octogon.daemon.scss import SCSSAutoCompiler
from octogon.lookup import characters
from octogon.data import scoreboard
from octogon.gui import SBTextWidget, SBDropdownWidget, SBWinsWidget
import threading
from multiprocessing import Process

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
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

# allows program to exit with CTRL+C
signal.signal(signal.SIGINT, signal.SIG_DFL)


class OctogonWidget(QMainWindow):
    def __init__(self):
        super().__init__()

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

        self.sb_p1_name = SBTextWidget(wid, "P1 Name", key="p1.name")
        self.sb_p2_name = SBTextWidget(wid, "P2 Name", key="p2.name")

        character_names = characters.values()

        self.sb_p1_char = SBDropdownWidget(
            wid, "Character", key="p1.character"
        )
        self.sb_p1_char.edit.addItems(character_names)

        self.sb_p2_char = SBDropdownWidget(
            wid, "Character", key="p2.character"
        )
        self.sb_p2_char.edit.addItems(character_names)

        # self.sb_p1_wins = QButtonGroup(self)
        self.sb_p1_wins = SBWinsWidget(self, "Wins", "p1.wins")
        self.sb_p2_wins = SBWinsWidget(self, "Wins", "p2.wins")

        self.sb_round_title = SBTextWidget(self, "Round Title", "round_title")
        self.sb_round_games = SBDropdownWidget(self, "Best of", "round_games")
        self.sb_round_games.edit.addItems(["3", "5"])

        self.sb_update_bt = QPushButton("Update")
        self.sb_update_bt.clicked.connect(scoreboard.save)

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

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Q:
            self.close()


def main():

    # server = create_server()
    observer = SCSSAutoCompiler()

    try:
        # configure QT window
        app = QApplication(sys.argv)
        window = OctogonWidget()  # NOQA

        # start server in another thread
        # thread = threading.Thread(target=start_server, args=(server,))
        thread = Process(target=start_server)
        thread.daemon = True
        thread.start()

        # start SCSS autocompiler
        # watcher_thread = threading.Thread(target=observer.start)
        # watcher_thread.daemon = True
        # watcher_thread.start()
        observer.start()

        app.exec_()

    except KeyboardInterrupt:
        raise KeyboardInterrupt()

    except Exception:
        print(traceback.format_exc())

    finally:
        thread.terminate()
        thread.join()
        print("server has stopped.")
        observer.stop()
        # watcher_thread.join()
        print("scss compiler has stopped.")


main()
