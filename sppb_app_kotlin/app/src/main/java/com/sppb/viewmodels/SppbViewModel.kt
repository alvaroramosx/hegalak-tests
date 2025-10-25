package com.sppb.viewmodels

import android.app.Application
import android.content.ContentValues
import android.content.Context
import android.os.Build
import android.os.Environment
import android.provider.MediaStore
import android.util.Log
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.sppb.data.models.*
import com.sppb.services.DriveUploaderService
import com.sppb.services.ExcelExporterService
import com.sppb.services.PdfGeneratorService
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import java.io.File
import java.io.FileInputStream
import java.time.LocalDate
import java.time.format.DateTimeFormatter

private const val TAG = "SppbViewModel"

/**
 * ViewModel principal de la aplicación SPPB
 * Gestiona el estado y la lógica de negocio
 */
class SppbViewModel(application: Application) : AndroidViewModel(application) {
    
    private val context: Context = application.applicationContext
    
    // Servicios
    private val pdfGenerator = PdfGeneratorService(context)
    private val excelExporter = ExcelExporterService(context)
    private val driveUploader = DriveUploaderService(context)
    
    // Estado de la sesión
    private val _sessionState = MutableStateFlow(SessionState())
    val sessionState: StateFlow<SessionState> = _sessionState.asStateFlow()
    
    // Estado de la UI
    private val _statusMessage = MutableStateFlow("")
    val statusMessage: StateFlow<String> = _statusMessage.asStateFlow()
    
    private val _isLoading = MutableStateFlow(false)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()
    
    // Configuración
    private val _centerName = MutableStateFlow("Centro de Fisioterapia")
    val centerName: StateFlow<String> = _centerName.asStateFlow()
    
    private val _driveFolderUrl = MutableStateFlow("")
    val driveFolderUrl: StateFlow<String> = _driveFolderUrl.asStateFlow()
    
    private val _therapistName = MutableStateFlow("")
    val therapistName: StateFlow<String> = _therapistName.asStateFlow()
    
    // ========================================================================
    // Métodos para actualizar datos del paciente
    // ========================================================================
    
    fun updatePatientName(name: String) {
        _sessionState.value = _sessionState.value.copy(name = name)
    }
    
    fun updatePatientAge(age: String) {
        _sessionState.value = _sessionState.value.copy(age = age)
    }
    
    fun updateTestDate(date: String) {
        _sessionState.value = _sessionState.value.copy(testDate = date)
    }
    
    fun updateTherapist(therapist: String) {
        _sessionState.value = _sessionState.value.copy(therapist = therapist)
        _therapistName.value = therapist
    }
    
    // ========================================================================
    // Métodos para actualizar equilibrio
    // ========================================================================
    
    fun updateFeetTogether(seconds: Float) {
        _sessionState.value = _sessionState.value.copy(feetTogetherS = seconds)
    }
    
    fun updateSemiTandem(seconds: Float) {
        _sessionState.value = _sessionState.value.copy(semiTandemS = seconds)
    }
    
    fun updateTandem(seconds: Float) {
        _sessionState.value = _sessionState.value.copy(tandemS = seconds)
    }
    
    // ========================================================================
    // Métodos para actualizar marcha
    // ========================================================================
    
    fun updateGaitTime1(seconds: Float?) {
        _sessionState.value = _sessionState.value.copy(gaitTime1S = seconds)
    }
    
    fun updateGaitUnable1(unable: Boolean) {
        _sessionState.value = _sessionState.value.copy(gaitUnable1 = unable)
    }
    
    fun updateGaitTime2(seconds: Float?) {
        _sessionState.value = _sessionState.value.copy(gaitTime2S = seconds)
    }
    
    fun updateGaitUnable2(unable: Boolean) {
        _sessionState.value = _sessionState.value.copy(gaitUnable2 = unable)
    }
    
    // ========================================================================
    // Métodos para actualizar silla
    // ========================================================================
    
    fun updateChairPretest(unable: Boolean) {
        _sessionState.value = _sessionState.value.copy(chairPretestUnable = unable)
    }
    
    fun updateChairTime(seconds: Float?) {
        _sessionState.value = _sessionState.value.copy(chairTimeS = seconds)
    }
    
    fun updateChairUnable(unable: Boolean) {
        _sessionState.value = _sessionState.value.copy(chairUnable = unable)
    }
    
