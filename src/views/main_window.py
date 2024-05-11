from PySide2 import QtCore, QtWidgets, QtGui
import functools, sys, os

from src.data.get_info import searchClientByName
from src.views.edit_window import EditWindow
from src.data.update_info import  UpdateInfo
from src.data.update_app import UpdateApp
from src.views.print_window import PrintWindow


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), "..\\."))) # Obtener la ruta principal del proyecto
        self.setup_ui()
    
    def setup_ui(self):
        #* ToolBar
        self.toolbar = QtWidgets.QToolBar()
        self.toolbar.setFixedHeight(25)
        self.toolbar.setMovable(False) 
                                               
        archivo_menu = QtWidgets.QMenu("Archivo", self)
        # archivo_menu.addAction("Actualizar", self.update_app)
        archivo_menu.addAction("Acerca de", )

        archivo_button = QtWidgets.QToolButton(self)
        archivo_button.setText("Archivo")
        archivo_button.setMenu(archivo_menu)  # Asignar el menú al botón
        archivo_button.setPopupMode(QtWidgets.QToolButton.InstantPopup)  # Mostrar el menú instantáneamente al hacer clic

        self.toolbar.addWidget(archivo_button)  

        #* Layouts
        self.header_layout = QtWidgets.QGridLayout()  # Header layout
        self.search_layout = QtWidgets.QGridLayout() # Search layout
        self.footer_layout = QtWidgets.QGridLayout() # Footer layout

        #* Central Widget
        self.ui() # Crear la interfaz de usuario
        central_widget = QtWidgets.QWidget(self) # Crear un widget central
        central_layout = QtWidgets.QGridLayout(central_widget) # Crear un layout para el widget central
        central_layout.addLayout(self.header_layout, 0, 0) # Agregar los layouts al widget central
        central_layout.addLayout(self.search_layout, 1, 0)
        central_layout.addLayout(self.footer_layout, 2, 0)

        self.addToolBar(self.toolbar)
        self.setCentralWidget(central_widget)

        #* Styles
        self.apply_style()

        #* Events
        self.search_button.clicked.connect(self.search_client)
        self.search_edit.returnPressed.connect(self.search_client) 
        self.search_button_update.clicked.connect(self.update_info)

    def ui(self):
        #! Header
        logo_label = QtWidgets.QLabel()
        logo_label.setPixmap(QtGui.QPixmap(os.path.join(self.path, "public", "img", "logo.png")))  # Ruta a la imagen del logo
        logo_label.setAlignment(QtCore.Qt.AlignLeft)

        self.title_label = QtWidgets.QLabel("Generar Ruta de Envio")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        # Add layout
        self.header_layout.addWidget(self.title_label, 0, 1, 1, 2)
        self.header_layout.addWidget(logo_label, 0, 0)

        #! Serach
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
        self.search_layout.addWidget(self.search_edit, 0, 0)
        self.search_layout.addWidget(self.search_button, 0, 1)
        self.search_layout.addWidget(self.search_button_update, 0, 2)
        self.search_layout.addWidget(self.table, 1, 0, 1, 3)

        #! Footer
        footer_label = QtWidgets.QLabel("Power By: Julian chingal")
        footer_label.setStyleSheet( """QLabel { 
                              color: #d3d3d3; 
                              font-size: 9px; 
                              padding: 3px; }""")
        footer_label.setAlignment(QtCore.Qt.AlignLeft)

        self.footer_layout.addWidget(footer_label, 0, 0)

    @QtCore.Slot()
    def edit_client(self, name):

        result = searchClientByName(name)
        editDialog = EditWindow(result, self)
        
        if editDialog.exec_() == QtWidgets.QDialog.Accepted:

            print("Cambios guardados")
        else:
            print("Edición cancelada")

    @QtCore.Slot()
    def print_client(self, name):

        result = searchClientByName(name)
        PrintWindow(result, self)
        # printDialog = PrintWindow(result, self)

        # if printDialog.exec_() == QtWidgets.QDialog.Accepted:

        #     print("imprimiendo guardados")
        # else:
        #     print("impresion cancelada")

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

    def update_info(self):

        if UpdateInfo():
             QtWidgets.QMessageBox.information(self, "Actualizando", "Se ha actualizado la informacion")
        else:
            QtWidgets.QMessageBox.warning(self, "Actualizando", "Se ha actualizado la informacion")

    def update_table(self, clients):
        # Limpiar contenido
        self.table.clearContents() 

        # Crear botones
        edit_button = QtWidgets.QPushButton()
        edit_button.setIcon(QtGui.QIcon(os.path.join(self.path, "public", "img", "_edit.png"))) 
        edit_button.setIconSize(QtCore.QSize(24, 24))  
        edit_button.setFixedSize(30, 30)

        print_button = QtWidgets.QPushButton()  
        print_button.setIcon(QtGui.QIcon(os.path.join(self.path, "public", "img","print.png")))  
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
            # group_box.addWidget(print_btn_clone)
        
            self.table.setCellWidget(row, 3, widget_container)

            edit_btn_clone.clicked.connect(functools.partial(self.edit_client, client["name"]))
            print_btn_clone.clicked.connect(functools.partial(self.print_client, client["name"]))
    
    def update_app(self):
        path_app = sys.executable
        UpdateApp(path_app)

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
                background-color: #E8E8E8;
                border: 1px solid #A9A9A9;
            }
            
            QPushButton:pressed {
                background-color: #DCDCDC;
                border: 1px solid #A9A9A9;
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
            QMainWindow {
                background-color: white
            }
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
                width: 80px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #45a049;
            }

            QTableWidget{
                background-color: white;
                border: 1px solid green;
                border-radius: 10px;
                color: black;
                padding: 4px;
            }

            QTableWidget::item:selected {
                background-color: #118F31;
                color: white;
            }

            QToolBar {
                background-color: #f3f3f3; 
                border: none;
            }

            QMenu {
                color: black;
            }

            QMenu::item:selected {
                background-color: #118F31;
                color: white;
            }

            QToolButton {
                color: black;
                border: none;
                width: 80px;
                height: 100%;
            }
            QToolButton:hover {
                background-color: #45a049;
                color: white;
            }
            QToolButton:pressed {
                background-color: gray;
            }

        """

        self.setStyleSheet(widget_style)
        # Labels
        self.title_label.setStyleSheet(label_style)