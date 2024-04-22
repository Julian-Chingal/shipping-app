from PySide2 import QtWidgets, QtCore, QtGui
from src.template.pdf_template import PrintTemplate

class EditWindow(QtWidgets.QDialog):
    def __init__(self, client_info, parent = None):
        super().__init__(parent)

        self.client = client_info # Informacion del cliente

        self.setWindowTitle("Editar cliente") # Titulo de la ventana
        self.main_layout = QtWidgets.QGridLayout() # Layout de la ventana
        self.setLayout(self.main_layout) # Asignar el layout a la ventana
        self.resize(400, 300) # Tamaño de la ventana

        self.setup_ui() # Llamar al metodo para crear la interfaz

    def setup_ui(self): # Crear la interfaz de la ventana
        #* Dialog   
        #Title
        self.title_label =  QtWidgets.QLabel("Editar cliente")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)

        #* Inputs
        name_label = QtWidgets.QLabel("Nombre:")
        self.name_edit = QtWidgets.QLineEdit()

        id_label = QtWidgets.QLabel("Identificacion:")
        self.id_edit = QtWidgets.QLineEdit()

        phone_label = QtWidgets.QLabel("Telefono:")
        self.phone_edit = QtWidgets.QLineEdit()

        city_label = QtWidgets.QLabel("Ciudad:")
        self.city_edit = QtWidgets.QLineEdit()

        state_label = QtWidgets.QLabel("Departamento:")
        self.state_edit = QtWidgets.QLineEdit()

        address_label = QtWidgets.QLabel("Direccion:")
        self.address_edit = QtWidgets.QTextEdit()

        #* Checkbox
        self.check_box = QtWidgets.QCheckBox("Recoge en oficina?")
        self.check_box.setChecked(False)
        self.check_box.stateChanged.connect(self.toggle_office_text)

        # Botones
        save_button = QtWidgets.QPushButton("Imprimir")
        cancel_button = QtWidgets.QPushButton("Cancelar")

        #* Add to layout
        self.main_layout.addWidget(self.title_label,0 ,0, 1, 2)
        self.main_layout.addWidget(name_label,1 ,0)
        self.main_layout.addWidget(self.name_edit,2 ,0)

        self.main_layout.addWidget(id_label, 1,1)
        self.main_layout.addWidget(self.id_edit, 2, 1)

        self.main_layout.addWidget(phone_label, 3,0,)
        self.main_layout.addWidget(self.phone_edit,4 ,0)

        self.main_layout.addWidget(city_label, 3,1)
        self.main_layout.addWidget(self.city_edit, 4, 1)

        self.main_layout.addWidget(state_label,5 ,0)
        self.main_layout.addWidget(self.state_edit,6 ,0)
        self.main_layout.addWidget(self.check_box, 6, 1)
        self.main_layout.addWidget(address_label,7 ,0)
        self.main_layout.addWidget(self.address_edit, 8, 0, 1, 2)

        # Agregar al main layout
        self.main_layout.addWidget(save_button, 9, 0)
        self.main_layout.addWidget(cancel_button, 9, 1)

        #* Styles
        self.styles()
        self.update_fields()

        #* Events
        save_button.clicked.connect(self.save_changes)
        cancel_button.clicked.connect(self.reject)

    def update_fields(self): # Actualizar los campos con la informacion del cliente
        #fill fields
        client = self.client[0]
        attributes = ["name", "vat", "phone", "street", "city", "state_id"]

        for attr in attributes: # Verificar si el valor es False
            value = client.get(attr)
            if value is False:
                setattr(self, attr, "None")
            else:
                setattr(self, attr, value)

        # agregar la informacion a los campos
        self.name_edit.setText(self.name)
        self.id_edit.setText(self.vat)
        self.phone_edit.setText(self.phone)
        self.city_edit.setText(self.city)
        self.state_edit.setText(self.state_id[1])
        self.address_edit.setText(self.street)

    def save_changes(self): # Guardar los cambios en un pdf
        data = {
            "name": self.name_edit.text(),
            "id": self.id_edit.text(),
            "phone": self.phone_edit.text(),
            "city": self.city_edit.text(),
            "state": self.state_edit.text(),
            "address": self.address_edit.toPlainText()
        }
        
        pdf = PrintTemplate(data)
        
        if pdf:
            alert = QtWidgets.QMessageBox(self)  # Alerta de impresion
            alert.setIcon(QtWidgets.QMessageBox.Information)
            alert.setWindowTitle("Cliente editado")
            alert.setText("Imprimiendo guia de envio")
            alert.setStandardButtons(QtWidgets.QMessageBox.Ok)

            QtCore.QTimer.singleShot(2000, alert.accept)
            alert.exec_()

            pdf.save()
            # self.accept()
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Ha ocurrido un error al imprimir la guia")

    def toggle_office_text(self, state): # Mostrar u ocultar el texto de recoge en oficina
        if state == QtCore.Qt.Checked:
            self.address_edit.append("EL CLIENTE RECOGE EN OFICINA")
        else:
            cursor = self.address_edit.textCursor()
            cursor.movePosition(QtGui.QTextCursor.End)
            cursor.select(QtGui.QTextCursor.LineUnderCursor)
            cursor.removeSelectedText()

    def styles(self): # Estilos de la ventana
        title_style = """
            QLabel {
                    color: #333333;  
                    font-size: 17px;  
                    font-family: sans-serif; 
                    padding: 10px;
                }
        """
        style = """
      
            QLabel {
                    color: #333333;  
                    font-size: 12px;  
                    font-family: sans-serif; 
                    padding: 5px;
                }
            
            QTextEdit{
                background-color: #f0f0f0;
                border: 1px solid gray;
                border-radius: 5px;
                padding: 7px;
                color: black; 
            }

            QTextEdit:focus {
                border: 0.5px solid #118F31;
                background-color: #e0ffe0; 
            }

          QCheckBox {
                color: #333333;
                font-size: 12px;
                font-family: sans-serif;
                padding: 5px;
            }

            QCheckBox::indicator {
                background-color: #FFFFFF;  /* Color de fondo predeterminado */
                border: 1px solid #CCCCCC;  /* Borde predeterminado */
                width: 16px;  /* Ancho del indicador ajustado */
                height: 16px;  /* Altura del indicador ajustada */
            }

            QCheckBox::indicator:checked {
                background-color: #118F31;  /* Color de fondo cuando se selecciona */
                border: 1px solid #118F31;  /* Borde cuando se selecciona */
                /* Efecto de sombra para resaltar cuando está seleccionado */
                box-shadow: 0 0 2px rgba(0, 0, 0, 0.5);  /* Ajusta la sombra según lo desees */
            }
        """

        self.setStyleSheet(style)

        self.check_box.setStyleSheet(style)
        self.title_label.setStyleSheet(title_style)