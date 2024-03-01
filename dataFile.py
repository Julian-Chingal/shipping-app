import pandas  as pd
from difflib import get_close_matches as gcm

def readData():
    file = pd.read_excel('Data/Clientes.xlsx')
    return file

def findClient(clientName):
    file = readData()
    clients = file['Nombre'].tolist()

    # Return the client idf the name is in the list
    if clientName in clients:
        return [clientName]
    
    # Return the closest clients if the name is not in the list
    suggestion = gcm(clientName, clients, n=5, cutoff=0.6)
    return suggestion