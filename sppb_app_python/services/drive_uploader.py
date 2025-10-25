from __future__ import annotations

import re
from pathlib import Path
from typing import Optional, Tuple

from google.oauth2 import service_account
from google.oauth2.credentials import Credentials as OAuthCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]


def _extract_folder_id_from_url(url: str) -> Optional[str]:
	m = re.search(r"/folders/([a-zA-Z0-9_-]+)", url)
	if m:
		return m.group(1)
	# También soporta enlaces tipo open?id=<ID>
	m2 = re.search(r"[?&]id=([a-zA-Z0-9_-]+)", url)
	return m2.group(1) if m2 else None


def _get_oauth_credentials(credentials_json_path: str) -> OAuthCredentials:
	token_path = Path(credentials_json_path).with_name("token.json")
	creds: Optional[OAuthCredentials] = None
	if token_path.exists():
		creds = OAuthCredentials.from_authorized_user_file(str(token_path), SCOPES)
	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(credentials_json_path, SCOPES)
			creds = flow.run_local_server(port=0)
		with open(token_path, "w", encoding="utf-8") as f:
			f.write(creds.to_json())
	return creds


def _get_credentials(credentials_json_path: str, use_service_account: bool = False):
	if use_service_account:
		return service_account.Credentials.from_service_account_file(credentials_json_path, scopes=SCOPES)
	return _get_oauth_credentials(credentials_json_path)


def upload_file_to_drive(
	local_path: str,
	folder_url: str,
	credentials_json_path: str,
	use_service_account: bool = False,
) -> Tuple[str, str]:
	folder_id = _extract_folder_id_from_url(folder_url)
	if not folder_id:
		raise RuntimeError("URL de carpeta de Drive inválida")

	creds = _get_credentials(credentials_json_path, use_service_account=use_service_account)
	service = build("drive", "v3", credentials=creds)

	file_path = Path(local_path)
	media = MediaFileUpload(str(file_path), resumable=True)

	# Verificación previa: la carpeta existe, es accesible y es realmente una carpeta
	folder_meta = service.files().get(
		fileId=folder_id,
		fields="id, name, mimeType, driveId",
		supportsAllDrives=True,
	).execute()
	if folder_meta.get("mimeType") != "application/vnd.google-apps.folder":
		raise RuntimeError("El ID proporcionado no corresponde a una carpeta de Drive")
	# Con cuentas de servicio, subir a "Mi unidad" no es posible (no tienen cuota)
	# Se requiere una Unidad compartida (driveId presente) o delegación de dominio
	if use_service_account and not folder_meta.get("driveId"):
		raise RuntimeError(
			"Con cuentas de servicio debes usar una carpeta dentro de una Unidad compartida. "
			"Esta carpeta parece estar en 'Mi unidad'. Usa OAuth (USE_SERVICE_ACCOUNT=False) "
			"o mueve la carpeta a una Unidad compartida y compártela con la cuenta de servicio."
		)

	file_metadata = {"name": file_path.name, "parents": [folder_id]}
	# supportsAllDrives=True permite subir tanto a "Mi unidad" como a "Unidades compartidas"
	created = service.files().create(
		body=file_metadata,
		media_body=media,
		fields="id, webViewLink",
		supportsAllDrives=True,
	).execute()
	return created.get("id"), created.get("webViewLink")





