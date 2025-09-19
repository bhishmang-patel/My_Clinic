# main.py

import sys
import os
from PyQt5.QtWidgets import QApplication
from ui.login_ui import LoginWindow
from database.db_setup import create_tables

if __name__ == "__main__":
    create_tables()

    # Fix scaling warning
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)

    # Load QSS style
    try:
        with open("assets/style.qss", "r") as f:
            style = f.read()
            app.setStyleSheet(style)
    except FileNotFoundError:
        print("Style file not found. Using default style.")

    win = LoginWindow()
    win.show()
    sys.exit(app.exec_())
