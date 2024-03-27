from PySide2 import QtCore, QtWidgets, QtGui
from src.data.dataFile import searchClientByName

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        #! Header
        header_layout = QtWidgets.QGridLayout()
        logo_label = QtWidgets.QLabel()
        logo_label.setPixmap(QtGui.QPixmap(""))  # Ruta a la imagen del logo
        self.title_label = QtWidgets.QLabel("Generar Ruta de Envio")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        # Add layout
        header_layout.addWidget(self.title_label, 0, 0, 1, 2)
        # header_layout.addWidget(logo_label, 0, 0)

        #! Serach
        search_layout = QtWidgets.QGridLayout()

        # Inputs
        self.search_edit = QtWidgets.QLineEdit()
        self.search_edit.setPlaceholderText("Buscar cliente por nombre")

        # Buttons
        self.search_button = QtWidgets.QPushButton("Buscar")
        self.search_button_update = QtWidgets.QPushButton("Actualizar")

        # Table
        self.table = QtWidgets.QTableWidget()
        self.table.itemSelectionChanged.connect(self.tableItemChanged)

        # Add layout
        search_layout.addWidget(self.search_edit, 0, 0)
        search_layout.addWidget(self.search_button, 0, 1)
        search_layout.addWidget(self.search_button_update, 0, 2)
        search_layout.addWidget(self.table, 1, 0, 1, 3)


        #! Main layout
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.addLayout(header_layout, 0, 0, 1, 2)  # Encabezado ocupa dos columnas
        main_layout.addLayout(search_layout, 1, 0)

        #! Styles
        self.apply_style()

        #! Events
        self.search_button.clicked.connect(self.search_client)
        # self.modify_button.clicked.connect(self.modify_client)

    @QtCore.Slot()
    def search_client(self):
        # Lógica para buscar clientes
        search_text = self.search_edit.text()
        result = searchClientByName(search_text)
        self.update_table(result)

    @QtCore.Slot()
    def modify_client(self):
        # Lógica para modificar clientes
        print("Modificando cliente...")

    @QtCore.Slot()
    def update_search(self):
        pass

    def update_table(self, clients):
        self.table.clearContents() # Limpiar contenido
        self.table.setRowCount(len(clients))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nombre", "Identificacion", "Ciudad", "Teléfono"])
        
        # Seleccionar toda la fila
        self.table.setSelectionMode(QtWidgets.QTableWidget.SingleSelection)
        self.table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)  
        self.table.verticalHeader().setVisible(False) 

        for row, client in enumerate(clients):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(client["name"]))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(client["vat"]))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(client["city"]))
            self.table.setItem(row, 3, QtWidgets.QTableWidgetItem(client["phone"]))

    def tableItemChanged(self):
        selected_items = self.table.selectedItems()
        if selected_items:
            row = selected_items[0].row()
            name = self.table.item(row, 0).text()
            vat = self.table.item(row, 1).text()
            city = self.table.item(row, 2).text()
            phone = self.table.item(row, 3).text()
            print("Cliente seleccionado:", name, vat, city, phone)

    def apply_style(self):
        # Estilo para los iconos
        QtWidgets.QApplication.setStyle("Fusion")

        # Estilo para los widgets
        widget_style = """
            QLabel {
                color: #333333;  /* Color del texto para los labels */
                font-size: 14px;  /* Tamaño de fuente */
                font-family: sans-serif;  /* Fuente */
            }

            QLineEdit{
                background-color: #f0f0f0;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 8px;
            }

            QLineEdit:focus {
                border: 2px solid #4CAF50;
                padding: 10px;
            }

            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }

            QTableWidget::item:selected {
                background-color: #4CAF50;
                border: 1px solid gray;
                border-radius: 5px;
                color: white;
            }
        """

        # Table
        self.table.setStyleSheet(widget_style)

        # Labels
        self.title_label.setStyleSheet(widget_style)

        # Inputs
        self.search_edit.setStyleSheet(widget_style)
        
        # Buttons
        self.search_button.setStyleSheet(widget_style)
        self.search_button_update.setStyleSheet(widget_style)