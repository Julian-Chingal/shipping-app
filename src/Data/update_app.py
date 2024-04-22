import os, urllib.request
import shutil
import subprocess
import dropbox

token = "sl.Bz0JHk39IGY-UofjfzJxIkxLOVTBQGyUSbEMJ_Sr1SR4dXakw5XPozmM-DopyimIhLMMWU38-Ki1PvJlNnkJQaKqxGLaHCX3mkRuup4KtWrHv_o2NmqltkLv9Hgs8pcIpoUU7BRP3N2z"

def DownloadNewRelease(token):
    try:
        dbx = dropbox.Dropbox(token)
        dbx.users_get_current_account()  # Verificar conexión
        
        # Crear un directorio temporal para descargar la nueva versión
        temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_download')
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        
        temp_file_path = os.path.join(temp_dir, "app.exe")
        
        # Descargar la nueva versión en el directorio temporal
        with open(temp_file_path, "wb") as f:
            metadata, res = dbx.files_download(path="/app.exe")
            f.write(res.content)
        
        print("La nueva versión ha sido descargada exitosamente.")
        
        return temp_file_path  # Devuelve la ruta del archivo descargado
    except dropbox.exceptions.ApiError as e:
        print(f"Error al descargar el archivo: {e}")
    except Exception as e:
        print(f"Error desconocido: {e}")
    
    return None  # Indica que hubo un error en la descarga

def download_pru():
    url = "https://www.dropbox.com/scl/fi/cwejpkbu6fqvtipfvc10u/app_v1.exe?rlkey=tsa1xoy03pd8uj7mp31wveo76&st=0j745i9y&dl=0"

    # Crear un directorio temporal para descargar la nueva versión
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_download')
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    temp_file_path = os.path.join(temp_dir, "app.exe")
    
    a = urllib.request.urlretrieve(url, temp_file_path)

    if a:
        print("Descarga exitosa")
    else:
        print("Error en la descarga")


def ReplaceAndRestartApp(new_file_path, old_file_path):
    if new_file_path:
        try:
            # Cerrar la aplicación
            subprocess.call(["taskkill", "/f", "/im", "app.exe"])
            
            # Reemplazar la versión antigua con la nueva versión descargada
            shutil.move(new_file_path, old_file_path)
            
            # Abrir la aplicación nuevamente
            subprocess.Popen([old_file_path])
            
            return True
        except Exception as e:
            print(f"Error al reemplazar y reiniciar la aplicación: {e}")
    
    return False

def CleanupTempDirectory(temp_dir):
    try:
        shutil.rmtree(temp_dir)  # Eliminar la carpeta temporal y su contenido
        print("Carpeta temporal eliminada correctamente.")
    except Exception as e:
        print(f"Error al eliminar la carpeta temporal: {e}")

def UpdateApp(path_to_app):
    global token
    new_file_path = DownloadNewRelease(token)

    if new_file_path:
        if ReplaceAndRestartApp(new_file_path, path_to_app):
            print("La aplicación ha sido actualizada exitosamente.")
            CleanupTempDirectory(os.path.join(os.path.dirname(new_file_path), 'temp_download'))
        else:
            print("Error al reemplazar y reiniciar la aplicación.")
    else:
        print("Error al descargar la nueva versión.")


if __name__ == "__main__":
    download_pru()

