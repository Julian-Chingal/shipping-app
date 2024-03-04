from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import json
import os

class printTemplate():
    def __init__(self, name, phone, address):
        self.name = name
        self.phone = phone
        self.address = address

        # Files Path
        current_path = os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
        self.path_pdf = os.path.join(current_path, "template", "template.pdf")
        self.fileJson = os.path.join(current_path, "Data", "company_config.json")
        self.image = os.path.join(current_path,"img", "logo.png")

        # Sheet size config
        self.half_letter = (letter[0], letter[1] / 2)
        pdfmetrics.registerFont(TTFont('BookAntiqua-Bold', 'ANTQUAB.TTF'))
        pdfmetrics.registerFont(TTFont('BookAntiqua', 'BKANT.ttf'))

    def extractCompanyInfo(self):
        with open(self.fileJson, "r") as archivo:
            companyInfo = json.load(archivo)
        return companyInfo

    def createTemplate(self,c):
        company = self.extractCompanyInfo()

        # Company Info
        c.drawString(70, 320, company["name"]) 
        c.drawString(70, 300, "Tel: " + company["phone"]) 
        c.drawString(70, 280, company["address"]) 
        c.drawString(70, 260, company["city"])

        # c.drawInlineImage(self.image, x=100, y=350, width=100, height=50, preserveAspectRatio=True)
        # c.rect(x=100, y=500, width=100, height=50, stroke=1, fill=0)

        c.line(70,250, 200,250)

        # Client Info
        c.setFont("BookAntiqua-Bold", 14) 
        c.drawString(300, 200, "Señor(a): ") 
        c.drawString(300, 150, "Telefono: ") 
        c.drawString(300, 100, "Dirección: ")

        c.setFont("BookAntiqua", 15) 
        c.drawString(300, 180, self.name) 
        c.drawString(300, 130, self.phone) 
        address_lines = self.address.splitlines()
        y_position = 80
        for line in address_lines:
            c.drawString(300, y_position, line)
            y_position -= 20  # Aj

    def saveTemplate(self):
        c = canvas.Canvas(self.path_pdf, pagesize=self.half_letter)
        c.setFont("BookAntiqua-Bold", 15)
        self.createTemplate(c)
        c.showPage()
        c.save()
        

pdf = printTemplate("juan Perez de la  communicacion olla S.A.S","1233516", "barrio paraiso \n Pepe perez")
pdf.saveTemplate()