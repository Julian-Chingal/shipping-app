from dataFile import findClient, readData
import tkinter as tk
from tkinter import ttk, messagebox





# Functions ------------------------------------------------------
def showClient():
    client = findEntry.get()
    suggestion = findClient(client)
    
    if not client:
        showAllClient()
        return

    if not suggestion:
        messagebox.showinfo('Error', 'Cliente no encontrado')
        findEntry.delete(0, 'end') #Limpiar casilla de busqueda
        btn_add.config(state="disabled")
        btn_impr.config(state="disabled")

    else:
        tree_clients.delete(*tree_clients.get_children())
        for info in suggestion:
            tree_clients.insert('','end', values=info)
        
        btn_add.config(state="normal")
         
def showAllClient():
    data = readData()
    tree_clients.delete(*tree_clients.get_children()) #Limpiar antes de poner informacion
    for info in data:
        tree_clients.insert('', 'end', values=info)

def inserClient():
    select = tree_clients.selection()
    
    # Limpiar Casillas
    entry_name_info.delete(0, 'end')
    entry_phone_info.delete(0, 'end')
    txt_address_info.delete(1.0, 'end')

    if select:
        item = tree_clients.item(select)
        values = item['values']
        entry_name_info.insert(0, values[0])
        entry_phone_info.insert(0, values[1])
        txt_address_info.insert(1.0, values[2])
        btn_impr.config(state="normal")

def changeTheme():
    currentTheme = style.theme_use()    
    if currentTheme == 'forest-light':
        style.theme_use('forest-dark')
        app.config(bg="#313131")
    else:
        style.theme_use('forest-light')
        app.config(bg="#ffffff")

# Setup ---------------------------------------------------------
app = tk.Tk()
app.title('Generador Guias de Despacho')
# app.geometry('900x500')
app.option_add('*tearOff', False)

# Make the app responsive
app.columnconfigure(index=0, weight=1)
app.columnconfigure(index=1, weight=1)
app.columnconfigure(index=2, weight=1)
app.rowconfigure(index=0, weight=0)
app.rowconfigure(index=1, weight=1)
app.rowconfigure(index=2, weight=1)

# Style ----------------------------------------------------------
style = ttk.Style(app)

# tlc file
app.tk.call('source', 'theme/forest-dark.tcl')
app.tk.call('source', 'theme/forest-light.tcl')

style.theme_use('forest-light')

# Header Frame -----------------------------------------------------------------------------------------
header_frame = ttk.Frame(app, padding=(10,5))
header_frame.grid(row=0, column=0, columnspan=2, padx=(10, 10), pady=(10, 5), sticky="nsew")

label_title = ttk.Label(header_frame, text="Generador Plantilla Despacho de Clientes", font=('',15))
label_title.grid(row=0,column=0,padx=0,pady=(10,20), sticky="w")

change_theme = ttk.Checkbutton(header_frame, text="Tema", style="Switch", command=changeTheme)
change_theme.grid(row=1,column=0, padx=0, pady=(0,10), sticky="se")

# Search Frame -----------------------------------------------------------------------------------------
search_frame = ttk.LabelFrame(app, text="Busqueda Cliente", padding=(10,10))
search_frame.grid(row=1, column=0, padx=(5, 5), pady=(0, 10), sticky="nsew")

# Search Frame
search_frame.columnconfigure(0, weight=1)  # Ajustar la primera columna al centro
search_frame.columnconfigure(1, weight=0)  # Mantener el ancho fijo del botón
search_frame.columnconfigure(2, weight=0)  # Mantener el ancho fijo del botón

# Entry
findEntry = ttk.Entry(search_frame)
findEntry.insert(0, "Escriba un Nombre")
findEntry.grid(row=1,column=0, padx=(0,5), pady=(0,10), sticky="ew")

# Button
btn_search = ttk.Button(search_frame, text="Buscar", style="Accent.TButton", command=showClient)
btn_search.grid(row=1, column=1, padx=(0,5), pady=(0,10), sticky="nsew" )

btn_add = ttk.Button(search_frame, text="Editar", state="disabled", command=inserClient)
btn_add.grid(row=1, column=2, padx=(0,5), pady=(0,10), sticky="nsew")

#Tree
tree_clients = ttk.Treeview(search_frame, columns=('Nombre', 'Telefono', 'Direccion'), show='headings')
tree_clients.heading('Nombre', text="Nombre")
tree_clients.heading('Telefono', text="Telefono")
tree_clients.heading('Direccion', text="Direccion")
tree_clients.grid(row=2, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")

# Template Frame -----------------------------------------------------------------------------------------
template_frame = ttk.LabelFrame(app, text="Plantilla", padding=(10,10))
template_frame.grid(row=1, column=1, padx=(10, 5), pady=(0, 10), sticky="nsew")


# Template Frame
template_frame.columnconfigure(0, weight=1)  # Ajustar la primera columna al centro
template_frame.rowconfigure((0, 2, 4), weight=0)  # Mantener el alto fijo de las etiquetas
template_frame.rowconfigure((1, 3, 5), weight=0)  # Mantener el alto fijo de las entradas
template_frame.rowconfigure(6, weight=0)  # Mantener el alto fijo del botón


# Name
label_name = ttk.Label(template_frame, text="Nombre del Cliente")
label_name.grid(row=0, column=0, padx=3, pady=(0,1), sticky="w")

entry_name_info = ttk.Entry(template_frame)
entry_name_info.grid(row=1, column=0, padx=5, pady=(0,10), sticky="ew")

# Phone
label_phone = ttk.Label(template_frame, text="Telefono del Cliente")
label_phone.grid(row=2, column=0, padx=3, pady=(0,1), sticky="w")

entry_phone_info = ttk.Entry(template_frame)
entry_phone_info.grid(row=3, column=0, padx=5, pady=(0,10), sticky="ew")

# Address
label_address = ttk.Label(template_frame, text="Direccion del Cliente")
label_address.grid(row=4, column=0, padx=3, pady=(0,1), sticky="w")

txt_address_info = tk.Text(template_frame, height=4, width= 5 ,wrap='word')
txt_address_info.grid(row=5, column=0, padx=6, pady=(0,20), sticky="ew")

# Button
btn_impr = ttk.Button(template_frame, text="Imprimir",state="disabled", style="Accent.TButton")
btn_impr.grid(row=6, column=0 , padx=5, pady=(0,10), sticky="nsew")

# Center the window, and set minsize
app.update()
app.minsize(app.winfo_width(), app.winfo_height())
x_cordinate = int((app.winfo_screenwidth()/2) - (app.winfo_width()/2))
y_cordinate = int((app.winfo_screenheight()/2) - (app.winfo_height()/2))
app.geometry("+{}+{}".format(x_cordinate, y_cordinate))

# Start the main loop
app.mainloop()