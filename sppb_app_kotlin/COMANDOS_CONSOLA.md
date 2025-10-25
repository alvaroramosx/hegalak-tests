# 🖥️ Ejecutar SPPB App desde Consola

## ✅ Requisitos Previos

### 1. Instalar JDK 17

**Descargar:**
- https://adoptium.net/temurin/releases/

**Verificar instalación:**
```powershell
java -version
```

Debe mostrar: `openjdk version "17.x.x"`

### 2. Configurar Android SDK

**Opción A: Si tienes Android Studio instalado**

El SDK ya está en:
```
C:\Users\TU_USUARIO\AppData\Local\Android\Sdk
```

**Opción B: Descargar solo el SDK (sin Android Studio)**

1. Descarga Command Line Tools:
   https://developer.android.com/studio#command-line-tools-only

2. Extrae en una carpeta, por ejemplo:
   ```
   C:\Android\cmdline-tools
   ```

3. Instala componentes necesarios:
```powershell
cd C:\Android\cmdline-tools\bin
.\sdkmanager --sdk_root=C:\Android "platform-tools" "platforms;android-34" "build-tools;34.0.0"
```

### 3. Configurar Variables de Entorno

Añade al PATH de Windows:

```
ANDROID_HOME = C:\Users\TU_USUARIO\AppData\Local\Android\Sdk
JAVA_HOME = C:\Program Files\Eclipse Adoptium\jdk-17.x.x

PATH += %ANDROID_HOME%\platform-tools
PATH += %ANDROID_HOME%\tools
PATH += %JAVA_HOME%\bin
```

**En PowerShell (temporal):**
```powershell
$env:ANDROID_HOME = "C:\Users\$env:USERNAME\AppData\Local\Android\Sdk"
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-17.x.x"
$env:Path += ";$env:ANDROID_HOME\platform-tools;$env:JAVA_HOME\bin"
```

---

## 🚀 Comandos para Compilar

### Navegar al proyecto

```powershell
cd sppb_app_kotlin
```

### 1. Limpiar proyecto

```powershell
.\gradlew clean
```

### 2. Compilar APK de Debug

```powershell
.\gradlew assembleDebug
```

**Resultado:**
```
app\build\outputs\apk\debug\app-debug.apk
```

### 3. Compilar APK de Release (sin firmar)

```powershell
.\gradlew assembleRelease
```

**Resultado:**
```
app\build\outputs\apk\release\app-release-unsigned.apk
```

### 4. Compilar Bundle (AAB) para Play Store

```powershell
.\gradlew bundleRelease
```

**Resultado:**
```
app\build\outputs\bundle\release\app-release.aab
```

---

## 📱 Instalar en Dispositivo/Emulador

### Listar dispositivos conectados

```powershell
adb devices
```

Debe mostrar:
```
List of devices attached
emulator-5554   device
```

### Instalar APK

```powershell
adb install app\build\outputs\apk\debug\app-debug.apk
```

O reinstalar (sobrescribir):
```powershell
adb install -r app\build\outputs\apk\debug\app-debug.apk
```

### Desinstalar

```powershell
adb uninstall com.sppb
```

---

## 🎮 Ejecutar la App

### Iniciar la app instalada

```powershell
adb shell am start -n com.sppb/.MainActivity
```

### Ver logs en tiempo real

```powershell
adb logcat -s SPPB:V AndroidRuntime:E
```

---

## 🔄 Workflow Completo (Un Solo Comando)

### Debug: Compilar + Instalar + Ejecutar

```powershell
.\gradlew installDebug && adb shell am start -n com.sppb/.MainActivity
```

---

## 🧪 Testing desde Consola

### Ejecutar tests unitarios

```powershell
.\gradlew test
```

### Ejecutar tests instrumentados (en dispositivo)

```powershell
.\gradlew connectedAndroidTest
```

---

## 📊 Otros Comandos Útiles

### Ver todas las tareas disponibles

```powershell
.\gradlew tasks
```

### Ver dependencias

```powershell
.\gradlew dependencies
```

### Analizar tamaño del APK

```powershell
.\gradlew :app:assembleDebug
# Luego ver en: app\build\outputs\apk\debug\
```

### Limpiar + Compilar

```powershell
.\gradlew clean assembleDebug
```

---

## 🎯 Comandos ADB Útiles

### Ver logs de la app

```powershell
adb logcat | findstr "com.sppb"
```

### Limpiar datos de la app

```powershell
adb shell pm clear com.sppb
```

### Ver info de la app instalada

```powershell
adb shell dumpsys package com.sppb
```

### Tomar screenshot

```powershell
adb shell screencap -p /sdcard/screenshot.png
adb pull /sdcard/screenshot.png
```

### Grabar video de pantalla

```powershell
adb shell screenrecord /sdcard/demo.mp4
# Ctrl+C para detener
adb pull /sdcard/demo.mp4
```

