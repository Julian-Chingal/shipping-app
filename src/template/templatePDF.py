from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import json
import os, sys

class printTemplate():
    def __init__(self, name, phone, address, city):
        self.name = name
        self.phone = phone
        self.address = address
        self.city = city

        # Files Path
        current_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), "..\\..")))
        print(current_path)
        self.path_pdf = os.path.join(current_path,"src", "template", "template.pdf")
        self.fileJson = os.path.join(current_path, "src", "data", "company_config.json")
        self.image = os.path.join(current_path, "src", "img", "logo.png")

        # self.path_pdf = os.path.join("src/template/template.pdf")
        # self.fileJson = os.path.join("src/data/company_config.json")
        # self.image = os.path.join("src/img/logo.png")

        # Sheet size config
        self.half_letter = letter
        pdfmetrics.registerFont(TTFont('BookAntiqua-Bold', 'ANTQUAB.TTF'))
        pdfmetrics.registerFont(TTFont('BookAntiqua', 'BKANT.ttf'))

    def extractCompanyInfo(self):
        with open(self.fileJson, "r") as archivo:
            companyInfo = json.load(archivo)
        return companyInfo

    def createTemplate(self,c):
        company = self.extractCompanyInfo()

        # Company Info
        c.drawString(60, 750, "Remitente:")
        c.line(60,747, 150,747)
        c.drawString(60, 730, company["name"]) 
        c.drawString(60, 710, "Tel: " + company["phone"]) 
        c.drawString(60, 690, company["address"]) 
        c.drawString(60, 670, company["city"])

        # c.drawInlineImage(self.image, x=100, y=350, width=100, height=50, preserveAspectRatio=True)
        # c.rect(x=100, y=500, width=100, height=50, stroke=1, fill=0)

        c.line(70,665, 200, 665)

        # Client Info
        c.setFont("BookAntiqua-Bold", 14) 
        c.drawString(250, 620, "Señor(a): ") 
        c.drawString(250, 583, "Identificacion: ") 
        c.drawString(250, 546, "Telefono: ") 
        c.drawString(250, 509, "Dirección: ")

        c.setFont("BookAntiqua", 15) 
        c.drawString(250, 603, self.name) 
        c.drawString(250, 566, "117551679")
        c.drawString(250, 529, self.phone) 
        c.drawString(250, 493, self.city)
        address_lines = self.address.splitlines()
        y_position = 477
        for line in address_lines:
            c.drawString(250, y_position, line)
            y_position -= 20  # Aj

    def createTemplatePick(self,c):
        company = self.extractCompanyInfo()

        # Company Info
        c.drawString(60, 750, "Remitente:")
        c.line(60,747, 150,747)
        c.drawString(60, 730, company["name"]) 
        c.drawString(60, 710, "Tel: " + company["phone"]) 
        c.drawString(60, 690, company["address"]) 
        c.drawString(60, 670, company["city"])

        # c.drawInlineImage(self.image, x=100, y=350, width=100, height=50, preserveAspectRatio=True)
        # c.rect(x=100, y=500, width=100, height=50, stroke=1, fill=0)

        c.line(70,665, 200, 665)

        # Client Info
        c.setFont("BookAntiqua-Bold", 14) 
        c.drawString(250, 620, "Señor(a): ") 
        c.drawString(250, 583, "Identificacion: ") 
        c.drawString(250, 546, "Telefono: ") 
        c.drawString(250, 509, "Dirección: ")

        c.setFont("BookAntiqua", 15) 
        c.drawString(250, 603, self.name) 
        c.drawString(250, 566, "117551679")
        c.drawString(250, 529, self.phone) 
        c.drawString(250, 493, "EL CLIENTE RECIBE EN OFICINA")
        c.drawString(250, 476, self.city)

    def saveTemplate(self, sel):
        c = canvas.Canvas(self.path_pdf, pagesize=self.half_letter)
        c.setFont("BookAntiqua-Bold", 15)
        if sel == True:
            self.createTemplatePick(c)
        else:
            self.createTemplate(c)
        c.showPage()
        c.save()
        

# pdf = printTemplate("juan Perez de la  communicacion olla S.A.S","1233516", "Barrio Paraiso \n Pepe perez", "BOGOTA")
# pdf.saveTemplate("N")