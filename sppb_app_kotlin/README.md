# SPPB App - Versión Android/Kotlin

Aplicación Android nativa para realizar y generar informes del test SPPB (Short Physical Performance Battery).

Esta es la versión Kotlin/Android de la aplicación SPPB original en Python/Kivy, con la misma funcionalidad y lógica pero optimizada para dispositivos Android.

## 🎯 Características

- ✅ **Flujo guiado completo**: Datos iniciales → Equilibrio (3 pruebas) → Marcha → Silla → Resumen
- ✅ **Cálculo automático de puntuaciones** según estándares SPPB
- ✅ **Interpretación fisioterapéutica** detallada
- ✅ **Exportación a PDF** con informe completo
- ✅ **Exportación a Excel** con todos los datos
- ✅ **Subida a Google Drive** (opcional)
- ✅ **Interfaz moderna** con Jetpack Compose y Material Design 3
- ✅ **Tema visual** análogo a la app original (colores cálidos marrón/beige)
- ✅ **Indicadores visuales** de puntuación tipo "donut gauge"

## 📱 Requisitos

### Para compilar:
- **Android Studio** Hedgehog (2023.1.1) o superior
- **JDK 17** o superior
- **Android SDK** API 26+ (Android 8.0+)
- **Gradle** 8.2+

### Para ejecutar:
- Dispositivo Android con **API 26+** (Android 8.0 Oreo o superior)
- Conexión a internet (para subida a Drive)

## 🚀 Instalación y Compilación

### 1. Clonar/Abrir el proyecto

```bash
cd sppb_app_kotlin
```

### 2. Abrir en Android Studio

1. Abre Android Studio
2. File → Open → Selecciona la carpeta `sppb_app_kotlin`
3. Espera a que Gradle sincronice

### 3. Configurar SDK

Si Android Studio no encuentra el SDK automáticamente:

1. File → Project Structure → SDK Location
2. Configura la ruta del Android SDK
3. Asegúrate de tener instalado SDK API 34

### 4. Compilar

#### Desde Android Studio:
- Build → Make Project (Ctrl+F9)
- Build → Build Bundle(s) / APK(s) → Build APK(s)

#### Desde línea de comandos:
```bash
./gradlew assembleDebug
```

El APK se generará en: `app/build/outputs/apk/debug/app-debug.apk`

### 5. Ejecutar en emulador o dispositivo

#### En emulador:
1. Tools → Device Manager
2. Crea un dispositivo virtual (recomendado: Pixel 5, API 34)
3. Run → Run 'app'

#### En dispositivo físico:
1. Habilita **Opciones de desarrollador** en tu Android
2. Activa **Depuración USB**
3. Conecta el dispositivo por USB
4. Run → Run 'app'

## 📚 Estructura del Proyecto

```
sppb_app_kotlin/
├── app/
│   ├── src/main/
│   │   ├── java/com/sppb/
│   │   │   ├── data/
│   │   │   │   ├── models/
│   │   │   │   │   └── SppbModels.kt          # Modelos de datos y lógica SPPB
│   │   │   │   └── repositories/
│   │   │   ├── services/
│   │   │   │   ├── ExplanationService.kt      # Textos interpretativos
│   │   │   │   ├── PdfGeneratorService.kt     # Generación de PDF (iText)
│   │   │   │   ├── ExcelExporterService.kt    # Exportación Excel (Apache POI)
│   │   │   │   └── DriveUploaderService.kt    # Subida a Google Drive
│   │   │   ├── viewmodels/
│   │   │   │   └── SppbViewModel.kt           # ViewModel principal
│   │   │   ├── ui/
│   │   │   │   ├── theme/
│   │   │   │   │   ├── Theme.kt               # Tema Material 3
│   │   │   │   │   └── Type.kt                # Tipografía
│   │   │   │   ├── components/
│   │   │   │   │   └── CommonComponents.kt    # Componentes reutilizables
│   │   │   │   └── screens/
│   │   │   │       ├── StartScreen.kt         # Pantalla inicial
│   │   │   │       ├── BalanceScreens.kt      # Pantallas de equilibrio (3)
│   │   │   │       ├── GaitScreen.kt          # Pantalla de marcha
│   │   │   │       ├── ChairScreen.kt         # Pantalla de silla
│   │   │   │       └── SummaryScreen.kt       # Pantalla de resumen
│   │   │   └── MainActivity.kt                # Activity principal + Navegación
│   │   ├── res/
│   │   │   ├── values/
│   │   │   │   ├── strings.xml                # Textos de la app
│   │   │   │   ├── colors.xml                 # Colores del tema
│   │   │   │   └── themes.xml                 # Tema base
│   │   │   └── xml/
│   │   │       ├── file_paths.xml             # Rutas para FileProvider
│   │   │       ├── backup_rules.xml           # Reglas de backup
│   │   │       └── data_extraction_rules.xml
│   │   └── AndroidManifest.xml                # Manifest de la app
│   └── build.gradle.kts                       # Dependencias de la app
├── build.gradle.kts                           # Configuración raíz
├── settings.gradle.kts                        # Configuración de Gradle
└── README.md                                  # Este archivo
```

## 🔧 Tecnologías y Librerías

### Core
- **Kotlin** 1.9.20
- **Jetpack Compose** (UI moderna declarativa)
- **Material Design 3** (tema visual)
- **Navigation Compose** (navegación entre pantallas)
- **ViewModel** + **StateFlow** (gestión de estado)

### Generación de documentos
- **iText7** - Generación de PDFs
- **Apache POI** - Exportación a Excel

### Google Drive
- **Google Play Services Auth** - Autenticación
- **Google API Client Android** - Cliente API
- **Google Drive API v3** - Subida de archivos

