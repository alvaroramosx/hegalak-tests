# 🚀 Guía de Inicio Rápido - SPPB App Kotlin

## ⚡ 5 Pasos para Ejecutar la App

### 1️⃣ Verificar Requisitos

```bash
# Verifica que tienes instalado:
- Android Studio Hedgehog (2023.1.1) o superior
- JDK 17 o superior
```

### 2️⃣ Abrir el Proyecto

1. Abre **Android Studio**
2. **File** → **Open**
3. Navega a la carpeta `sppb_app_kotlin`
4. Haz clic en **OK**

### 3️⃣ Esperar Sincronización

- Gradle sincronizará automáticamente (puede tardar 2-5 minutos la primera vez)
- Verás el progreso en la parte inferior de Android Studio
- ✅ Cuando termine, verás "Gradle sync finished"

### 4️⃣ Crear Emulador (si no tienes uno)

1. **Tools** → **Device Manager**
2. **Create Device**
3. Selecciona **Pixel 5**
4. System Image: **API 34 (UpsideDownCake)**
5. **Finish**

### 5️⃣ Ejecutar

1. Asegúrate de que el emulador/dispositivo esté seleccionado en la barra superior
2. Haz clic en el botón ▶️ **Run** (o presiona **Shift+F10**)
3. Espera a que compile e instale
4. ✅ ¡La app se abrirá automáticamente!

---

## 📱 Prueba Rápida

Una vez que la app esté ejecutándose:

### Test de Ejemplo

1. **Pantalla inicial**:
   - Nombre: `Juan Pérez`
   - Edad: `75`
   - Fecha: (deja la actual)
   - Fisioterapeuta: `Dr. García`
   - Haz clic en **Empezar**

2. **Pies Juntos**:
   - Tiempo: `10`
   - Verás que se marca automáticamente "Mantuvo 10 segundos"
   - **Siguiente**

3. **Semitándem**:
   - Tiempo: `10`
   - **Siguiente**

4. **Tándem**:
   - Tiempo: `5`
   - Verás que se marca "3-9.99 segundos"
   - **Siguiente**

5. **Marcha**:
   - Tiempo 1: `5.5`
   - Tiempo 2: `6.0`
   - Verás la categoría calculada automáticamente
   - **Siguiente**

6. **Silla**:
   - Deja pre-test sin marcar
   - Tiempo: `12`
   - Verás la categoría calculada
   - **Finalizar**

7. **Resumen**:
   - Verás los gráficos circulares con las puntuaciones
   - **Total esperado**: 9/12 (Fragilidad baja)
   - Haz clic en **Enviar a Drive / Exportar**
   - Los archivos PDF y Excel se generarán en `/storage/emulated/0/Android/data/com.sppb/files/output/`

---

## 🔧 Solución Rápida de Problemas

### ❌ Error: SDK not found

```
Solución:
File → Project Structure → SDK Location
Configura la ruta: C:\Users\TuUsuario\AppData\Local\Android\sdk
```

### ❌ Error: Gradle sync failed

```
Solución:
File → Invalidate Caches → Invalidate and Restart
```

### ❌ Error: No emulator available

```
Solución:
Tools → Device Manager → Create Device → Pixel 5 → API 34
```

### ❌ App crashes al exportar

```
Solución:
Permisos no concedidos. En el emulador:
Settings → Apps → SPPB → Permissions → Enable all
```

---

## 🎯 Flujo Completo de la App

```
┌─────────────────┐
│  INICIO         │ ← Datos del paciente
│  (Start)        │
└────────┬────────┘
         ↓
┌─────────────────┐
│  EQUILIBRIO     │
│  1A: Pies juntos│ → Tiempo 0-10s
└────────┬────────┘
         ↓
┌─────────────────┐
│  EQUILIBRIO     │
│  1B: Semitándem │ → Tiempo 0-10s
└────────┬────────┘
         ↓
┌─────────────────┐
│  EQUILIBRIO     │
│  1C: Tándem     │ → Tiempo 0-10s
└────────┬────────┘
         ↓
┌─────────────────┐
│  MARCHA         │
│  4 metros       │ → 2 mediciones (mejor tiempo)
└────────┬────────┘
         ↓
┌─────────────────┐
│  SILLA          │
│  5 levantamientos│ → Tiempo en segundos
└────────┬────────┘
         ↓
┌─────────────────┐
│  RESUMEN        │ ← Gráficos + Puntuación total
│  (Summary)      │ → Exportar PDF/Excel/Drive
└─────────────────┘
```

