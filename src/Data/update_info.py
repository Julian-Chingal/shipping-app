import requests
import os, sys

# Variables
# url = "https://docs.google.com/spreadsheets/d/1XjTytSq-7bnvrtk3sLuDgbzSVmMtM4pX/edit?usp=drive_link&ouid=113043754513403743529&rtpof=true&sd=true"
url = "https://drive.google.com/file/d/12M_IfInPaBn5MOtpgDYWh--LtzYQ2U-h/view?usp=sharing"
file_id = url.split('/')[-2]

current_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.join(os.path.dirname(__file__), "..\\.")))
# file_path = os.path.join(current_path, "src", "data", "Clientes.xlsx")
file_path = os.path.join(current_path, "data", "clientList.json")

def updateInfo():
    # Retrieve the download URL using the file ID
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    try:
        # Send the GET request to download the file
        response = requests.get(download_url, stream=True)

        if response.status_code == 200:
            # Check for successful download
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print("Descarga exitosa!!")
            return True
        else:
            print(f"Failed to download file: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return False

# if __name__ == "__main__":
#     if updateInfo():
#         print("File downloaded successfully!")
#     else:
#         print("Failed to download file.")