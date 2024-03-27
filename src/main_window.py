# -*- coding: utf-8 -*-
# MyApp.py

"""
MyApp - Una aplicación para generar plantillas de despacho de clientes.

Este programa proporciona una interfaz gráfica de usuario (GUI) para buscar clientes,
editar sus detalles y generar plantillas de despacho de clientes en formato PDF.
"""
from src.dataFile import findClient, readData
from src.template.templatePDF import printTemplate
from src.get_info import updateInfo
import tkinter as tk
from tkinter import ttk, messagebox,Tk
import subprocess
import os

class MyApp:
    def __init__(self, root:Tk):
        self.root = root
        self.root.resizable(False, False)
        self.root.title('Guias de Despacho')
        self.root.option_add('*tearOff', False)
        img_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "img", "icon.ico")
        self.root.iconbitmap(img_path)
        # Style 
        self.style = ttk.Style(self.root)

        current_dir = os.path.dirname(__file__)
        current_theme_path = os.path.dirname(current_dir)

        theme_dark_path = os.path.join(current_theme_path, "theme", "forest-dark.tcl")
        theme_light_path = os.path.join(current_theme_path, "theme", "forest-light.tcl")

        self.root.tk.call('source', theme_dark_path)
        self.root.tk.call('source', theme_light_path)

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
        self.header_frame.grid(row=0, column=0, padx=(10, 10), pady=(10, 5), sticky="nsew")

        self.label_title = ttk.Label(self.header_frame, text="Generar Guia Despacho de Cliente", font=('',15))
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
        self.findEntry.grid(row=0,column=0, padx=(0,5), pady=(0,10), sticky="ew")

        # Button
        self.btn_search = ttk.Button(self.search_frame, text="Buscar", style="Accent.TButton", command=self.showClient)
        self.btn_search.grid(row=0, column=1, padx=(0,5), pady=(0,10), sticky="nsew" )

        self.btn_add = ttk.Button(self.search_frame, text="Editar", state="disabled", command=self.inserClient)
        self.btn_add.grid(row=0, column=2, padx=(0,5), pady=(0,10), sticky="nsew")

        self.btn_update = ttk.Button(self.search_frame, text="Actualizar", style="Accent.TButton", command=self.updateClients)
        self.btn_update.grid(row=0, column=3, padx=(0,5), pady=(0,10), sticky="nsew")

        #Tree
        self.tree_clients = ttk.Treeview(self.search_frame, columns=('Nombre', 'Telefono', 'Ciudad'), show='headings')
        self.tree_clients.heading('Nombre', text="Nombre")
        self.tree_clients.heading('Telefono', text="Telefono")
        self.tree_clients.heading('Ciudad', text="Ciudad")
        self.tree_clients.grid(row=1, column=0, columnspan=4, padx=(5,0), pady=(10,0), sticky="nsew")

        # Template Frame -----------------------------------------------------------------------------------------
        self.template_frame = ttk.LabelFrame(self.main_frame, text="Plantilla", padding=(10,10))
        self.template_frame.grid(row=1, column=1, padx=(10, 5), pady=(0, 10), sticky="nsew")


        # Template Frame
        self.template_frame.columnconfigure(0, weight=1)  # Ajustar la primera columna al centro
        self.template_frame.rowconfigure((0, 2, 4), weight=0)  # Mantener el alto fijo de las etiquetas
        self.template_frame.rowconfigure((1, 3, 5), weight=0)  # Mantener el alto fijo de las entradas
        self.template_frame.rowconfigure(6, weight=0)  # Mantener el alto fijo del botón

        # Name
        self.label_name = ttk.Label(self.template_frame, text="Nombre")
        self.label_name.grid(row=0, column=0, padx=3, pady=(0,1), sticky="w")

        self.entry_name_info = ttk.Entry(self.template_frame)
        self.entry_name_info.grid(row=1, column=0, padx=5, pady=(0,10), sticky="ew")

        # Phone
        self.label_phone = ttk.Label(self.template_frame, text="Teléfono")
        self.label_phone.grid(row=2, column=0, padx=3, pady=(0,1), sticky="w")

        self.entry_phone_info = ttk.Entry(self.template_frame)
        self.entry_phone_info.grid(row=3, column=0, padx=5, pady=(0,10), sticky="ew")

        # ID
        self.label_id = ttk.Label(self.template_frame, text= "Identificacion")
        self.label_id.grid(row=0, column=1 , padx=4 , pady=(0,1), sticky="w")

        self.entry_id = ttk.Entry(self.template_frame)
        self.entry_id.grid(row=1,column=1, padx=5, pady=(0,10), sticky="ew")

        # City
        self.label_city_info = ttk.Label(self.template_frame, text= "Ciudad")
        self.label_city_info.grid(row=2, column=1, padx=4, pady=(0,1), sticky="w")

        self.entry_city_info = ttk.Entry(self.template_frame)
        self.entry_city_info.grid(row=3, column=1, padx=5,pady=(0,10),  sticky="ew")

        # Select
        self.check = tk.BooleanVar(value=False)
        self.pickUpOffice = ttk.Checkbutton(self.template_frame, text="Oficina?", variable= self.check)
        self.pickUpOffice.grid(row=4, column=0, columnspan=2, padx=4, pady=(0,10) , sticky="nsew")

        # Address
        self.label_address = ttk.Label(self.template_frame, text="Dirección")
        self.label_address.grid(row=5, column=0, padx=3, pady=(0,1), sticky="w")

        self.txt_address_info = tk.Text(self.template_frame, height=6, width= 7 ,wrap='word')
        self.txt_address_info.grid(row=6, column=0,columnspan=2, padx=6, pady=(0,20), sticky="ew")

        # Button
        self.btn_impr = ttk.Button(self.template_frame, text="Imprimir",state="disabled", command=self.printGuide, style="Accent.TButton", width=10)
        self.btn_impr.grid(row=7, column=0 , padx=4, columnspan=2,  pady=(0,10), sticky="nsew")

        # Footer Frame -----------------------------------------------------------------------------------------
        self.footer_frame = ttk.Frame(self.main_frame, padding=(10,5))
        self.footer_frame.grid(row=2, column=0, columnspan=2, padx=(5, 5), pady=(5, 5), sticky="nsew")

        self.label_signature = ttk.Label(self.footer_frame, text="POWERED BY Julian Chingal", font=('',10), foreground="gray")
        self.label_signature.grid(row=0,column=0,padx=0,pady=(2,0), sticky="e")

        # Configure the packing of the frames
        self.root.pack_propagate(False)
        self.main_frame.pack_propagate(False)
        # self.center_window()

        # Enter key bind
        self.findEntry.bind('<Return>', lambda event: self.showClient())

    def center_window(self):
        self.root.update()
        self.root.minsize(self.root.winfo_width(), self.root.winfo_height())
        x_cordinate = int((self.root.winfo_screenwidth()/2) - (self.root.winfo_width()/2))
        y_cordinate = int((self.root.winfo_screenheight()/2) - (self.root.winfo_height()/2))
        self.root.geometry("+{}+{}".format(x_cordinate, y_cordinate))

    def showClient(self):
        client = self.findEntry.get().upper()
        suggestion = findClient(client)

        if not suggestion:
            messagebox.showinfo('Error', 'Cliente no encontrado')
            self.findEntry.delete(0, 'end') #Limpiar casilla de busqueda
            self.btn_add.config(state="disabled")
            self.btn_impr.config(state="disabled")

        else:
            self.tree_clients.delete(*self.tree_clients.get_children())
            for info in suggestion:
                self.tree_clients.insert('','end', values=(info[0], info[2], info[4], *info))
            
            self.btn_add.config(state="normal")

    def inserClient(self):
        select = self.tree_clients.selection()
        
        # Clear boxes
        self.entry_name_info.delete(0, 'end')
        self.entry_id.delete(0, 'end')
        self.entry_phone_info.delete(0, 'end')
        self.txt_address_info.delete(1.0, 'end')
        self.entry_city_info.delete(0, 'end')

        if select:
            item = self.tree_clients.item(select)
            values = item['values']
            self.entry_name_info.insert(0, values[0])
            self.entry_id.insert(0, values[4])
            self.entry_phone_info.insert(0, values[1])
            self.txt_address_info.insert(1.0, values[6])
            self.entry_city_info.insert(0, values[2])
            self.btn_impr.config(state="normal")

    def printGuide(self):
        name = self.entry_name_info.get()
        id_client = self.entry_id.get()
        phone = self.entry_phone_info.get()
        address = self.txt_address_info.get("1.0", tk.END).strip() 
        city = self.entry_city_info.get()

        pdf = printTemplate(name, id_client, phone, address, city )
        pdf.saveTemplate(self.check.get())

        path = os.path.join(pdf.path_pdf)
        print("file path route pdf: "+ path)
        if pdf:
            messagebox.showinfo('Success', 'PDF Generado Exitosamente')
        else:
            messagebox.showerror('Warning', "Ocurrio un error!")
        
        subprocess.Popen(["start", path], shell=True)

    def updateClients(self):
        info = updateInfo()
        if info:
            messagebox.showinfo("Success", "Lista de clientes actualizada")
        else:
            messagebox.showerror("Error", "No se pudo actualizar la lista de clientes")

    def changeTheme(self):
        currentTheme = self.style.theme_use()    
        if currentTheme == 'forest-light':
            self.style.theme_use('forest-dark')
            self.root.config(bg="#313131")
        else:
            self.style.theme_use('forest-light')
            self.root.config(bg="#ffffff")