# SPPB App

Aplicación Kivy para realizar y generar informes del test SPPB (Short Physical Performance Battery).

## Características

- Flujo guiado: datos iniciales, equilibrio, marcha, silla, y resumen final.
- Exportación a PDF y Excel en `output/`.
- Subida opcional a Google Drive con OAuth o cuenta de servicio.
- Detección de dispositivo y tamaños de ventana adaptados.
- Resumen visual con dónuts y colores por rendimiento.
- Interpretación fisioterapéutica automática (corta en pantalla, detallada en PDF).

## Requisitos

Python 3.11 recomendado.

Instala dependencias:

```bash
pip install -r requirements.txt
```

Para usar gráficos Garden (opcional):

```bash
pip install kivy-garden kivy_garden.graph
```

## Ejecutar

```bash
python -m sppb_app.main
```

## Configuración

Edita `sppb_app/config.py`:

- `OUTPUT_DIR`: carpeta de salida.
- `CENTER_NAME`: nombre del centro (aparece en PDF).
- `DRIVE_FOLDER_URL`: carpeta de destino en Drive (vacío para desactivar subida).
- `USE_SERVICE_ACCOUNT` y `CREDENTIALS_JSON_PATH`: modo de autenticación Drive.
- `LOGO_PATH`: ruta al logo. Si se deja vacío, se intentará `sppb_app/assets/logo.png`.
- `DEVICE_KIND` y tamaños de ventana para escritorio.

## Flujo de datos

- En la pantalla inicial se capturan: nombre, edad, fecha y fisioterapeuta.
- En el resumen, se muestra puntuación por bloques (0–4) y total (0–12), con dónuts.
- Al exportar, el PDF incluye:
  - Datos del paciente (incl. fisioterapeuta)
  - Resultados detallados
  - Conclusión total
  - Interpretación fisioterapéutica por bloque y global

## Credenciales de Drive

- Cuenta de servicio: coloca el JSON y comparte la carpeta de Drive con el cliente de servicio.
- OAuth usuario: coloca `credentials.json`; se generará `token.json` en el primer uso.

## Notas

- El logo se busca en `config.LOGO_PATH` y, si no está, en `sppb_app/assets/logo.png`.
- Los dónuts cambian de color por tramos: rojo → naranja → amarillo → verde claro → verde.


