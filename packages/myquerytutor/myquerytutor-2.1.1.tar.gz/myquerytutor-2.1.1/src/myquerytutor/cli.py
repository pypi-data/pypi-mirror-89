
import sys
from PyQt5.QtWidgets import QApplication
from myquerytutor.mainwindow import MainWindow


def main(argv=sys.argv):
    """
    Args:
        argv (list): List of arguments

    Returns:
        int: A return code

    Does stuff.
    """
    sys.argv.append("--disable-web-security")
    app = QApplication(sys.argv)
    app.setOrganizationName("Tuxtas")
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())

    return 0