---

## 📊 Interpretación Rápida

### Puntuaciones:
- **Equilibrio**: 0-4 puntos
- **Marcha**: 0-4 puntos  
- **Silla**: 0-4 puntos
- **TOTAL**: 0-12 puntos

### Interpretación:
- **0-4 puntos**: 🔴 Fragilidad alta
- **5-8 puntos**: 🟡 Fragilidad moderada
- **9-12 puntos**: 🟢 Fragilidad baja

---

## 📂 Archivos Generados

### Ubicación:
```
/storage/emulated/0/Android/data/com.sppb/files/output/
```

### Archivos:
- `SPPB_[nombre]_[timestamp].pdf` - Informe completo
- `SPPB_[nombre]_[timestamp].xlsx` - Datos en Excel

### Para ver los archivos:

**En emulador:**
1. Abre la app "Files" o "Downloads"
2. Navega a `Android/data/com.sppb/files/output/`

**Desde Android Studio:**
1. View → Tool Windows → Device File Explorer
2. Navega a `/data/data/com.sppb/files/output/`
3. Click derecho → Save As...

---

## 🎨 Personalización Rápida

### Cambiar colores:

Edita `app/src/main/res/values/colors.xml`:

```xml
<color name="primary">#7C2D12</color>      <!-- Marrón principal -->
<color name="secondary">#EA580C</color>    <!-- Naranja -->
<color name="background">#F8F3EA</color>   <!-- Beige fondo -->
```

### Cambiar nombre del centro:

Edita `app/src/main/java/com/sppb/viewmodels/SppbViewModel.kt`:

```kotlin
private val _centerName = MutableStateFlow("Tu Centro de Fisioterapia")
```

---

## 📱 Instalar en Dispositivo Real

### Paso 1: Habilitar modo desarrollador

En tu Android:
1. **Ajustes** → **Acerca del teléfono**
2. Toca 7 veces en **Número de compilación**
3. Verás "Ahora eres desarrollador"

### Paso 2: Habilitar depuración USB

1. **Ajustes** → **Sistema** → **Opciones de desarrollador**
2. Activa **Depuración USB**

### Paso 3: Conectar y ejecutar

1. Conecta el dispositivo por USB
2. Acepta la autorización en el dispositivo
3. En Android Studio, selecciona tu dispositivo en la barra superior
4. Haz clic en **Run** ▶️

---

## ⚙️ Compilar APK para Distribución

### Debug APK (para pruebas):

```bash
./gradlew assembleDebug
```

APK en: `app/build/outputs/apk/debug/app-debug.apk`

### Release APK (para producción):

1. Crea un keystore:
```bash
keytool -genkey -v -keystore sppb-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias sppb
```

2. Compila:
```bash
./gradlew assembleRelease
```

APK en: `app/build/outputs/apk/release/app-release.apk`

---

## 🎓 Aprende Más

### Documentación del proyecto:
- 📖 `README.md` - Documentación completa
- 🔄 `EQUIVALENCIAS_PYTHON_KOTLIN.md` - Comparación con Python
- 📋 `PROYECTO_COMPLETO.md` - Resumen del proyecto

### Recursos externos:
- [Android Developers](https://developer.android.com)
- [Jetpack Compose](https://developer.android.com/jetpack/compose)
- [Kotlin](https://kotlinlang.org)

---

## ✅ Checklist de Inicio

- [ ] Android Studio instalado
- [ ] Proyecto abierto en Android Studio
- [ ] Gradle sincronizado correctamente
- [ ] Emulador/dispositivo configurado
- [ ] App ejecutándose
- [ ] Test de prueba completado
- [ ] PDF y Excel generados correctamente

---

## 🎉 ¡Listo!

Si llegaste hasta aquí y todo funcionó, **¡felicidades!** 🎊

Tienes una aplicación Android completa y funcional para realizar tests SPPB.

**Próximos pasos sugeridos:**
1. Probar con diferentes pacientes
2. Personalizar el logo y colores
3. Configurar Google Drive (opcional)
4. Compilar APK para distribución

---

**¿Problemas?** Consulta `README.md` para más detalles o revisa la sección de solución de problemas.

**¿Todo bien?** ¡Empieza a usar la app! 🚀


