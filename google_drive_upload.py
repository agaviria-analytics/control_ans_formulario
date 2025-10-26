from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

# ------------------------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------------------------
# Ruta al archivo JSON de credenciales (ajusta el nombre exacto si cambia)
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), '..', 'generated-tine-472900-u7-6afc104f3621.json')

# ID de la carpeta en Drive (de tu enlace de Google Drive)
FOLDER_ID = "1d8kNCq2Db0qJBmEwdfZEuxk0SzhguBCI"

# ------------------------------------------------------------
# CONEXIÓN CON GOOGLE DRIVE
# ------------------------------------------------------------
def conectar_drive():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    service = build('drive', 'v3', credentials=creds)
    return service

# ------------------------------------------------------------
# SUBIR ARCHIVO (PDF o IMAGEN)
# ------------------------------------------------------------
def subir_a_drive(ruta_local, nombre_archivo):
    try:
        service = conectar_drive()

        # Verificar acceso a la carpeta
        try:
            folder_info = service.files().get(fileId=FOLDER_ID, fields="id, name").execute()
            print(f"📁 Carpeta encontrada en Drive: {folder_info['name']} (ID: {folder_info['id']})")
        except Exception as e:
            print("❌ No se pudo acceder a la carpeta en Drive:", e)
            return f"Error de carpeta: {str(e)}"

        file_metadata = {
            'name': nombre_archivo,
            'parents': [FOLDER_ID]
        }
        media = MediaFileUpload(ruta_local, resumable=True)
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f"✅ Subido correctamente: {nombre_archivo}")
        return f"Subido correctamente: {nombre_archivo}"

    except Exception as e:
        print(f"⚠ Error al subir {nombre_archivo}:", e)
        return f"Error al subir {nombre_archivo}: {e}"

# ------------------------------------------------------------
# TEST MANUAL (opcional)
# ------------------------------------------------------------
if __name__ == "__main__":
    # Prueba de conexión y listado de la carpeta
    service = conectar_drive()
    try:
        results = service.files().list(q=f"'{FOLDER_ID}' in parents", pageSize=10, fields="files(id, name)").execute()
        files = results.get("files", [])
        print("\nArchivos encontrados en la carpeta destino:")
        for f in files:
            print(f" - {f['name']} ({f['id']})")
        if not files:
            print("🟡 Carpeta vacía pero accesible correctamente.")
    except Exception as e:
        print("❌ Error al listar carpeta:", e)
