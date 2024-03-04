import requests
import os, sys

# Variables
url_online = ""

current_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), "..\\.")))
file_path = os.path.join(current_path, "src","data", "Clientes.xlsx")

def descargar_archivo_desde_onedrive(url, ruta_local):
    try:
        # Realiza la solicitud HTTP para descargar el archivo
        response = requests.get(url)
        response.raise_for_status()  # Verifica si la descarga fue exitosa

        # Guarda el contenido en un archivo local
        with open(ruta_local, 'wb') as archivo_local:
            archivo_local.write(response.content)

        print(f"Archivo descargado correctamente en {ruta_local}")
    except Exception as e:
        print(f"Error al descargar el archivo: {e}")

