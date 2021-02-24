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
        self.window.sb_update_bt.setText("Scoreboard updated!")

        def _reset_button():
            self.window.sb_update_bt.setText("Update")

        # reset button text after 2 seconds
        Timer(2.0, _reset_button).start()

    def swap(self):
        """Swap P1 and P2's information."""

        win = self.window

        # swap names
        p1_name = win.sb_p1_name.edit.text()
        p2_name = win.sb_p2_name.edit.text()
        win.sb_p1_name.edit.setText(p2_name)
        win.sb_p2_name.edit.setText(p1_name)

        # swap characters
        p1_char = win.sb_p1_char.edit.currentIndex()
        p2_char = win.sb_p2_char.edit.currentIndex()
        win.sb_p1_char.edit.setCurrentIndex(p2_char)
        win.sb_p2_char.edit.setCurrentIndex(p1_char)

        # swap wins
        p1_wins = [btn.isChecked() for btn in win.sb_p1_wins.btns]
        p2_wins = [btn.isChecked() for btn in win.sb_p2_wins.btns]
        [win.sb_p1_wins.btns[i].setChecked(p2_wins[i]) for i in range(len(p1_wins))]
        [win.sb_p2_wins.btns[i].setChecked(p1_wins[i]) for i in range(len(p2_wins))]

