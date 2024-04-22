import sys, os
from src.views.main_window import MainWindow
from PySide2 import QtWidgets, QtGui

current_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), ".\\.")))     
img_path = os.path.join(current_path, "src", "public", "img", "icon.png")

def main():
    app = QtWidgets.QApplication([])

    window = MainWindow()
    window.setWindowTitle("Guias App")
    window.resize(590, 500)

    icon = QtGui.QIcon(img_path)
    window.setWindowIcon(icon)
    window.show()
    sys.exit(app.exec_()) 
    

if __name__ == "__main__":
    main()