    // ========================================================================
    // Cálculo de puntuaciones
    // ========================================================================
    
    fun getCurrentScores(): SppbScores {
        return _sessionState.value.currentScores()
    }
    
    // ========================================================================
    // Generación y exportación de informes
    // ========================================================================
    
    fun generateAndExportReport() {
        viewModelScope.launch {
            try {
                _isLoading.value = true
                _statusMessage.value = "Generando informe..."
                
                val state = _sessionState.value
                
                // Validar datos
                if (state.name.isBlank() || state.age.isBlank()) {
                    _statusMessage.value = "❗ Introduce nombre y edad del paciente"
                    _isLoading.value = false
                    return@launch
                }
                
                Log.d(TAG, "Iniciando generación de informe para: ${state.name}")
                
                // Preparar información del paciente
                val patientInfo = PatientInfo(
                    name = state.name,
                    age = state.age.toIntOrNull() ?: 0,
                    testDate = try {
                        LocalDate.parse(state.testDate)
                    } catch (e: Exception) {
                        Log.w(TAG, "Error parseando fecha, usando fecha actual", e)
                        LocalDate.now()
                    },
                    therapist = state.therapist
                )
                
                // Obtener puntuaciones
                val inputs = state.toInputs()
                val scores = computeScores(inputs)
                
                // Preparar resultados
                val results = mapOf<String, Any?>(
                    "feetTogetherS" to inputs.feetTogetherS,
                    "semiTandemS" to inputs.semiTandemS,
                    "tandemS" to inputs.tandemS,
                    "gaitTimeS" to inputs.gaitTimeS,
                    "gaitUnable" to inputs.gaitUnable,
                    "chairTimeS" to inputs.chairTimeS,
                    "chairUnable" to inputs.chairUnable,
                    "balanceScore" to scores.balanceScore,
                    "gaitScore" to scores.gaitScore,
                    "chairScore" to scores.chairScore,
                    "total" to scores.total,
                    "interpretation" to scores.interpretation
                )
                
                // Generar nombre de archivo
                val timestamp = System.currentTimeMillis()
                val baseName = "SPPB_${state.name}_${timestamp}"
                
                // Directorio de salida
                val outputDir = context.getExternalFilesDir(null)?.resolve("output")
                outputDir?.mkdirs()
                
                if (outputDir == null) {
                    throw Exception("No se pudo crear el directorio de salida")
                }
                
                Log.d(TAG, "Directorio de salida: ${outputDir.absolutePath}")
                
                val pdfPath = outputDir.resolve("$baseName.pdf").absolutePath
                val xlsxPath = outputDir.resolve("$baseName.xlsx").absolutePath
                
                // Generar PDF
                try {
                    _statusMessage.value = "Generando PDF..."
                    Log.d(TAG, "Generando PDF en: $pdfPath")
                    pdfGenerator.generatePdf(
                        outputPath = pdfPath,
                        patientInfo = patientInfo,
                        results = results,
                        centerName = _centerName.value
                    )
                    Log.d(TAG, "PDF generado exitosamente")
                } catch (e: Exception) {
                    Log.e(TAG, "Error generando PDF", e)
                    throw Exception("Error generando PDF: ${e.message}")
                }
                
                // Generar Excel
                try {
                    _statusMessage.value = "Generando Excel..."
                    Log.d(TAG, "Generando Excel en: $xlsxPath")
                    excelExporter.exportToExcel(
                        outputPath = xlsxPath,
                        patientInfo = patientInfo,
                        results = results
                    )
                    Log.d(TAG, "Excel generado exitosamente")
                } catch (e: Exception) {
                    Log.e(TAG, "Error generando Excel", e)
                    throw Exception("Error generando Excel: ${e.message}")
                }
                
                // Copiar archivos a la carpeta de Descargas
                _statusMessage.value = "Guardando en Descargas..."
                try {
                    val pdfFile = File(pdfPath)
                    val xlsxFile = File(xlsxPath)
                    
                    copyFileToDownloads(pdfFile, "$baseName.pdf")
                    copyFileToDownloads(xlsxFile, "$baseName.xlsx")
                    
                    Log.d(TAG, "Archivos copiados a Descargas exitosamente")
                } catch (e: Exception) {
                    Log.e(TAG, "Error copiando a Descargas", e)
                    throw Exception("Error guardando en Descargas: ${e.message}")
                }
                
                // Subir a Drive si está configurado
                val driveUrl = _driveFolderUrl.value
                if (driveUrl.isNotBlank()) {
                    val folderId = driveUploader.extractFolderIdFromUrl(driveUrl)
                    if (folderId != null) {
                        _statusMessage.value = "Subiendo a Drive..."
                        Log.d(TAG, "Subiendo archivos a Drive, folder ID: $folderId")
                        try {
                            driveUploader.uploadFileToDrive(pdfPath, folderId)
                            driveUploader.uploadFileToDrive(xlsxPath, folderId)
                            _statusMessage.value = "✅ Archivos guardados en Descargas y subidos a Drive"
                            Log.d(TAG, "Archivos subidos a Drive exitosamente")
                        } catch (e: Exception) {
                            Log.e(TAG, "Error subiendo a Drive", e)
                            _statusMessage.value = "✅ Archivos guardados en Descargas"
                        }
                    } else {
                        _statusMessage.value = "✅ Archivos guardados en Descargas"
                        Log.d(TAG, "URL de Drive inválida, archivos guardados en Descargas")
                    }
                } else {
                    _statusMessage.value = "✅ Archivos guardados en Descargas"
                    Log.d(TAG, "Archivos guardados en Descargas")
                }
                
            } catch (e: Exception) {
                Log.e(TAG, "Error en generateAndExportReport", e)
                _statusMessage.value = "❗ Error: ${e.message}"
                e.printStackTrace()
            } finally {
                _isLoading.value = false
            }
        }
    }
    
