import sys
from src.window import MainWindow
# from src.window_pru import MainWindow
from PySide2 import QtWidgets, QtGui

def main():
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.setWindowTitle("Guias App")
    window.resize(600, 500)

    icon = QtGui.QIcon('src/public/icon.png')
    window.setWindowIcon(icon)
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()