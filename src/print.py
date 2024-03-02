import os
import subprocess

# Obtener la lista de impresoras
def obtener_impresoras():
    impresoras = []
    # Ejecutar el comando para obtener las impresoras
    cmd = "wmic printer get name"
    impresoras_disponibles = subprocess.check_output(cmd, shell=True)
    impresoras_disponibles = impresoras_disponibles.decode('utf-8').split('\n')
    for impresora in impresoras_disponibles:
        if impresora:
            impresoras.append(impresora)
    return impresoras

# Imprimir un archivo
def imprimir_archivo(impresora, archivo):
    cmd = "lpr -P {} {}".format(impresora, archivo)
    os.system(cmd)

# Uso de las funciones
impresoras = obtener_impresoras()
print("Impresoras disponibles: ", impresoras)

# Supongamos que quieres imprimir en la primera impresora disponible
# if impresoras:
#     imprimir_archivo(impresoras[0], "/ruta/al/archivo/a/imprimir")
