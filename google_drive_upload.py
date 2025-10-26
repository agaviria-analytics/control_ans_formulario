from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

# ------------------------------------------------------------
# CONFIGURACIÓN DE GOOGLE DRIVE
# ------------------------------------------------------------
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), '..', 'generated-tine-472900-u7-6afc104f3621.json')
FOLDER_ID = "1-Rg12PF0j59-sLYkjn3e_Hy9lcwxF5uz"  # ID de tu carpeta 'Evidencias_ANS'

# ------------------------------------------------------------
# CONEXIÓN A GOOGLE DRIVE
# ------------------------------------------------------------
def conectar_drive():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )
    return build("drive", "v3", credentials=creds)

# ------------------------------------------------------------
# SUBIR ARCHIVO A GOOGLE DRIVE
# ------------------------------------------------------------
def subir_a_drive(ruta_local, nombre_archivo):
    service = conectar_drive()

    file_metadata = {
        "name": nombre_archivo,
        "parents": [FOLDER_ID]
    }

    media = MediaFileUpload(ruta_local, resumable=True)
    archivo = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    print(f"✅ Archivo subido a Google Drive: {nombre_archivo}")
    return archivo.get("id")
