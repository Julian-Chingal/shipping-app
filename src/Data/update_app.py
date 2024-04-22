import os
import shutil
import subprocess
import dropbox

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