### Otras
- **Coroutines** - Operaciones asíncronas
- **DataStore** - Almacenamiento de preferencias

## 🎨 Diseño y Estética

La aplicación replica la estética de la versión Python/Kivy:

- **Colores principales**: Marrón oscuro (#7C2D12), Naranja (#EA580C)
- **Fondo**: Beige claro (#F8F3EA)
- **Indicadores de puntuación**: Gráficos circulares (donut) con colores graduales:
  - Rojo → Naranja → Amarillo → Verde claro → Verde
- **Componentes**: Tarjetas elevadas, botones redondeados, campos de texto con borde

## 📊 Lógica del Test SPPB

### Equilibrio (0-4 puntos)
1. **Pies juntos** (0-10s): Si no mantiene 10s → 0 puntos, termina test de equilibrio
2. **Semitándem** (0-10s): Si no mantiene 10s → 1 punto, termina test de equilibrio
3. **Tándem** (0-10s):
   - < 3s → 2 puntos totales
   - 3-9.99s → 3 puntos totales
   - ≥ 10s → 4 puntos totales

### Velocidad de Marcha (0-4 puntos)
- Se realizan 2 mediciones de 4 metros
- Se toma el **mejor tiempo** (el más corto)
- Puntuación según tiempo:
  - No puede o > 8.70s → 0-1 puntos
  - 6.21-8.70s → 2 puntos
  - 4.82-6.20s → 3 puntos
  - < 4.82s → 4 puntos

### Levantarse de Silla (0-4 puntos)
- Pre-test: ¿Puede levantarse sin brazos?
- 5 repeticiones sin usar los brazos
- Puntuación según tiempo:
  - No puede o > 60s → 0 puntos
  - ≥ 16.70s → 1 punto
  - 13.70-16.69s → 2 puntos
  - 11.20-13.69s → 3 puntos
  - ≤ 11.19s → 4 puntos

### Total (0-12 puntos)
- **0-4**: Fragilidad alta
- **5-8**: Fragilidad moderada
- **9-12**: Fragilidad baja

## 🔐 Configuración de Google Drive

Para habilitar la subida a Drive:

### 1. Crear proyecto en Google Cloud Console

1. Ve a https://console.cloud.google.com
2. Crea un nuevo proyecto
3. Habilita la API de Google Drive

### 2. Crear credenciales OAuth 2.0

1. APIs y servicios → Credenciales
2. Crear credenciales → ID de cliente de OAuth
3. Tipo: Android
4. Nombre del paquete: `com.sppb`
5. Huella digital SHA-1:
```bash
keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android -keypass android
```
6. Descarga el JSON de configuración

### 3. Configurar en la app

Actualmente, la autenticación de Drive se hace en runtime. Para producción, deberías:

1. Colocar `google-services.json` en `app/`
2. Añadir plugin de Google Services en `build.gradle.kts`

## 📄 Generación de Informes

### PDF
- Utiliza **iText7**
- Incluye: datos paciente, resultados, puntuaciones, interpretación detallada
- Se guarda en: `/storage/emulated/0/Android/data/com.sppb/files/output/`

### Excel
- Utiliza **Apache POI**
- Formato XLSX con todos los datos estructurados
- Mismo directorio que el PDF

### Google Drive
- Subida opcional a carpeta configurada
- Requiere autenticación con cuenta de Google
- Sube tanto PDF como Excel

## 🐛 Solución de Problemas

### Error: SDK no encontrado
```
Solución: File → Project Structure → SDK Location → Configura ruta del SDK
```

### Error: Gradle sync failed
```
Solución: File → Invalidate Caches → Invalidate and Restart
```

### Error: Google Drive upload failed
```
Solución: Verifica permisos de Drive en la app, re-autoriza la cuenta de Google
```

### Error: PDF generation failed
```
Solución: Verifica permisos de almacenamiento en Android Settings → Apps → SPPB → Permissions
```

## 🆚 Diferencias con la Versión Python

| Característica | Python/Kivy | Kotlin/Android |
|----------------|-------------|----------------|
| **Plataforma** | Multiplataforma | Solo Android |
| **UI Framework** | Kivy | Jetpack Compose |
| **Tamaño app** | ~20-30 MB | ~10-15 MB |
| **Rendimiento** | Bueno | Excelente |
| **Integración OS** | Limitada | Nativa |
| **Actualizaciones** | Manual | Play Store |
| **Look & Feel** | Custom | Material Design 3 |
| **Offline** | Sí | Sí |

## 📱 Publicación en Play Store

Para publicar la app:

1. **Crear keystore de producción**:
```bash
keytool -genkey -v -keystore sppb-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias sppb
```

2. **Configurar signing** en `app/build.gradle.kts`:
```kotlin
signingConfigs {
    create("release") {
        storeFile = file("../sppb-release-key.jks")
        storePassword = "your_password"
        keyAlias = "sppb"
        keyPassword = "your_password"
    }
}
```

3. **Generar APK/AAB de release**:
```bash
./gradlew bundleRelease
```

4. **Subir a Play Console**:
   - https://play.google.com/console
   - Crear nueva app
   - Subir AAB generado

## 📝 Licencia

Este proyecto es una reimplementación de la aplicación SPPB original en Python/Kivy.

## 👥 Autor

Desarrollado como versión Kotlin/Android de la aplicación SPPB original.

## 📞 Soporte

Para reportar problemas o sugerencias, crea un issue en el repositorio.

---

**Versión**: 1.0.0  
**Última actualización**: Octubre 2025  
**Compatibilidad**: Android 8.0+ (API 26+)


