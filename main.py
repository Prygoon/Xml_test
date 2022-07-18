import sys

from PyQt5.QtWidgets import QApplication

from GUI.mainwindow import MainWindow


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.resize(640, 480)
    window.show()

    return app.exec_()


if __name__ == '__main__':
    main()

