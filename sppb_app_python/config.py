from __future__ import annotations

from pathlib import Path
from typing import Optional

# Directorio de salida para PDF/XLSX
OUTPUT_DIR: Path = Path("output")

# Nombre del centro que aparecerá en el informe
CENTER_NAME: str = "Centro de Fisioterapia"

# URL de la carpeta de Drive (formato https://drive.google.com/drive/folders/<FOLDER_ID>)
# Déjalo vacío para no subir y guardar solo en local
DRIVE_FOLDER_URL: str = "https://drive.google.com/drive/u/3/folders/0AK5JNFVwFvJzUk9PVA"

# Ruta al logo (opcional). Si None o cadena vacía, el PDF mostrará un marcador genérico
LOGO_PATH: Optional[str] = "assets/logo.png"

# Subida a Drive: credenciales y modo de autenticación
# - Si USE_SERVICE_ACCOUNT=True, se usa una cuenta de servicio con un JSON de clave
# - Si False, se usa OAuth de usuario final (se generará/leerá token.json junto al credentials.json)
USE_SERVICE_ACCOUNT: bool = True
CREDENTIALS_JSON_PATH: str = "credentials.json"


# Ajustes de ventana por tipo de dispositivo
# - DEVICE_KIND: forzar tipo de dispositivo ('phone' | 'tablet') o None para auto
# - PHONE_WINDOW_SIZE / TABLET_WINDOW_SIZE: tamaños usados en escritorio
DEVICE_KIND: Optional[str] = None
PHONE_WINDOW_SIZE = (480, 800)
TABLET_WINDOW_SIZE = (900, 900)








