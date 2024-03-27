import sys
from src.window import MainWindow
from PySide2 import QtWidgets

def main():
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.setWindowTitle("Mi Aplicación")
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()