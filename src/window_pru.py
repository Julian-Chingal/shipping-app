from PySide2 import QtCore, QtWidgets, QtGui
from data.dataFile import searchClientByName

class CellWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Diseño del widget (considerar layout)
        # ...

        # Crear botones de edición e impresión (tamaño e iconos según preferencia)
        self.edit_button = QtWidgets.QPushButton()
        self.edit_button.setIcon(QtGui.QIcon("src/public/edit_icon.png"))
        self.edit_button.setIconSize(QtCore.QSize(24, 24))
        self.edit_button.setFixedSize(30, 30)

        self.print_button = QtWidgets.QPushButton("P")

        # Conectar botones a métodos correspondientes
        self.edit_button.clicked.connect(self.edit_client)
        self.print_button.clicked.connect(self.print_client)

    @QtCore.Slot()
    def edit_client(self):
        # Lógica para modificar clientes
        print("Modificando cliente...")

    @QtCore.Slot()
    def print_client(self):
        # Lógica para imprimir clientes
        print("Imprimiendo cliente...")


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        # ... (código original omitido)

        # Styles (consider separating into a stylesheet)
        self.apply_style()

        # Event connections
        self.search_button.clicked.connect(self.search_client)
        self.search_edit.returnPressed.connect(self.search_client)

    @QtCore.Slot()
    def search_client(self):
        search_text = self.search_edit.text()
        result = searchClientByName(search_text)
        if result:
            self.update_table(result)
        else:
            messageBox = QtWidgets.QMessageBox()
            messageBox.information(self, "Cliente no encontrado",
                                   "No se encontraron clientes con el nombre especificado.")
            self.search_edit.clear()

    def update_table(self, clients):
        self.table.clearContents()
        self.table.setRowCount(len(clients))

        for row, client in enumerate(clients):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(client["name"]))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(client["vat"]))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(client["city"]))

            # Crear widget de celda personalizado
            widget = CellWidget()
            widget.setup(client["name"], lambda: self.edit_client(), lambda: self.print_client())
            self.table.setCellWidget(row, 3, widget)


# Crear botones una vez
edit_button = QtWidgets.QPushButton()
edit_button.setIcon(QtGui.QIcon("src/public/icon.png"))
edit_button.setIconSize(QtCore.QSize(24, 24))
edit_button.setFixedSize(30, 30)

print_button = QtWidgets.QPushButton("P")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
