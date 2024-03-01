from pdfdocument.document import PDFDocument

def create_pdf(template_path, output_path, var1, var2, var3):
    pdf = PDFDocument(output_path)
    pdf.init_report()
    pdf.h2('Título de tu documento')

    # Aquí puedes agregar tus variables al documento
    pdf.p(f'Variable 1: {var1}')
    pdf.p(f'Variable 2: {var2}')
    pdf.p(f'Variable 3: {var3}')

    pdf.generate()

# Luego puedes llamar a la función con tus variables
create_pdf('ruta/a/tu/plantilla', 'ruta/a/tu/salida', 'valor1', 'valor2', 'valor3')
