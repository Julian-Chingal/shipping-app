from PySide2.QtPrintSupport import QPrintDialog, QPrinter
from PySide2  import QtGui 

from src.template.pdf_template import PrintTemplate

class PrintWindow:
    def __init__(self, client_info, parent = None):
        # super().__init__(parent)
        self.client = client_info
        self.path = "src/template/template.pdf"
        
        self.setup_ui()
        
    def setup_ui(self):
        pass

    def GeneratePDF(self):
        client = self.client[0]
        attributes = ["name", "vat", "phone", "street", "city", "state_id"]

        data = {}
        for attr in attributes:
            value = client.get(attr)
            data[attr] = value if value is not False else "None"

        pdf = PrintTemplate(data)
        pdf.save() # Save the pdf file in the path
    