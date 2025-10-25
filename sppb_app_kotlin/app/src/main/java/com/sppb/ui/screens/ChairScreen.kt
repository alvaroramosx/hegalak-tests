package com.sppb.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Divider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.sppb.ui.components.*
import com.sppb.viewmodels.SppbViewModel

/**
 * Pantalla 3: Levantarse de la silla
 */
@Composable
fun ChairScreen(
    viewModel: SppbViewModel,
    onFinish: () -> Unit,
    onBack: () -> Unit
) {
    var pretestUnable by remember { mutableStateOf(false) }
    var time by remember { mutableStateOf("") }
    var unable by remember { mutableStateOf(false) }
    
    // Calcular categoría
    val category = remember(pretestUnable, time, unable) {
        when {
            pretestUnable || unable -> "No puede completar o tarda > 60 s (0 puntos)"
            else -> {
                val t = time.toFloatOrNull()
                when {
                    t == null || t > 60f -> "No puede completar o tarda > 60 s (0 puntos)"
                    t >= 16.70f -> "≥ 16.70 s (1 punto)"
                    t >= 13.70f -> "13.70-16.69 s (2 puntos)"
                    t >= 11.20f -> "11.20-13.69 s (3 puntos)"
                    else -> "≤ 11.19 s (4 puntos)"
                }
            }
        }
    }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
    ) {
        SppbCard {
            SectionTitle("3. Levantarse de la silla")
            
            Text(
                text = "El paciente debe levantarse y sentarse 5 veces consecutivas lo más rápido posible, sin usar los brazos",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Pre-test
            Text(
                text = "Pre-test",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary
            )
            
            LabeledCheckbox(
                checked = pretestUnable,
                onCheckedChange = {
                    pretestUnable = it
                    if (it) {
                        time = ""
                        unable = false
                    }
                },
                label = "¿No puede levantarse sin apoyarse con los brazos?"
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            Divider()
            Spacer(modifier = Modifier.height(16.dp))
            
            // Tiempo de 5 repeticiones
            Text(
                text = "Prueba de 5 levantamientos",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary
            )
            
            NumberInputField(
                value = time,
                onValueChange = { time = it },
                label = "Tiempo para 5 repeticiones (segundos)",
                enabled = !pretestUnable && !unable
            )
            
            LabeledCheckbox(
                checked = unable,
                onCheckedChange = {
                    unable = it
                    if (it) time = ""
                },
                label = "No pudo completar las 5 repeticiones",
                enabled = !pretestUnable
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            Divider()
            Spacer(modifier = Modifier.height(16.dp))
            
            // Categoría calculada
            Text(
                text = "Categoría de puntuación",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary
            )
            
            Text(
                text = category,
                style = MaterialTheme.typography.bodyLarge,
                color = MaterialTheme.colorScheme.onSurface
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                SecondaryButton(
                    text = "Anterior",
                    onClick = onBack,
                    modifier = Modifier.weight(1f)
                )
                
                PrimaryButton(
                    text = "Finalizar",
                    onClick = {
                        viewModel.updateChairPretest(pretestUnable)
                        viewModel.updateChairTime(time.toFloatOrNull())
                        viewModel.updateChairUnable(unable)
                        onFinish()
                    },
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}


