# SPPB App - Versión Python/Kivy

Aplicación multiplataforma para realizar y generar informes del test SPPB (Short Physical Performance Battery).

## 🎯 Características

- ✅ Multiplataforma: Windows, Mac, Linux, Android, iOS
- ✅ Flujo guiado: datos iniciales, equilibrio, marcha, silla, y resumen final
- ✅ Exportación a PDF y Excel en `output/`
- ✅ Subida opcional a Google Drive con OAuth o cuenta de servicio
- ✅ Detección de dispositivo y tamaños de ventana adaptados
- ✅ Resumen visual con dónuts y colores por rendimiento
- ✅ Interpretación fisioterapéutica automática

## 📋 Requisitos

- Python 3.11 recomendado
- pip (gestor de paquetes Python)

## 🚀 Instalación

### 1. Crear entorno virtual (recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. (Opcional) Instalar gráficos Garden

```bash
pip install kivy-garden kivy_garden.graph
```

## ▶️ Ejecutar

```bash
python -m sppb_app.main
```

## ⚙️ Configuración

Edita `sppb_app/config.py`:

- `OUTPUT_DIR`: carpeta de salida (por defecto: `output/`)
- `CENTER_NAME`: nombre del centro (aparece en PDF)
- `DRIVE_FOLDER_URL`: carpeta de destino en Drive (vacío para desactivar)
- `USE_SERVICE_ACCOUNT`: modo de autenticación Drive
- `CREDENTIALS_JSON_PATH`: ruta a las credenciales
- `LOGO_PATH`: ruta al logo (por defecto: `sppb_app/assets/logo.png`)

## 📊 Flujo de Datos

1. **Pantalla inicial**: captura nombre, edad, fecha y fisioterapeuta
2. **Equilibrio**: pies juntos → semitándem → tándem
3. **Marcha**: velocidad en 4 metros (2 mediciones)
4. **Silla**: 5 levantamientos sin usar brazos
5. **Resumen**: puntuación por bloques (0-4) y total (0-12)
6. **Exportación**: PDF + Excel en `output/`

## 🔐 Google Drive

### Cuenta de servicio (recomendado)

1. Crea proyecto en Google Cloud Console
2. Habilita Google Drive API
3. Crea cuenta de servicio
4. Descarga JSON de credenciales
5. Comparte la carpeta de Drive con el email de la cuenta de servicio
6. Coloca el JSON en `credentials.json`

### OAuth usuario

1. Descarga `credentials.json` desde Google Cloud Console
2. En el primer uso, se abrirá el navegador para autorizar
3. Se generará `token.json` automáticamente

## 📝 Notas

- El logo se busca en `config.LOGO_PATH` y, si no está, en `sppb_app/assets/logo.png`
- Los dónuts cambian de color por tramos: rojo → naranja → amarillo → verde claro → verde
- Las puntuaciones se calculan según el estándar SPPB

## 📦 Estructura

```
sppb_app/
├── main.py                    # Punto de entrada
├── config.py                  # Configuración
├── assets/
│   └── logo.png              # Logo del centro
├── models/
│   └── sppb_logic.py         # Lógica de cálculo SPPB
├── services/
│   ├── pdf_generator.py      # Generación PDF
│   ├── excel_exporter.py      # Exportación Excel
│   ├── drive_uploader.py      # Subida Drive
│   └── explanations.py        # Textos interpretativos
└── ui/
    ├── screens.py             # Pantallas de la app
    ├── state.py               # Estado de la sesión
    └── theme.kv               # Tema visual
```

## 🆚 Comparación con Versión Android

### Ventajas de esta versión:
- ✅ Multiplataforma (no solo Android)
- ✅ Mismo código para todas las plataformas
- ✅ No requiere Android Studio
- ✅ Desarrollo más rápido

### Desventajas:
- ⚠️ Apps más grandes (~20-30 MB)
- ⚠️ Menor integración con el OS
- ⚠️ UI no completamente nativa

Ver la versión Android en `../sppb_app_kotlin/` para mejor rendimiento en Android.

## 📞 Soporte

Para problemas específicos, consulta la documentación o crea un issue.

---

**Versión**: 1.0.0  
**Última actualización**: Octubre 2025

