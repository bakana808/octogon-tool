import sys
from server import start_server, create_server
from watcher import start_watcher
import threading
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
)


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

        grid = QGridLayout()
        grid.setSpacing(10)

        # sub-layout for smash.gg related options
        smash_group = QGridLayout(self)
        smash_group.addWidget(smash_title_label, 0, 0)
        smash_group.addWidget(smash_tourny_label, 1, 0)
        smash_group.addWidget(smash_tourny_edit, 1, 1)
        smash_group.addWidget(smash_event_label, 2, 0)
        smash_group.addWidget(smash_event_edit, 2, 1)

        grid.addLayout(smash_group, 0, 0)
        spacer = QSpacerItem(QSizePolicy.Minimum, QSizePolicy.Expanding)
        grid.addItem(spacer, 1, 0, 1, -1)

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

    server = create_server()
    observer = start_watcher()

    try:
        app = QApplication(sys.argv)

        window = OctogonWidget()
        # start server in another thread

        thread = threading.Thread(target=start_server, args=(server,))
        thread.daemon = True
        thread.start()

        watcher_thread = threading.Thread(target=observer.start)
        watcher_thread.daemon = True
        watcher_thread.start()

        app.exec()
    except Exception as e:
        print(e)
    finally:
        server.shutdown()
        thread.join()
        print("server has stopped.")
        observer.stop()
        watcher_thread.join()
        print("watcher has stopped.")


main()
