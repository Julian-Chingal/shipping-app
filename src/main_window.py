# -*- coding: utf-8 -*-
# MyApp.py

"""
MyApp - Una aplicación para generar plantillas de despacho de clientes.

Este programa proporciona una interfaz gráfica de usuario (GUI) para buscar clientes,
editar sus detalles y generar plantillas de despacho de clientes en formato PDF.
"""
from src.dataFile import findClient, readData
from src.template.templatePDF import printTemplate
import tkinter as tk
from tkinter import ttk, messagebox,Tk
import subprocess
import os

class MyApp:
    def __init__(self, root:Tk):
        self.root = root
        self.root.resizable(False, False)
        self.root.title('Generador Guias de Despacho')
        self.root.option_add('*tearOff', False)
        self.root.iconbitmap(os.path.join("src","img","icon.ico"))
        # Style 
        self.style = ttk.Style(self.root)

        self.root.tk.call('source', 'theme/forest-dark.tcl')
        self.root.tk.call('source', 'theme/forest-light.tcl')

        self.style.theme_use('forest-light')

        # Make the self.root responsive
        self.root.columnconfigure(index=0, weight=1)
        self.root.rowconfigure(index=0, weight=0)

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)

        # Init UI
        self.setup_ui()
    
    def setup_ui(self):
        # Header Frame -----------------------------------------------------------------------------------------
        self.header_frame = ttk.Frame(self.main_frame, padding=(10,5))
        self.header_frame.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(10, 5), sticky="nsew")

        self.label_title = ttk.Label(self.header_frame, text="Generador Plantilla Despacho de Clientes", font=('',15))
        self.label_title.grid(row=0,column=0,padx=0,pady=(10,20), sticky="w")

        self.change_theme = ttk.Checkbutton(self.header_frame, text="Tema", style="Switch", command=self.changeTheme)
        # self.change_theme.grid(row=1,column=0, padx=0, pady=(0,10), sticky="se")

        # Search Frame -----------------------------------------------------------------------------------------
        self.search_frame = ttk.LabelFrame(self.main_frame, text="Busqueda Cliente", padding=(10,10))
        self.search_frame.grid(row=1, column=0, padx=(5, 5), pady=(0, 10), sticky="nsew")

        # Search Frame
        self.search_frame.columnconfigure(0, weight=1)  # Ajustar la primera columna al centro
        self.search_frame.columnconfigure(1, weight=0)  # Mantener el ancho fijo del botón
        self.search_frame.columnconfigure(2, weight=0)  # Mantener el ancho fijo del botón

        # Entry
        self.findEntry = ttk.Entry(self.search_frame)
        # self.findEntry.insert(0, "Escriba un Nombre")
        self.findEntry.grid(row=0,column=0, padx=(0,5), pady=(0,10), sticky="ew")

        # Button
        self.btn_search = ttk.Button(self.search_frame, text="Buscar", style="Accent.TButton", command=self.showClient)
        self.btn_search.grid(row=0, column=1, padx=(0,5), pady=(0,10), sticky="nsew" )

        self.btn_add = ttk.Button(self.search_frame, text="Editar", state="disabled", command=self.inserClient)
        self.btn_add.grid(row=0, column=2, padx=(0,5), pady=(0,10), sticky="nsew")

        #Tree
        self.tree_clients = ttk.Treeview(self.search_frame, columns=('Nombre', 'Telefono', 'Direccion'), show='headings')
        self.tree_clients.heading('Nombre', text="Nombre")
        self.tree_clients.heading('Telefono', text="Telefono")
        self.tree_clients.heading('Direccion', text="Direccion")
        self.tree_clients.grid(row=1, column=0, columnspan=3, padx=(5,0), pady=(10,0), sticky="nsew")

        # Template Frame -----------------------------------------------------------------------------------------
        self.template_frame = ttk.LabelFrame(self.main_frame, text="Plantilla", padding=(10,10))
        self.template_frame.grid(row=1, column=1, padx=(10, 5), pady=(0, 10), sticky="nsew")


        # Template Frame
        self.template_frame.columnconfigure(0, weight=1)  # Ajustar la primera columna al centro
        self.template_frame.rowconfigure((0, 2, 4), weight=0)  # Mantener el alto fijo de las etiquetas
        self.template_frame.rowconfigure((1, 3, 5), weight=0)  # Mantener el alto fijo de las entradas
        self.template_frame.rowconfigure(6, weight=0)  # Mantener el alto fijo del botón

        # Name
        self.label_name = ttk.Label(self.template_frame, text="Nombre del Cliente")
        self.label_name.grid(row=0, column=0, padx=3, pady=(0,1), sticky="w")

        self.entry_name_info = ttk.Entry(self.template_frame)
        self.entry_name_info.grid(row=1, column=0, padx=5, pady=(0,10), sticky="ew")

        # Phone
        self.label_phone = ttk.Label(self.template_frame, text="Telefono del Cliente")
        self.label_phone.grid(row=2, column=0, padx=3, pady=(0,1), sticky="w")

        self.entry_phone_info = ttk.Entry(self.template_frame)
        self.entry_phone_info.grid(row=3, column=0, padx=5, pady=(0,10), sticky="ew")

        # Address
        self.label_address = ttk.Label(self.template_frame, text="Direccion del Cliente")
        self.label_address.grid(row=4, column=0, padx=3, pady=(0,1), sticky="w")

        self.txt_address_info = tk.Text(self.template_frame, height=6, width= 7 ,wrap='word')
        self.txt_address_info.grid(row=5, column=0, padx=6, pady=(0,20), sticky="ew")

        # Button
        self.btn_impr = ttk.Button(self.template_frame, text="Imprimir",state="disabled", command=self.printGuide, style="Accent.TButton")
        self.btn_impr.grid(row=6, column=0 , padx=5, pady=(0,10), sticky="nsew")

        # Footer Frame -----------------------------------------------------------------------------------------
        self.footer_frame = ttk.Frame(self.main_frame, padding=(10,5))
        self.footer_frame.grid(row=2, column=0, columnspan=2, padx=(5, 5), pady=(5, 5), sticky="nsew")

        self.label_signature = ttk.Label(self.footer_frame, text="Desarrollado por: Julian Chingal", font=('',10), foreground="gray")
        self.label_signature.grid(row=0,column=0,padx=0,pady=(2,0), sticky="e")

        # Configurar el envasado de los frames
        self.root.pack_propagate(False)
        self.main_frame.pack_propagate(False)
        # self.center_window()

    def center_window(self):
        self.root.update()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
        x_cordinate = int((self.root.winfo_screenwidth()/2) - (self.root.winfo_width()/2))
        y_cordinate = int((self.root.winfo_screenheight()/2) - (self.root.winfo_height()/2))
        self.root.geometry("+{}+{}".format(x_cordinate, y_cordinate))

    def showClient(self):
        client = self.findEntry.get()
        suggestion = findClient(client)
        
        if not client:
            self.showAllClient()
            return

        if not suggestion:
            messagebox.showinfo('Error', 'Cliente no encontrado')
            self.findEntry.delete(0, 'end') #Limpiar casilla de busqueda
            self.btn_add.config(state="disabled")
            self.btn_impr.config(state="disabled")

        else:
            self.tree_clients.delete(*self.tree_clients.get_children())
            for info in suggestion:
                self.tree_clients.insert('','end', values=info)
            
            self.btn_add.config(state="normal")
         
    def showAllClient(self):
        data = readData()
        self.tree_clients.delete(*self.tree_clients.get_children()) #Limpiar antes de poner informacion
        for info in data:
            self.tree_clients.insert('', 'end', values=info)

    def inserClient(self):
        select = self.tree_clients.selection()
        
        # Clear boxes
        self.entry_name_info.delete(0, 'end')
        self.entry_phone_info.delete(0, 'end')
        self.txt_address_info.delete(1.0, 'end')

        if select:
            item = self.tree_clients.item(select)
            values = item['values']
            self.entry_name_info.insert(0, values[0])
            self.entry_phone_info.insert(0, values[1])
            self.txt_address_info.insert(1.0, values[2])
            self.btn_impr.config(state="normal")

    def printGuide(self):
        name = self.entry_name_info.get()
        phone = self.entry_phone_info.get()
        address = self.txt_address_info.get("1.0", tk.END).strip() 

        pdf = printTemplate(name, phone, address )
        pdf.saveTemplate()
        path = pdf.path_pdf
        messagebox.showinfo('Success', 'PDF Generado Exitosamente')
        subprocess.Popen([path], shell=True)

    def changeTheme(self):
        currentTheme = self.style.theme_use()    
        if currentTheme == 'forest-light':
            self.style.theme_use('forest-dark')
            self.root.config(bg="#313131")
        else:
            self.style.theme_use('forest-light')
            self.root.config(bg="#ffffff")