### Ver archivos de la app

```powershell
adb shell run-as com.sppb ls /data/data/com.sppb/files/output/
```

### Descargar archivos generados (PDF/Excel)

```powershell
adb pull /storage/emulated/0/Android/data/com.sppb/files/output/SPPB_*.pdf .
adb pull /storage/emulated/0/Android/data/com.sppb/files/output/SPPB_*.xlsx .
```

---

## 🔧 Iniciar Emulador desde Consola

### Listar emuladores disponibles

```powershell
emulator -list-avds
```

### Iniciar un emulador específico

```powershell
emulator -avd Pixel_5_API_34
```

### Iniciar emulador en background

```powershell
Start-Process emulator -ArgumentList "-avd Pixel_5_API_34"
```

---

## 📦 Crear APK Firmado desde Consola

### 1. Crear keystore (solo una vez)

```powershell
keytool -genkey -v -keystore sppb-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias sppb
```

Te pedirá:
- Contraseña del keystore
- Nombre, organización, etc.

### 2. Configurar signing en build.gradle.kts

Añade en `app/build.gradle.kts`:

```kotlin
android {
    signingConfigs {
        create("release") {
            storeFile = file("../sppb-release-key.jks")
            storePassword = "TU_PASSWORD"
            keyAlias = "sppb"
            keyPassword = "TU_PASSWORD"
        }
    }
    
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            // ...
        }
    }
}
```

### 3. Compilar APK firmado

```powershell
.\gradlew assembleRelease
```

**Resultado:**
```
app\build\outputs\apk\release\app-release.apk
```

---

## 🚨 Solución de Problemas

### Error: "ANDROID_HOME not set"

```powershell
$env:ANDROID_HOME = "C:\Users\$env:USERNAME\AppData\Local\Android\Sdk"
```

### Error: "Could not find or load main class"

```powershell
# Verifica Java
java -version

# Configura JAVA_HOME
$env:JAVA_HOME = "C:\Program Files\Eclipse Adoptium\jdk-17.x.x"
```

### Error: "SDK location not found"

Crea/edita `local.properties`:
```properties
sdk.dir=C:\\Users\\TU_USUARIO\\AppData\\Local\\Android\\Sdk
```

### Error: "daemon not running"

```powershell
adb kill-server
adb start-server
```

### Error: "No devices found"

```powershell
# Verifica conexión
adb devices

# Reinicia adb
adb kill-server && adb start-server
```

---

## 🎬 Script de Automatización

Crea un archivo `build-and-run.ps1`:

```powershell
# Script para compilar e instalar automáticamente

Write-Host "🧹 Limpiando proyecto..." -ForegroundColor Yellow
.\gradlew clean

Write-Host "🔨 Compilando APK..." -ForegroundColor Yellow
.\gradlew assembleDebug

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Compilación exitosa" -ForegroundColor Green
    
    Write-Host "📱 Instalando en dispositivo..." -ForegroundColor Yellow
    adb install -r app\build\outputs\apk\debug\app-debug.apk
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Instalación exitosa" -ForegroundColor Green
        
        Write-Host "🚀 Iniciando app..." -ForegroundColor Yellow
        adb shell am start -n com.sppb/.MainActivity
        
        Write-Host "✅ ¡App ejecutándose!" -ForegroundColor Green
    } else {
        Write-Host "❌ Error al instalar" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Error al compilar" -ForegroundColor Red
}
```

**Ejecutar el script:**
```powershell
.\build-and-run.ps1
```

---

## 📝 Resumen de Comandos Esenciales

```powershell
# COMPILAR
.\gradlew assembleDebug                    # APK debug
.\gradlew assembleRelease                  # APK release
.\gradlew bundleRelease                    # Bundle para Play Store

# INSTALAR Y EJECUTAR
adb install -r app\build\outputs\apk\debug\app-debug.apk
adb shell am start -n com.sppb/.MainActivity

# TODO EN UNO
.\gradlew installDebug && adb shell am start -n com.sppb/.MainActivity

# VER LOGS
adb logcat -s SPPB:V

# DESCARGAR ARCHIVOS GENERADOS
adb pull /storage/emulated/0/Android/data/com.sppb/files/output/ .
```

---

## 🎯 Ventajas de Usar Consola

✅ Más rápido que Android Studio  
✅ Menos uso de memoria  
✅ Fácil de automatizar (CI/CD)  
✅ Scripts de build personalizados  
✅ No requiere IDE pesado  

---

## 📚 Recursos

- **Gradle**: https://docs.gradle.org
- **ADB**: https://developer.android.com/tools/adb
- **Android CLI Tools**: https://developer.android.com/tools

---

**¡Ahora puedes compilar y ejecutar la app completamente desde la consola!** 🚀