    /**
     * Copia un archivo a la carpeta de Descargas pública
     */
    private fun copyFileToDownloads(sourceFile: File, fileName: String): String {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            // Android 10+ (API 29+): Usar MediaStore
            val resolver = context.contentResolver
            val contentValues = ContentValues().apply {
                put(MediaStore.MediaColumns.DISPLAY_NAME, fileName)
                put(MediaStore.MediaColumns.MIME_TYPE, getMimeType(fileName))
                put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS)
                put(MediaStore.MediaColumns.IS_PENDING, 1)
            }
            
            val uri = resolver.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, contentValues)
            
            if (uri != null) {
                resolver.openOutputStream(uri)?.use { outputStream ->
                    FileInputStream(sourceFile).use { inputStream ->
                        inputStream.copyTo(outputStream)
                    }
                }
                
                // Marcar como completo para que sea visible
                val updateValues = ContentValues().apply {
                    put(MediaStore.MediaColumns.IS_PENDING, 0)
                }
                resolver.update(uri, updateValues, null, null)
                
                Log.d(TAG, "Archivo copiado a Descargas vía MediaStore: $fileName")
                Log.d(TAG, "URI: $uri")
                "Descargas/$fileName"
            } else {
                throw Exception("No se pudo crear archivo en Descargas")
            }
        } else {
            // Android 9 y anteriores: Usar directorio público de Descargas
            @Suppress("DEPRECATION")
            val downloadsDir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
            downloadsDir.mkdirs()
            val destFile = File(downloadsDir, fileName)
            
            sourceFile.copyTo(destFile, overwrite = true)
            
            // Notificar al MediaScanner para que el archivo sea visible
            @Suppress("DEPRECATION")
            android.media.MediaScannerConnection.scanFile(
                context,
                arrayOf(destFile.absolutePath),
                arrayOf(getMimeType(fileName))
            ) { path, uri ->
                Log.d(TAG, "MediaScanner: Archivo escaneado: $path -> $uri")
            }
            
            Log.d(TAG, "Archivo copiado a Descargas: ${destFile.absolutePath}")
            destFile.absolutePath
        }
    }
    
    /**
     * Obtiene el MIME type de un archivo según su extensión
     */
    private fun getMimeType(fileName: String): String {
        return when {
            fileName.endsWith(".pdf") -> "application/pdf"
            fileName.endsWith(".xlsx") -> "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            else -> "application/octet-stream"
        }
    }
    
    // ========================================================================
    // Utilidades
    // ========================================================================
    
    fun resetSession() {
        _sessionState.value = SessionState()
        _statusMessage.value = ""
    }
    
    fun clearStatusMessage() {
        _statusMessage.value = ""
    }
    
    fun setCenterName(name: String) {
        _centerName.value = name
    }
    
    fun setDriveFolderUrl(url: String) {
        _driveFolderUrl.value = url
    }
}


