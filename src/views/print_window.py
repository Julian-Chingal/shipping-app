from PySide2 import QtWidgets, QtPrintSupport
from src.template.pdf_template import PrintTemplate

class PrintWindow(QtPrintSupport.QPrintDialog):
    def __init__(self, client_info, parent = None):
        super().__init__(parent)

        self.client = client_info
        
        self.path = "src/template/template.pdf"
        
        
        # self.GeneratePDF()
        self.setup_ui()
        
    def setup_ui(self):
        self.print = self.printer()
        self.print.setOutputFileName(self.path)
        self.print_dialog = QtPrintSupport.QPrintDialog(self.print)

        if self.print_dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.GeneratePDF()
            self.accept()
        else:
            self.reject()
        


    def GeneratePDF(self):
        client = self.client[0]
        attributes = ["name", "vat", "phone", "street", "city", "state_id"]

        for attr in attributes:
            value = client.get(attr)
            if value is False:
                setattr(self, attr, "")
            else:
                setattr(self, attr, value)
        
        pdf = PrintTemplate(self.name, self.vat, self.phone, self.street, self.city, self.state_id[1])
        pdf.save()
    