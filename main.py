from dataFile import findClient
from tkinter import Tk, Label, Entry, Button, messagebox, Frame
from tkinter.ttk import Combobox

# Variables
root = Tk()

# Widgets
search_frame = Frame(root, bg='blue')
info_frame = Frame(root, bg='red')

# Entradas
findEntry = Entry(search_frame)
nameEntry = Entry(root)
directionEntry = Entry(root)
telephoneEntry = Entry(root)
combobox = Combobox(root)


# Funtions
def showClient():
    client = findEntry.get()
    suggestion = findClient(client)

    if not suggestion:
        messagebox.showinfo('Error', 'Cliente no encontrado')
    else:
        combobox['values'] = suggestion
        

def getValues():
    select = combobox.selection_get()

    print(select)

# Interface ---------------------------------------------------------------------------------
root.title('Generador Guias de Despacho')
root.geometry('700x500')
root.config(bg='gray')

# Frames
search_frame.pack(pady=10)
info_frame.pack(pady=10)

# Widgets
label_find = Label(search_frame, 
                   text='Buscar Cliente',
                   font=('Courier', 14),
                   bg='gray',
                   justify='center')
label_find.pack()

findEntry.pack()
findEntry.focus()

btn_find = Button(search_frame, 
                text='Buscar',
                font=('Courier', 12), 
                command=showClient)
btn_find.pack()

combobox.pack()

combobox.bind("<<ComboboxSelected>>", getValues)
# Main
root.mainloop()