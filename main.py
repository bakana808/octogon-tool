import sys
from server import start_server, create_server
import threading
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QApplication, QWidget


class OctogonWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle("Octogon Panel")
        self.show()

    def keyPressEvent(self, e: QKeyEvent):
        if e.key() == Qt.Key_Q:
            self.close()


def main():

    try:
        app = QApplication(sys.argv)

        window = OctogonWidget()

        # start server in another thread

        server = create_server()
        thread = threading.Thread(target=start_server, args=(server, ))
        thread.daemon = True
        thread.start()

        app.exec()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        print("server has stopped.")


main()
