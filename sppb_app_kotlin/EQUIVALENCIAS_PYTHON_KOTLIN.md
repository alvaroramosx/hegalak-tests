# Equivalencias: Python/Kivy ↔ Kotlin/Android

Este documento muestra las equivalencias entre la aplicación original en Python/Kivy y la nueva versión en Kotlin/Android.

## 📂 Estructura de Archivos

| Python/Kivy | Kotlin/Android | Propósito |
|-------------|----------------|-----------|
| `sppb_app/models/sppb_logic.py` | `com.sppb.data.models.SppbModels.kt` | Lógica de cálculo SPPB |
| `sppb_app/services/pdf_generator.py` | `com.sppb.services.PdfGeneratorService.kt` | Generación de PDF |
| `sppb_app/services/excel_exporter.py` | `com.sppb.services.ExcelExporterService.kt` | Exportación Excel |
| `sppb_app/services/drive_uploader.py` | `com.sppb.services.DriveUploaderService.kt` | Subida a Drive |
| `sppb_app/services/explanations.py` | `com.sppb.services.ExplanationService.kt` | Textos interpretativos |
| `sppb_app/ui/screens.py` | `com.sppb.ui.screens/*.kt` | Pantallas de la app |
| `sppb_app/ui/state.py` | `com.sppb.viewmodels.SppbViewModel.kt` | Gestión de estado |
| `sppb_app/main.py` | `com.sppb.MainActivity.kt` | Punto de entrada |
| `sppb_app/config.py` | Constantes en código / Resources | Configuración |

## 🎨 Frameworks y Librerías

### UI Framework

| Python/Kivy | Kotlin/Android |
|-------------|----------------|
| **Kivy** | **Jetpack Compose** |
| Declarativo con .kv files | Declarativo con @Composable |
| Widget-based | Composable functions |
| Custom rendering | Material Design 3 |

#### Ejemplo de Widget/Composable:

**Python/Kivy:**
```python
class PrimaryButton(Button):
    pass

# En .kv:
<PrimaryButton>:
    size_hint_y: None
    height: 56
    background_color: rgba('#7C2D12')
```

**Kotlin/Compose:**
```kotlin
@Composable
fun PrimaryButton(text: String, onClick: () -> Unit) {
    Button(
        onClick = onClick,
        modifier = Modifier.height(56.dp),
        colors = ButtonDefaults.buttonColors(
            containerColor = Color(0xFF7C2D12)
        )
    ) {
        Text(text)
    }
}
```

### Librerías de Documentos

| Funcionalidad | Python | Kotlin/Android |
|---------------|--------|----------------|
| **PDF** | ReportLab | iText7 |
| **Excel** | openpyxl | Apache POI |

#### Generación de PDF:

**Python (ReportLab):**
```python
from reportlab.pdfgen import canvas
c = canvas.Canvas(output_path)
c.drawString(x, y, "Texto")
c.save()
```

**Kotlin (iText7):**
```kotlin
val writer = PdfWriter(FileOutputStream(file))
val pdf = PdfDocument(writer)
val document = Document(pdf)
document.add(Paragraph("Texto"))
document.close()
```

### Google Drive

| Python | Kotlin/Android |
|--------|----------------|
| `google-api-python-client` | `google-api-services-drive` |
| `google-auth` | `play-services-auth` |
| OAuth2 manual | GoogleSignIn integrado |

## 📊 Modelos de Datos

### Classes/Data Classes

**Python:**
```python
from dataclasses import dataclass

@dataclass
class PatientInfo:
    name: str
    age: int
    test_date: date
```

**Kotlin:**
```kotlin
data class PatientInfo(
    val name: String,
    val age: Int,
    val testDate: LocalDate
)
```

### Funciones de Cálculo

**Python:**
```python
def score_balance(feet_together_s: float, semi_tandem_s: float, tandem_s: float) -> int:
    f = clamp_seconds(feet_together_s, 0, 10) or 0
    if f < 10:
        return 0
    # ...
    return 4
```

**Kotlin:**
```kotlin
fun scoreBalance(feetTogetherS: Float, semiTandemS: Float, tandemS: Float): Int {
    val f = clampSeconds(feetTogetherS, 0f, 10f) ?: 0f
    return when {
        f < 10f -> 0
        // ...
        else -> 4
    }
}
```

## 🎯 Gestión de Estado

### Python (Kivy)

**Estado mutable en clase:**
```python
class SessionState:
    name: str = ""
    age: str = ""
    feet_together_s: float = 0.0
    # ...
```

**Actualización:**
```python
state.name = "Juan"
state.feet_together_s = 10.0
```

### Kotlin (StateFlow + ViewModel)

**Estado reactivo:**
```kotlin
class SppbViewModel : ViewModel() {
    private val _sessionState = MutableStateFlow(SessionState())
    val sessionState: StateFlow<SessionState> = _sessionState.asStateFlow()
    
    fun updatePatientName(name: String) {
        _sessionState.value = _sessionState.value.copy(name = name)
    }
}
```

**Observación en UI:**
```kotlin
@Composable
fun MyScreen(viewModel: SppbViewModel) {
    val state by viewModel.sessionState.collectAsState()
    Text(text = state.name)
}
```

## 🖥️ Pantallas y Navegación

### Python/Kivy

