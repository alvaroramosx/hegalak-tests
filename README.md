# 📱 SPPB App - Test de Rendimiento Físico

Aplicación para realizar y generar informes del test SPPB (Short Physical Performance Battery).

Este proyecto contiene **dos versiones** de la misma aplicación:

- **Python/Kivy** - Multiplataforma (Windows, Mac, Linux, Android, iOS)
- **Kotlin/Android** - Aplicación nativa Android

---

## 📂 Estructura del Proyecto

```
hegalak-tests/
├── sppb_app_python/          # Aplicación Python/Kivy
│   ├── README.md             # Documentación Python
│   ├── requirements.txt       # Dependencias Python
│   └── sppb_app/            # Código fuente
│
├── sppb_app_kotlin/          # Aplicación Kotlin/Android
│   ├── README.md             # Documentación Android
│   ├── QUICKSTART.md         # Guía inicio rápido
│   └── app/                  # Código fuente Android
│
├── output/                   # Informes generados (PDF/Excel)
├── .gitignore                # Archivos ignorados por git
└── README.md                 # Este archivo
```

---

## 🎯 Funcionalidades

Ambas versiones incluyen:

- ✅ Flujo guiado completo del test SPPB
- ✅ Cálculo automático de puntuaciones (0-12)
- ✅ Interpretación de fragilidad (alta/moderada/baja)
- ✅ Generación de informe PDF
- ✅ Exportación a Excel
- ✅ Subida opcional a Google Drive
- ✅ Interfaz visual con gráficos

### Componentes del Test SPPB

1. **Equilibrio** (0-4 puntos)
   - Pies juntos
   - Semitándem
   - Tándem

2. **Velocidad de Marcha** (0-4 puntos)
   - Caminata de 4 metros

3. **Levantarse de Silla** (0-4 puntos)
   - 5 repeticiones sin usar brazos

### Interpretación

- **0-4 puntos**: Fragilidad alta 🔴
- **5-8 puntos**: Fragilidad moderada 🟡
- **9-12 puntos**: Fragilidad baja 🟢

---

## 🚀 Inicio Rápido

### Versión Python/Kivy

```bash
cd sppb_app_python
pip install -r requirements.txt
python -m sppb_app.main
```

Ver `sppb_app_python/README.md` para más detalles.

### Versión Kotlin/Android

```bash
cd sppb_app_kotlin
./gradlew assembleDebug
adb install app/build/outputs/apk/debug/app-debug.apk
```

Ver `sppb_app_kotlin/README.md` y `sppb_app_kotlin/QUICKSTART.md` para más detalles.

---

## 📚 Documentación

### Python/Kivy
- `sppb_app_python/README.md` - Guía completa

### Kotlin/Android
- `sppb_app_kotlin/README.md` - Documentación completa
- `sppb_app_kotlin/QUICKSTART.md` - Guía de inicio rápido
- `sppb_app_kotlin/COMANDOS_CONSOLA.md` - Comandos desde terminal
- `sppb_app_kotlin/EQUIVALENCIAS_PYTHON_KOTLIN.md` - Comparación de versiones

---

## 🆚 ¿Qué Versión Usar?

### Usa Python/Kivy si:
- Necesitas multiplataforma (Windows, Mac, Linux, Android, iOS)
- Quieres desarrollo rápido
- Prefieres Python
- No necesitas máximo rendimiento

### Usa Kotlin/Android si:
- Solo necesitas Android
- Quieres rendimiento nativo óptimo
- Prefieres Material Design nativo
- Vas a publicar en Play Store

---

## 📄 Archivos Generados

Ambas versiones generan informes en la carpeta `output/`:

- `SPPB_[nombre]_[timestamp].pdf` - Informe completo en PDF
- `SPPB_[nombre]_[timestamp].xlsx` - Datos en Excel

---

## 🛠️ Tecnologías

### Python/Kivy
- Python 3.11
- Kivy (Framework UI)
- ReportLab (PDF)
- openpyxl (Excel)
- Google Drive API

### Kotlin/Android
- Kotlin 1.9.20
- Jetpack Compose (UI)
- Material Design 3
- iText7 (PDF)
- Apache POI (Excel)
- Google Drive API Android

---

## 📝 Licencia

Este proyecto está desarrollado para uso en fisioterapia y evaluación geriátrica.

---

## 👥 Autor

Desarrollado para evaluación del rendimiento físico en adultos mayores mediante el test SPPB.

---

## 📞 Soporte

Para problemas o preguntas, consulta la documentación específica de cada versión:
- Python: `sppb_app_python/README.md`
- Android: `sppb_app_kotlin/README.md`

---

**Versión**: 1.0.0  
**Última actualización**: Octubre 2025
