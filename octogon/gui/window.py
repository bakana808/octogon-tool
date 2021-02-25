import traceback
import qtsass
from typing import TYPE_CHECKING

# from server import start_server, create_server
from octogon.utils.data import NestedDict
from octogon.utils.logger import get_print_fn
from octogon.gui.listener import WindowListener
from octogon.gui.layout import create_layout
from octogon.gui.gui import SBTextWidget, SBDropdownWidget, SBWinsWidget, SBPortWidget

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

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
        self.widgets = NestedDict({}, True)
        self.listener = WindowListener(self)
        self.widget = create_layout(self)

        # layout
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
        # compile the scss file
        qtsass.compile_filename(
            "templates/qtsass/window.scss", "sites/style/window.css"
        )

        with open("sites/style/window.css", "r") as f:
            self.setStyleSheet(f.read())
            # print("updated window stylesheet")

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

    def __set_widget(self, key, widget):
        self.widgets[key] = widget
        return widget

    def _button(self, text, key) -> QPushButton:
        btn = QPushButton(text)
        btn.setObjectName(key)
        return self.__set_widget(key, btn)

    def sb_text(self, name, key) -> SBTextWidget:
        return self.__set_widget(key, SBTextWidget(self, name, key))

    def sb_dropdown(self, name, key, items) -> SBDropdownWidget:
        return self.__set_widget(key, SBDropdownWidget(self, name, key, items))

    def sb_wins(self, name, key) -> SBWinsWidget:
        return self.__set_widget(key, SBWinsWidget(self, name, key))

    def sb_port(self, key, port) -> SBPortWidget:
        return self.__set_widget(key, SBPortWidget(self, key, port))
