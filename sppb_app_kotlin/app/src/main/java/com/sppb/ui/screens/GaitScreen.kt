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
 * Pantalla 2: Velocidad de marcha (4 metros)
 */
@Composable
fun GaitScreen(
    viewModel: SppbViewModel,
    onNext: () -> Unit,
    onBack: () -> Unit
) {
    var time1 by remember { mutableStateOf("") }
    var unable1 by remember { mutableStateOf(false) }
    var time2 by remember { mutableStateOf("") }
    var unable2 by remember { mutableStateOf(false) }
    
    // Calcular mejor tiempo y categoría
    val bestTime = remember(time1, time2, unable1, unable2) {
        val t1 = if (!unable1) time1.toFloatOrNull() else null
        val t2 = if (!unable2) time2.toFloatOrNull() else null
        listOfNotNull(t1, t2).minOrNull()
    }
    
    val category = remember(bestTime) {
        when {
            bestTime == null -> "No pudo realizar la prueba"
            bestTime > 8.70f -> "> 8.70 s (1 punto)"
            bestTime >= 6.21f -> "6.21-8.70 s (2 puntos)"
            bestTime >= 4.82f -> "4.82-6.20 s (3 puntos)"
            else -> "< 4.82 s (4 puntos)"
        }
    }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
    ) {
        SppbCard {
            SectionTitle("2. Velocidad de marcha (4 m)")
            
            Text(
                text = "El paciente debe caminar 4 metros a velocidad habitual. Se realizan dos mediciones y se toma el mejor tiempo.",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Primera medición
            Text(
                text = "Primera medición",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary
            )
            
            NumberInputField(
                value = time1,
                onValueChange = { time1 = it },
                label = "Tiempo 1 (segundos)",
                enabled = !unable1
            )
            
            LabeledCheckbox(
                checked = unable1,
                onCheckedChange = {
                    unable1 = it
                    if (it) time1 = ""
                },
                label = "No pudo realizar la primera medición"
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            Divider()
            Spacer(modifier = Modifier.height(16.dp))
            
            // Segunda medición
            Text(
                text = "Segunda medición",
                style = MaterialTheme.typography.titleMedium,
                color = MaterialTheme.colorScheme.primary
            )
            
            NumberInputField(
                value = time2,
                onValueChange = { time2 = it },
                label = "Tiempo 2 (segundos)",
                enabled = !unable2
            )
            
            LabeledCheckbox(
                checked = unable2,
                onCheckedChange = {
                    unable2 = it
                    if (it) time2 = ""
                },
                label = "No pudo realizar la segunda medición"
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
                    text = "Siguiente",
                    onClick = {
                        viewModel.updateGaitTime1(time1.toFloatOrNull())
                        viewModel.updateGaitUnable1(unable1)
                        viewModel.updateGaitTime2(time2.toFloatOrNull())
                        viewModel.updateGaitUnable2(unable2)
                        onNext()
                    },
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}