**ScreenManager:**
```python
class WizardRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sm = ScreenManager()
        self.sm.add_widget(StartScreen(self))
        self.sm.add_widget(BalanceFeetScreen(self))
        
    def goto(self, name: str):
        self.sm.current = name
```

### Kotlin/Compose

**NavHost:**
```kotlin
@Composable
fun SppbApp() {
    val navController = rememberNavController()
    
    NavHost(navController, startDestination = "start") {
        composable("start") {
            StartScreen(onNext = { navController.navigate("balance_feet") })
        }
        composable("balance_feet") {
            BalanceFeetScreen(onNext = { navController.navigate("balance_semi") })
        }
    }
}
```

## 🎨 Temas y Estilos

### Python/Kivy

**theme.kv:**
```
<PrimaryButton@Button>:
    background_color: rgba('#7C2D12')
    color: rgba('#FFFFFF')
    font_size: 16sp
```

### Kotlin/Compose

**Theme.kt:**
```kotlin
private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF7C2D12),
    onPrimary = Color(0xFFFFFFFF),
    background = Color(0xFFF8F3EA)
)

@Composable
fun SPPBTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = LightColorScheme,
        typography = Typography,
        content = content
    )
}
```

## 🔄 Operaciones Asíncronas

### Python

**Threads/asyncio:**
```python
from threading import Thread

def upload_in_background():
    # operación larga
    upload_file_to_drive(path, url)

thread = Thread(target=upload_in_background)
thread.start()
```

### Kotlin

**Coroutines:**
```kotlin
viewModelScope.launch {
    try {
        _isLoading.value = true
        driveUploader.uploadFileToDrive(path, folderId)
        _statusMessage.value = "✅ Subido correctamente"
    } catch (e: Exception) {
        _statusMessage.value = "❗ Error: ${e.message}"
    } finally {
        _isLoading.value = false
    }
}
```

## 📁 Acceso a Archivos

### Python

```python
from pathlib import Path

output_dir = Path("output")
output_dir.mkdir(parents=True, exist_ok=True)
pdf_path = output_dir / f"SPPB_{name}_{timestamp}.pdf"
```

### Kotlin/Android

```kotlin
val outputDir = context.getExternalFilesDir(null)?.resolve("output")
outputDir?.mkdirs()
val pdfPath = outputDir?.resolve("SPPB_${name}_${timestamp}.pdf")?.absolutePath
```

## 🎯 Componentes UI Equivalentes

| Python/Kivy | Kotlin/Compose | Propósito |
|-------------|----------------|-----------|
| `Label` | `Text` | Mostrar texto |
| `TextInput` | `TextField` / `OutlinedTextField` | Entrada de texto |
| `Button` | `Button` | Botón clickeable |
| `CheckBox` | `Checkbox` | Casilla de verificación |
| `ProgressBar` | `LinearProgressIndicator` | Barra de progreso |
| `BoxLayout` | `Column` / `Row` | Layout vertical/horizontal |
| `GridLayout` | `LazyVerticalGrid` | Layout en cuadrícula |
| `ScrollView` | `LazyColumn` / `verticalScroll` | Scroll vertical |
| Custom Widget | `@Composable function` | Componente personalizado |

## 🔢 Tipos de Datos

| Python | Kotlin | Notas |
|--------|--------|-------|
| `str` | `String` | Texto |
| `int` | `Int` | Entero |
| `float` | `Float` | Decimal |
| `bool` | `Boolean` | Booleano |
| `None` | `null` | Valor nulo |
| `Optional[T]` | `T?` | Tipo nullable |
| `List[T]` | `List<T>` | Lista |
| `Dict[K, V]` | `Map<K, V>` | Diccionario/Mapa |
| `date` | `LocalDate` | Fecha |
| `datetime` | `LocalDateTime` | Fecha y hora |

## 🚀 Ventajas de cada Versión

### Python/Kivy

✅ Multiplataforma (Windows, Mac, Linux, Android, iOS)  
✅ Desarrollo rápido  
✅ Fácil de empaquetar  
✅ No requiere Android Studio  
✅ Mismo código para todas las plataformas  

❌ Apps más grandes (~20-30 MB)  
❌ Menor integración con el OS  
❌ UI custom (no nativa)  

### Kotlin/Android

✅ Rendimiento nativo excelente  
✅ Integración perfecta con Android  
✅ Apps más pequeñas (~10-15 MB)  
✅ Material Design 3 nativo  
✅ Distribución vía Play Store  
✅ Actualizaciones automáticas  

❌ Solo Android  
❌ Requiere Android Studio  
❌ Código específico de plataforma  

## 📝 Resumen

La versión Kotlin/Android es una **reimplementación completa** de la aplicación Python/Kivy, manteniendo:

- ✅ **Misma lógica de cálculo** SPPB
- ✅ **Mismo flujo de usuario**
- ✅ **Mismas funcionalidades** (PDF, Excel, Drive)
- ✅ **Estética similar** (colores, diseño)
- ✅ **Mismas interpretaciones** fisioterapéuticas

Pero optimizada para Android con:

- 🚀 Mejor rendimiento
- 📱 Integración nativa
- 🎨 Material Design 3
- 💾 Menor tamaño
- 🔄 Arquitectura MVVM moderna

---

**Conclusión**: Ambas versiones son completamente funcionales. Elige según tu plataforma objetivo:
- **Python/Kivy** → Multiplataforma, desarrollo rápido
- **Kotlin/Android** → Solo Android, experiencia nativa óptima


