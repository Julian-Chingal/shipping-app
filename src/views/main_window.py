from PySide2 import QtCore, QtWidgets, QtGui
import functools

from src.data.dataFile import searchClientByName
from src.views.edit_window import EditWindow
from src.views.print_window import PrintWindow

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        #! Header
        header_layout = QtWidgets.QGridLayout()
        
        logo_label = QtWidgets.QLabel()
        logo_label.setPixmap(QtGui.QPixmap("src\public\img\logo.png"))  # Ruta a la imagen del logo
        logo_label.setAlignment(QtCore.Qt.AlignLeft)

        self.title_label = QtWidgets.QLabel("Generar Ruta de Envio")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        # Add layout
        header_layout.addWidget(self.title_label, 0, 1, 1, 2)
        header_layout.addWidget(logo_label, 0, 0)

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
        # self.table.itemSelectionChanged.connect(self.tableItemChanged)
        self.table.setSelectionMode(QtWidgets.QTableWidget.NoSelection)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Nombre", "Identificacion", "Ciudad", "Acciones"])
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(0, 240)

        # Add layout
        search_layout.addWidget(self.search_edit, 0, 0)
        search_layout.addWidget(self.search_button, 0, 1)
        search_layout.addWidget(self.search_button_update, 0, 2)
        search_layout.addWidget(self.table, 1, 0, 1, 3)

        #! Footer
        footer_layout = QtWidgets.QGridLayout()
        footer_label = QtWidgets.QLabel("Power By: Julian chingal")
        footer_label.setStyleSheet( """QLabel { 
                              color: #d3d3d3; 
                              font-size: 9px; 
                              padding: 3px; }""")
        footer_label.setAlignment(QtCore.Qt.AlignLeft)

        footer_layout.addWidget(footer_label, 0, 0)

        #! Main layout
        main_layout = QtWidgets.QGridLayout(self)
        main_layout.addLayout(header_layout, 0, 0, 1, 2)  # Encabezado ocupa dos columnas
        main_layout.addLayout(search_layout, 1, 0)
        main_layout.addLayout(footer_layout, 2, 0, 1,2)

        #! Styles
        self.apply_style()

        #! Events
        self.search_button.clicked.connect(self.search_client)
        self.search_edit.returnPressed.connect(self.search_client) 

    @QtCore.Slot()
    def edit_client(self, name):
        # Lógica para modificar clientes
        result = searchClientByName(name)
        editDialog = EditWindow(result, self)
        
        if editDialog.exec_() == QtWidgets.QDialog.Accepted:
            # Si se aceptan los cambios en la ventana emergente, puedes realizar alguna acción
            print("Cambios guardados")
        else:
            print("Edición cancelada")

    @QtCore.Slot()
    def print_client(self, name):
        # Lógica para modificar clientes
        result = searchClientByName(name)
        printDialog = PrintWindow(result, self)

        if printDialog.exec_() == QtWidgets.QDialog.Accepted:
            # Si se aceptan los cambios en la ventana emergente, puedes realizar alguna acción
            print("imprimiendo guardados")
        else:
            print("impresion cancelada")

    @QtCore.Slot()
    def search_client(self):
        # Lógica para buscar clientes
        search_text = self.search_edit.text()
        result = searchClientByName(search_text)
        if result:
            self.update_table(result)
        else:
            QtWidgets.QMessageBox.information(self, "Cliente no encontrado", "No se encontraron clientes con el nombre especificado.")
            self.search_edit.clear()

    def update_table(self, clients):
        # Limpiar contenido
        self.table.clearContents() 

        # Crear botones
        edit_button = QtWidgets.QPushButton()
        edit_button.setIcon(QtGui.QIcon("src/public/img/edit.png")) 
        edit_button.setIconSize(QtCore.QSize(24, 24))  
        edit_button.setFixedSize(30, 30)

        print_button = QtWidgets.QPushButton()  
        print_button.setIcon(QtGui.QIcon("src/public/img/print.png"))  
        print_button.setIconSize(QtCore.QSize(24, 24)) 
        print_button.setFixedSize(30, 30)

        # Configurar tamaño de la tabla 
        self.table.setRowCount(len(clients))
        
        for row, client in enumerate(clients):
            self.table.setItem(row, 0, QtWidgets.QTableWidgetItem(client["name"]))
            self.table.setItem(row, 1, QtWidgets.QTableWidgetItem(client["vat"]))
            self.table.setItem(row, 2, QtWidgets.QTableWidgetItem(client["city"]))

            # Crear botones
            edit_btn_clone = self.clone_button(edit_button)
            print_btn_clone = self.clone_button(print_button)
            
            widget_container = QtWidgets.QWidget() # Contenedor para los botones
            group_box = QtWidgets.QHBoxLayout(widget_container)
            group_box.setContentsMargins(0, 0, 0, 0) 
            group_box.setSpacing(0) 

            group_box.addWidget(edit_btn_clone)
            group_box.addWidget(print_btn_clone)
        
            self.table.setCellWidget(row, 3, widget_container)

            edit_btn_clone.clicked.connect(functools.partial(self.edit_client, client["name"]))
            print_btn_clone.clicked.connect(functools.partial(self.print_client, client["name"]))
    
    def clone_button(self, button):
        new_button = QtWidgets.QPushButton(button.text())
        new_button.setIcon(button.icon())
        new_button.setIconSize(button.iconSize())
        new_button.setFixedSize(button.size())
        new_button.clicked.connect(button.click)
        new_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 5px;
            }
            
            QPushButton:hover {
            background-color:  #FFFFFF;
            }
            """)
        return new_button

    def apply_style(self):
        # Estilo para los iconos
        QtWidgets.QApplication.setStyle("Fusion")

        # Estilo para los widgets
        label_style = """ 
            QLabel {
                color: #333333;  
                font-size: 16px;  
                font-family: sans-serif; 
                padding: 10px;
            }
        """
        widget_style = """
            QLabel {
                color: #333333;  /* Color del texto para los labels */
                font-size: 14px;  /* Tamaño de fuente */
                font-family: sans-serif;  /* Fuente */
            }

            QLineEdit{
                background-color: #f0f0f0;
                border: 1px solid gray;
                border-radius: 10px;
                padding: 7px;
                color: black;  /* Color del texto en QLineEdit */
            }

            QLineEdit:focus {
                border: 0.5px solid #118F31;
                background-color: #e0ffe0;  /* Color de fondo cuando tiene foco */
            }

            QPushButton {
                background-color: #118F31;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #45a049;
            }

            QTableWidget{
                background-color: #f0f0f0;
                border: 1px solid green;
                border-radius: 10px;
                color: black;
                padding: 4px;
            }

            QTableWidget::item:selected {
                background-color: #118F31;
                color: white;
            }
        """

        self.setStyleSheet(widget_style)

        # Labels
        self.title_label.setStyleSheet(label_style)
