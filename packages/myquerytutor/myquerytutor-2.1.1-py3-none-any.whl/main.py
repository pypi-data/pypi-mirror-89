#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import QApplication
from myquerytutor.mainwindow import MainWindow


def main():
    sys.argv.append("--disable-web-security")
    app = QApplication(sys.argv)
    app.setOrganizationName("Tuxtas")
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
