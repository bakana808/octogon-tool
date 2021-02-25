from typing import TYPE_CHECKING
from threading import Timer

if TYPE_CHECKING:
    from octogon.gui.window import OctogonWidget


class WindowListener:
    """
    Contains methods that are called when something happens
    to the main window.
    """

    def __init__(self, window: "OctogonWidget"):
        self.window = window

    def update_scoreboard(self):
        """Update the scoreboard."""
        self.window.octogon.scoreboard.save()
        self.window.widgets["update_btn"].setText("Scoreboard updated!")

        def _reset_button():
            self.window.widgets["update_btn"].setText("Update")

        # reset button text after 2 seconds
        Timer(2.0, _reset_button).start()

    def swap(self):
        """Swap P1 and P2's information."""

        win = self.window

        # swap names
        p1_name = win.widgets["p1.name"].edit.text()
        p2_name = win.widgets["p2.name"].edit.text()
        win.widgets["p1.name"].edit.setText(p2_name)
        win.widgets["p2.name"].edit.setText(p1_name)

        # swap characters
        p1_char = win.widgets["p1.character"].cb_char.currentIndex()
        p2_char = win.widgets["p2.character"].cb_char.currentIndex()
        win.widgets["p1.character"].cb_char.setCurrentIndex(p2_char)
        win.widgets["p2.character"].cb_char.setCurrentIndex(p1_char)

        p1_color = win.widgets["p1.character"].cb_color.currentIndex()
        p2_color = win.widgets["p2.character"].cb_color.currentIndex()
        win.widgets["p1.character"].cb_color.setCurrentIndex(p2_color)
        win.widgets["p2.character"].cb_color.setCurrentIndex(p1_color)

        # swap wins
        p1_wins = [btn.isChecked() for btn in win.widgets["p1.wins"].btns]
        p2_wins = [btn.isChecked() for btn in win.widgets["p2.wins"].btns]
        [
            win.widgets["p1.wins"].btns[i].setChecked(p2_wins[i])
            for i in range(len(p1_wins))
        ]
        [
            win.widgets["p2.wins"].btns[i].setChecked(p1_wins[i])
            for i in range(len(p2_wins))
        ]
