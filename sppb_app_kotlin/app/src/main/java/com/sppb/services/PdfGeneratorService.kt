package com.sppb.services

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import com.itextpdf.kernel.pdf.PdfDocument
import com.itextpdf.kernel.pdf.PdfWriter
import com.itextpdf.layout.Document
import com.itextpdf.layout.element.Image
import com.itextpdf.layout.element.Paragraph
import com.itextpdf.layout.element.Text
import com.itextpdf.layout.properties.HorizontalAlignment
import com.itextpdf.layout.properties.TextAlignment
import com.itextpdf.io.image.ImageDataFactory
import com.sppb.R
import com.sppb.data.models.PatientInfo
import java.io.ByteArrayOutputStream
import java.io.File
import java.io.FileOutputStream
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

/**
 * Servicio para generar PDFs del informe SPPB
 * Análogo a pdf_generator.py usando iText7
 */
class PdfGeneratorService(private val context: Context) {
    
    /**
     * Genera un PDF del informe SPPB
     */
    fun generatePdf(
        outputPath: String,
        patientInfo: PatientInfo,
        results: Map<String, Any?>,
        centerName: String = "Centro de Fisioterapia",
        logoPath: String? = null
    ): String {
        val file = File(outputPath)
        file.parentFile?.mkdirs()
        
        val writer = PdfWriter(FileOutputStream(file))
        val pdf = PdfDocument(writer)
        val document = Document(pdf)
        
        // Encabezado
        addHeader(document, centerName, logoPath)
        
        // Datos del paciente
        document.add(
            Paragraph("Datos del paciente")
                .setBold()
                .setFontSize(12f)
                .setMarginTop(20f)
        )
        
        document.add(Paragraph("Nombre: ${patientInfo.name}").setFontSize(11f))
        document.add(Paragraph("Edad: ${patientInfo.age}").setFontSize(11f))
        document.add(Paragraph("Fecha: ${patientInfo.testDate}").setFontSize(11f))
        document.add(Paragraph("Fisioterapeuta: ${patientInfo.therapist}").setFontSize(11f))
        
        // Equilibrio
        document.add(
            Paragraph("Equilibrio")
                .setBold()
                .setFontSize(12f)
                .setMarginTop(15f)
        )
        
        document.add(Paragraph("Pies juntos (s): ${results["feetTogetherS"]}").setFontSize(11f))
        document.add(Paragraph("Semitándem (s): ${results["semiTandemS"]}").setFontSize(11f))
        document.add(Paragraph("Tándem (s): ${results["tandemS"]}").setFontSize(11f))
        document.add(Paragraph("Puntuación equilibrio: ${results["balanceScore"]} / 4").setFontSize(11f))
        
        // Marcha
        document.add(
            Paragraph("Velocidad de la marcha (4 m)")
                .setBold()
                .setFontSize(12f)
                .setMarginTop(15f)
        )
        
        val gaitUnable = results["gaitUnable"] as? Boolean ?: false
        val gaitTime = if (gaitUnable) "No pudo completar" else "${results["gaitTimeS"]} s"
        document.add(Paragraph("Tiempo: $gaitTime").setFontSize(11f))
        document.add(Paragraph("Puntuación marcha: ${results["gaitScore"]} / 4").setFontSize(11f))
        
        // Silla
        document.add(
            Paragraph("Levantarse de la silla (5 repeticiones)")
                .setBold()
                .setFontSize(12f)
                .setMarginTop(15f)
        )
        
        val chairUnable = results["chairUnable"] as? Boolean ?: false
        val chairTime = if (chairUnable) "No pudo completar" else "${results["chairTimeS"]} s"
        document.add(Paragraph("Tiempo: $chairTime").setFontSize(11f))
        document.add(Paragraph("Puntuación silla: ${results["chairScore"]} / 4").setFontSize(11f))
        
        // Total
        document.add(
            Paragraph("Total SPPB: ${results["total"]} / 12")
                .setBold()
                .setFontSize(13f)
                .setMarginTop(15f)
        )
        
        document.add(
            Paragraph("Conclusión: ${results["interpretation"]}")
                .setFontSize(12f)
        )
        
        // Interpretación detallada
        document.add(
            Paragraph("Interpretación detallada")
                .setBold()
                .setFontSize(12f)
                .setMarginTop(15f)
        )
        
        val balanceScore = results["balanceScore"] as? Int ?: 0
        val gaitScore = results["gaitScore"] as? Int ?: 0
        val chairScore = results["chairScore"] as? Int ?: 0
        val total = results["total"] as? Int ?: 0
        
        val explanations = ExplanationService.longExplanations(
            balanceScore, gaitScore, chairScore, total
        )
        
        listOf("equilibrio", "marcha", "silla", "total").forEach { key ->
            val text = explanations[key] ?: ""
            if (text.isNotEmpty()) {
                document.add(
                    Paragraph(key.replaceFirstChar { it.uppercase() })
                        .setBold()
                        .setFontSize(11f)
                        .setMarginTop(10f)
                )
                document.add(Paragraph(text).setFontSize(11f))
            }
        }
        
        // Pie de página
        val timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm"))
        document.add(
            Paragraph("Generado: $timestamp")
                .setFontSize(9f)
                .setTextAlignment(TextAlignment.RIGHT)
                .setMarginTop(20f)
        )
        
        document.close()
        
        return file.absolutePath
    }
    
    private fun addHeader(document: Document, centerName: String, logoPath: String?) {
        // Cargar logo desde recursos de Android
        try {
            val bitmap = BitmapFactory.decodeResource(context.resources, R.drawable.logo)
            if (bitmap != null) {
                // Convertir bitmap a byte array
                val stream = ByteArrayOutputStream()
                bitmap.compress(Bitmap.CompressFormat.PNG, 100, stream)
                val byteArray = stream.toByteArray()
                
                // Crear imagen para el PDF
                val imageData = ImageDataFactory.create(byteArray)
                val logo = Image(imageData)
                    .scaleToFit(480f, 240f)  // Ajustar tamaño del logo
                    .setHorizontalAlignment(HorizontalAlignment.RIGHT)
                    .setFixedPosition(
                        document.pdfDocument.defaultPageSize.width - 140f,  // Posición X (derecha)
                        document.pdfDocument.defaultPageSize.height - 80f,  // Posición Y (arriba)
                        120f  // Ancho
                    )
                
                document.add(logo)
            }
        } catch (e: Exception) {
            // Si falla cargar el logo, continuar sin él
            e.printStackTrace()
        }
        
        // Título
        document.add(
            Paragraph(centerName)
                .setBold()
                .setFontSize(16f)
                .setMarginTop(10f)
        )
        
        document.add(
            Paragraph("Informe de SPPB (Short Physical Performance Battery)")
                .setFontSize(12f)
        )
    }
}


