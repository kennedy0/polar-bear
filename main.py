import os
import sys

from PyQt5 import QtWidgets, QtCore

from windows.main_window import ScreenRecorder


def main(args):
    app = QtWidgets.QApplication(args)
    app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    title = "PolarBear"

    window = ScreenRecorder(title=title)
    window.show()
    window.set_window_width(window.config['default_width'])
    window.set_window_height(window.config['default_height'])

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
