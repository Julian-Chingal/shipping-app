import tkinter as tk
from tkinter import ttk, messagebox

app = tk.Tk()
app.title('Generador Guias de Despacho')
app.option_add('*tearOff', False)

# Make the app responsive
app.columnconfigure(index=0, weight=1)
app.columnconfigure(index=1, weight=1)
app.rowconfigure(index=0, weight=1)
app.rowconfigure(index=1, weight=1)

# Style
style = ttk.Style(app)

# tlc file

app.tk.call('source', 'theme/forest-light.tcl')
app.tk.call('source', 'theme/forest-dark.tcl')

style.theme_use('forest-light')

# List

# Start the main loop
app.mainloop()