from PySide2 import QtWidgets, QtCore
from src.template.pdf_template import PrintTemplate

class EditWindow(QtWidgets.QDialog):
    def __init__(self, client_info, parent = None):
        super().__init__(parent)

        self.client = client_info

        self.setWindowTitle("Editar cliente")
        self.main_layout = QtWidgets.QGridLayout()
        self.setLayout(self.main_layout)
        self.resize(400, 300)

        self.setup_ui()

    def setup_ui(self):     
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
        self.main_layout.addWidget(address_label,7 ,0)
        self.main_layout.addWidget(self.address_edit, 8, 0, 1, 2)


        self.main_layout.addWidget(save_button, 9, 0)
        self.main_layout.addWidget(cancel_button, 9, 1)

        #* Styles
        self.styles()
        self.update_fields()

        #* Events
        save_button.clicked.connect(self.save_changes)
        cancel_button.clicked.connect(self.reject)

    def update_fields(self):
        #fill fields
        client = self.client[0]
        attributes = ["name", "vat", "phone", "street", "city", "state_id"]

        for attr in attributes:
            value = client.get(attr)
            if value is False:
                setattr(self, attr, "")
            else:
                setattr(self, attr, value)

        self.name_edit.setText(self.name)
        self.id_edit.setText(self.vat)
        self.phone_edit.setText(self.phone)
        self.city_edit.setText(self.city)
        self.state_edit.setText(self.state_id[1])
        self.address_edit.setText(self.street)

    def save_changes(self):
        pdf = PrintTemplate(self.name_edit.text(), self.id_edit.text(), self.phone_edit.text(), self.address_edit.toPlainText(), self.city_edit.text(), self.state_edit.text())
        if pdf:
            QtWidgets.QMessageBox.information(self, "Cliente editado", "Imprimiendo guia de envio")
            pdf.save()
            self.accept()
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Ha ocurrido un error al imprimir la guia")

    def styles(self):
        title_style = """
            QLabel {
                    color: #333333;  
                    font-size: 17px;  
                    font-family: sans-serif; 
                    padding: 10px;
                }
        """
                # 

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

        """

        self.setStyleSheet(style)

        self.title_label.setStyleSheet(title_style)