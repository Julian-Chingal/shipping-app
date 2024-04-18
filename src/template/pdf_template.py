from fpdf import FPDF
from io import BytesIO
import sys, os, json, datetime, textwrap, subprocess

class PrintTemplate():
    def __init__(self, data):
        self.name = data.get("name", "None ")
        self.id_client = data.get("id", "None ")
        self.phone = data.get("phone", "None ")
        self.address = data.get("address", "None ")
        self.city = data.get("city", "None ")
        self.state = data.get("state", "None ")

        # Ruta de archivos
        current_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), "..\\..")))
        self.path_pdf = os.path.join(current_path, "src", "template", "template.pdf")
        self.fileJson = os.path.join(current_path, "src", "data", "company_config.json")
        self.image = os.path.join(current_path, "src", "public", "img", "logo.png") 

    def extract_company_info(self):
        with open(self.fileJson, "r") as archivo:
            company_info = json.load(archivo)
        return company_info

    def header(self, pdf):
        pdf.image("src/public/img/logo.png", 7, 8, 48, 14)
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
        pdf.cell(text=self.phone, new_x="LEFT", new_y="NEXT", align='L')

        pdf.set_font('helvetica', 'B', 15)
        pdf.cell(text = "Ciudad:", new_x= "LEFT",new_y = "NEXT", align = 'L')
        pdf.set_font('helvetica', '', 15)
        pdf.multi_cell(0, text=self.ajustar_texto(self.city + " - "+  self.state , 40),new_x= "LEFT",new_y = "NEXT", align='L')

        pdf.set_font('helvetica', 'B', 15)
        pdf.cell(text = "Direccion:", new_x= "LEFT",new_y = "NEXT", align = 'L')
        pdf.set_font('helvetica', '', 15)
        # pdf.multi_cell(0, text=self.ajustar_texto(self.address, 25),new_x= "LEFT",new_y = "NEXT", align='L')

        address_lines = self.address.split('\n')
        for line in address_lines:
            if line.strip(): 
                pdf.multi_cell(0, text=self.ajustar_texto(line, 30),new_x= "LEFT",new_y = "NEXT", align='L')


    def ajustar_texto(self, text, max_width):
        wrapper = textwrap.TextWrapper(width= max_width)
        wrapped_text = wrapper.fill(text)
        return wrapped_text

    def save(self):
        pdf = FPDF(orientation= 'p', unit= 'mm', format= 'A4')
        pdf.set_font('helvetica', 'B', 15)
        pdf.add_page()
        self.create_template(pdf)
        # pdf_output = BytesIO()
        pdf.output(self.path_pdf) # Save the pdf in the buffer o path
        # pdf.output(pdf_output) # Save the pdf in the buffer o path
        # pdf_output.seek(0)
        # return pdf_output.getvalue()
        subprocess.Popen([self.path_pdf], shell=True) #por ahora se abre directamente el pdf


# data = {
#             "name": "ATINA ENERGY SERVICES CORP SUCURSAL COLOMBIA",
#             "id": "1233516",
#             "phone": "3220215569",
#             "city":  "BOGOTA",
#             "state":  "BOGOTA",
#             "address": "Barrio Paraiso  Pepe perez"
#         }

# pdf = PrintTemplate(data)
# # pdf = PrintTemplate("SUCURSAL COLOMBIA","1233516", "3220215569","Barrio Paraiso  Pepe perez", "BOGOTA")
# pdf.save()