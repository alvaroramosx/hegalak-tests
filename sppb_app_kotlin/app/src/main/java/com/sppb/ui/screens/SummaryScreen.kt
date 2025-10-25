package com.sppb.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Divider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import com.sppb.services.ExplanationService
import com.sppb.ui.components.*
import com.sppb.viewmodels.SppbViewModel

/**
 * Pantalla de resumen final
 * Muestra las puntuaciones y permite exportar el informe
 */
@Composable
fun SummaryScreen(
    viewModel: SppbViewModel,
    onNewTest: () -> Unit
) {
    val statusMessage by viewModel.statusMessage.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()
    val scores = viewModel.getCurrentScores()
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
    ) {
        SppbCard {
            SectionTitle("Resumen final")
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Gráficos de puntuación
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                ScoreGauge(
                    title = "Equilibrio",
                    score = scores.balanceScore,
                    maxScore = 4
                )
                
                ScoreGauge(
                    title = "Marcha",
                    score = scores.gaitScore,
                    maxScore = 4
                )
                
                ScoreGauge(
                    title = "Silla",
                    score = scores.chairScore,
                    maxScore = 4
                )
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Puntuación total
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.Center
            ) {
                ScoreGauge(
                    title = "Total",
                    score = scores.total,
                    maxScore = 12,
                    modifier = Modifier.width(150.dp)
                )
            }
            
            Spacer(modifier = Modifier.height(24.dp))
            Divider()
            Spacer(modifier = Modifier.height(16.dp))
            
            // Resumen textual
            Text(
                text = ExplanationService.shortSummary(
                    scores.balanceScore,
                    scores.gaitScore,
                    scores.chairScore,
                    scores.total
                ),
                style = MaterialTheme.typography.bodyLarge,
                modifier = Modifier.fillMaxWidth(),
                textAlign = TextAlign.Center
            )
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Mensaje de estado
            if (statusMessage.isNotBlank()) {
                StatusMessage(message = statusMessage)
            }
            
            // Botón de exportar
            PrimaryButton(
                text = if (isLoading) "Generando..." else "Enviar a Drive / Exportar",
                onClick = {
                    viewModel.generateAndExportReport()
                },
                enabled = !isLoading
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            // Botón para nuevo test
            SecondaryButton(
                text = "Nuevo test",
                onClick = {
                    viewModel.resetSession()
                    onNewTest()
                }
            )
        }
    }
}


