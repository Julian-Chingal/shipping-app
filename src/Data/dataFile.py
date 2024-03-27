import os, sys, json

def readData():
    current_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), "..\\.")))
    file_path = os.path.join(current_path, "data", "clientList.json")

    # Verificar si el archivo existe
    if not os.path.exists(file_path):
        print("El archivo JSON no existe:", file_path)
        return None

    # Intentar leer el archivo JSON
    try:
        with open(file_path, 'r',  encoding='utf-8') as file:
            data = json.load(file)
            
            del data["status"]

            # Obtener el segundo valor de la lista dentro de la clave "state_id"
            state_id_second_value = data["data"][0]["state_id"][1]

        return data

    except Exception as e:
        print("Error al leer el archivo JSON:", e)
        return None

def searchClientByName(search_term):
    # Obtener los datos del JSON
    clients_data = readData()

    if clients_data is None:
        return None

    # Lista para almacenar los clientes que coinciden con el término de búsqueda
    matching_clients = []

    # Iterar sobre los clientes y buscar coincidencias por nombre
    for client in clients_data["data"]:
        client_name = client["name"]
        if search_term.lower() in client_name.lower():  # Buscar coincidencias (ignorar mayúsculas/minúsculas)
            matching_clients.append(client)

    return matching_clients