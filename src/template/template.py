from reportlab.pdfgen import canvas
from fpdf import FPDF
import sys, os, json, datetime, textwrap

class PrintTemplate():
    def __init__(self, name, id_client, phone, address, city):
        self.name = name
        self.id_client = id_client
        self.phone = phone
        self.address = address
        self.city = city

        # Ruta de archivos
        current_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), "..\\..")))
        self.path_pdf = os.path.join(current_path, "src", "template", "template.pdf")
        self.fileJson = os.path.join(current_path, "src", "data", "company_config.json")
        self.image = os.path.join(current_path, "src", "img", "logo.png") 

    def extract_company_info(self):
        with open(self.fileJson, "r") as archivo:
            company_info = json.load(archivo)
        return company_info

    def header(self, pdf):
        pdf.image("src/public/logo.png", 7, 8, 48, 14)
        pdf.set_font('Helvetica', 'B', 16)
        pdf.set_xy(150, 5)
        pdf.set_text_color(220, 220, 220)
        pdf.cell(text= "Fecha",align = 'R')
        pdf.ln(20)


    def create_template(self, pdf):
        company = self.extract_company_info()
        self.header(pdf)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(text = "Remitente:", align = 'L')
        pdf.ln(8)

        # Remitente
        pdf.set_font('helvetica', '', 15)
        pdf.cell(text = company["name"], align = 'L')
        pdf.ln(6)
        pdf.cell(text = "Tel: " + company["phone"], align = 'L')
        pdf.ln(6)
        pdf.cell(text = company["address"], align = 'L')
        pdf.ln(6)
        pdf.cell(text = company["city"], align = 'L')
        pdf.ln(10)

        # Destinatario
        pdf.set_x(80)
        pdf.set_font('helvetica', 'B', 15)
        pdf.cell(text = "Destinatario:",new_x= "LEFT", new_y = "NEXT", align = 'L')
        pdf.set_font('helvetica', '', 15)
        pdf.multi_cell(0, text=self.ajustar_texto(self.name, 40),new_x= "LEFT",new_y = "NEXT", align='L')

        pdf.set_font('helvetica', 'B', 15)
        pdf.cell(text = "Identificacion:", new_x= "LEFT",new_y = "NEXT", align = 'L')
        pdf.set_font('helvetica', '', 15)
        pdf.cell(text = self.id_client, new_x= "LEFT",new_y = "NEXT", align = 'L')

        pdf.set_font('helvetica', 'B', 15)
        pdf.cell(text = "Telefono:", new_x= "LEFT",new_y = "NEXT", align = 'L')
        pdf.set_font('helvetica', '', 15)
        pdf.cell(text = self.phone, new_x= "LEFT",new_y = "NEXT", align = 'L')

        pdf.set_font('helvetica', 'B', 15)
        pdf.cell(text = "Direccion:", new_x= "LEFT",new_y = "NEXT", align = 'L')
        pdf.set_font('helvetica', '', 15)
        pdf.multi_cell(0, text=self.ajustar_texto(self.address, 40),new_x= "LEFT",new_y = "NEXT", align='L')

    def ajustar_texto(self, text, max_width):
        wrapper = textwrap.TextWrapper(width= max_width)
        wrapped_text = wrapper.fill(text)
        return wrapped_text

    def save(self):
        pdf = FPDF(orientation= 'p', unit= 'mm', format= 'A4')
        pdf.set_font('helvetica', 'B', 15)
        pdf.add_page()
        self.create_template(pdf)
        pdf.output(self.path_pdf)

# pdf = PrintTemplate("ATINA ENERGY SERVICES CORP SUCURSAL COLOMBIA","1233516", "3220215569","Barrio Paraiso  Pepe perez", "BOGOTA")
# # pdf = PrintTemplate("SUCURSAL COLOMBIA","1233516", "3220215569","Barrio Paraiso  Pepe perez", "BOGOTA")
# pdf.save()