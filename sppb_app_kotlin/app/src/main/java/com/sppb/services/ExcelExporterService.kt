package com.sppb.services

import android.content.Context
import com.sppb.data.models.PatientInfo
import org.apache.poi.ss.usermodel.WorkbookFactory
import org.apache.poi.xssf.usermodel.XSSFWorkbook
import java.io.File
import java.io.FileOutputStream

/**
 * Servicio para exportar datos a Excel
 * Análogo a excel_exporter.py usando Apache POI
 */
class ExcelExporterService(private val context: Context) {
    
    /**
     * Exporta los datos del test SPPB a un archivo Excel
     */
    fun exportToExcel(
        outputPath: String,
        patientInfo: PatientInfo,
        results: Map<String, Any?>
    ): String {
        val file = File(outputPath)
        file.parentFile?.mkdirs()
        
        val workbook = XSSFWorkbook()
        val sheet = workbook.createSheet("SPPB")
        
        val rows = listOf(
            listOf("Fecha", patientInfo.testDate.toString()),
            listOf("Nombre", patientInfo.name),
            listOf("Edad", patientInfo.age.toString()),
            emptyList(),
            listOf("Equilibrio"),
            listOf("Pies juntos (s)", results["feetTogetherS"]?.toString() ?: ""),
            listOf("Semitándem (s)", results["semiTandemS"]?.toString() ?: ""),
            listOf("Tándem (s)", results["tandemS"]?.toString() ?: ""),
            listOf("Puntuación equilibrio", results["balanceScore"]?.toString() ?: ""),
            emptyList(),
            listOf("Marcha 4 m"),
            listOf(
                "Tiempo (s)",
                if (results["gaitUnable"] as? Boolean == true) "No pudo"
                else results["gaitTimeS"]?.toString() ?: ""
            ),
            listOf("Puntuación marcha", results["gaitScore"]?.toString() ?: ""),
            emptyList(),
            listOf("Levantarse de la silla (5x)"),
            listOf(
                "Tiempo (s)",
                if (results["chairUnable"] as? Boolean == true) "No pudo"
                else results["chairTimeS"]?.toString() ?: ""
            ),
            listOf("Puntuación silla", results["chairScore"]?.toString() ?: ""),
            emptyList(),
            listOf("Total SPPB", results["total"]?.toString() ?: ""),
            listOf("Conclusión", results["interpretation"]?.toString() ?: "")
        )
        
        // Escribir datos
        rows.forEachIndexed { rowIndex, rowData ->
            val row = sheet.createRow(rowIndex)
            rowData.forEachIndexed { colIndex, cellData ->
                val cell = row.createCell(colIndex)
                cell.setCellValue(cellData.toString())
            }
        }
        
        // Ajustar anchos de columna manualmente (autoSizeColumn no funciona en Android)
        // El ancho se especifica en unidades de 1/256 del ancho de un carácter
        sheet.setColumnWidth(0, 35 * 256)  // ~35 caracteres para la primera columna
        sheet.setColumnWidth(1, 25 * 256)  // ~25 caracteres para la segunda columna
        
        // Guardar archivo
        FileOutputStream(file).use { outputStream ->
            workbook.write(outputStream)
        }
        
        workbook.close()
        
        return file.absolutePath
    }
}


