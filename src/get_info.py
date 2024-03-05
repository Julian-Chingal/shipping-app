import gdown
import os, sys

# Variables
url =  "https://docs.google.com/spreadsheets/d/1XjTytSq-7bnvrtk3sLuDgbzSVmMtM4pX/edit?usp=drive_link&ouid=113043754513403743529&rtpof=true&sd=true"
file_id = url.split('/')[-2]

current_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), "..\\.")))
file_path = os.path.join(current_path, "src","data", "Clientes.xlsx")

def updateInfo():
    prefix = 'https://drive.google.com/uc?/export=download&id='
    c = prefix+file_id
    try:
        gdown.download(c, output=file_path)
        return True
    except:
        return False