package com.sppb.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.sppb.ui.components.*
import com.sppb.viewmodels.SppbViewModel

/**
 * Pantalla 1A: Equilibrio - Pies juntos
 */
@Composable
fun BalanceFeetScreen(
    viewModel: SppbViewModel,
    onNext: () -> Unit,
    onBack: () -> Unit
) {
    var time by remember { mutableStateOf("") }
    var optionYes by remember { mutableStateOf(false) }
    var optionNo by remember { mutableStateOf(false) }
    var optionNA by remember { mutableStateOf(false) }
    
    // Auto-marcar opciones según el tiempo
    LaunchedEffect(time) {
        val t = time.toFloatOrNull()
        if (t != null) {
            optionNA = false
            if (t >= 10f) {
                optionYes = true
                optionNo = false
            } else {
                optionYes = false
                optionNo = true
            }
        }
    }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
    ) {
        SppbCard {
            SectionTitle("1A. Pies juntos")
            
            Text(
                text = "El paciente debe mantener los pies juntos durante 10 segundos",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            NumberInputField(
                value = time,
                onValueChange = { time = it },
                label = "Tiempo mantenido (segundos)"
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            LabeledCheckbox(
                checked = optionYes,
                onCheckedChange = {
                    optionYes = it
                    if (it) {
                        optionNo = false
                        optionNA = false
                    }
                },
                label = "Mantuvo 10 segundos (1 punto)"
            )
            
            LabeledCheckbox(
                checked = optionNo,
                onCheckedChange = {
                    optionNo = it
                    if (it) {
                        optionYes = false
                        optionNA = false
                    }
                },
                label = "No mantuvo 10 segundos (0 puntos)"
            )
            
            LabeledCheckbox(
                checked = optionNA,
                onCheckedChange = {
                    optionNA = it
                    if (it) {
                        optionYes = false
                        optionNo = false
                    }
                },
                label = "No intentado (0 puntos)"
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
                        val t = time.toFloatOrNull()
                        val seconds = when {
                            t != null -> t.coerceIn(0f, 10f)
                            optionYes -> 10f
                            else -> 0f
                        }
                        viewModel.updateFeetTogether(seconds)
                        onNext()
                    },
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}

/**
 * Pantalla 1B: Equilibrio - Semitándem
 */
@Composable
fun BalanceSemiScreen(
    viewModel: SppbViewModel,
    onNext: () -> Unit,
    onBack: () -> Unit
) {
    var time by remember { mutableStateOf("") }
    var optionYes by remember { mutableStateOf(false) }
    var optionNo by remember { mutableStateOf(false) }
    var optionNA by remember { mutableStateOf(false) }
    
    LaunchedEffect(time) {
        val t = time.toFloatOrNull()
        if (t != null) {
            optionNA = false
            if (t >= 10f) {
                optionYes = true
                optionNo = false
            } else {
                optionYes = false
                optionNo = true
            }
        }
    }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
    ) {
        SppbCard {
            SectionTitle("1B. Semitándem")
            
            Text(
                text = "El paciente debe mantener la posición de semitándem durante 10 segundos",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            NumberInputField(
                value = time,
                onValueChange = { time = it },
                label = "Tiempo mantenido (segundos)"
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            LabeledCheckbox(
                checked = optionYes,
                onCheckedChange = {
                    optionYes = it
                    if (it) {
                        optionNo = false
                        optionNA = false
                    }
                },
                label = "Mantuvo 10 segundos (1 punto)"
            )
            
            LabeledCheckbox(
                checked = optionNo,
                onCheckedChange = {
                    optionNo = it
                    if (it) {
                        optionYes = false
                        optionNA = false
                    }
                },
                label = "No mantuvo 10 segundos (0 puntos)"
            )
            
            LabeledCheckbox(
                checked = optionNA,
                onCheckedChange = {
                    optionNA = it
                    if (it) {
                        optionYes = false
                        optionNo = false
                    }
                },
                label = "No intentado (0 puntos)"
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
                        val t = time.toFloatOrNull()
                        val seconds = when {
                            t != null -> t.coerceIn(0f, 10f)
                            optionYes -> 10f
                            else -> 0f
                        }
                        viewModel.updateSemiTandem(seconds)
                        onNext()
                    },
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}

/**
 * Pantalla 1C: Equilibrio - Tándem
 */
@Composable
fun BalanceTandemScreen(
    viewModel: SppbViewModel,
    onNext: () -> Unit,
    onBack: () -> Unit
) {
    var time by remember { mutableStateOf("") }
    var option10 by remember { mutableStateOf(false) }
    var option3to9 by remember { mutableStateOf(false) }
    var optionLt3 by remember { mutableStateOf(false) }
    var optionNA by remember { mutableStateOf(false) }
    
    LaunchedEffect(time) {
        val t = time.toFloatOrNull()
        if (t != null) {
            optionNA = false
            when {
                t >= 10f -> {
                    option10 = true
                    option3to9 = false
                    optionLt3 = false
                }
                t >= 3f -> {
                    option10 = false
                    option3to9 = true
                    optionLt3 = false
                }
                t > 0f -> {
                    option10 = false
                    option3to9 = false
                    optionLt3 = true
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
            SectionTitle("1C. Tándem")
            
            Text(
                text = "El paciente debe mantener la posición de tándem completo",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            NumberInputField(
                value = time,
                onValueChange = { time = it },
                label = "Tiempo mantenido (segundos)"
            )
            
            Spacer(modifier = Modifier.height(8.dp))
            
            LabeledCheckbox(
                checked = option10,
                onCheckedChange = {
                    option10 = it
                    if (it) {
                        option3to9 = false
                        optionLt3 = false
                        optionNA = false
                    }
                },
                label = "Mantuvo 10 segundos (2 puntos)"
            )
            
            LabeledCheckbox(
                checked = option3to9,
                onCheckedChange = {
                    option3to9 = it
                    if (it) {
                        option10 = false
                        optionLt3 = false
                        optionNA = false
                    }
                },
                label = "Mantuvo 3-9.99 segundos (1 punto)"
            )
            
            LabeledCheckbox(
                checked = optionLt3,
                onCheckedChange = {
                    optionLt3 = it
                    if (it) {
                        option10 = false
                        option3to9 = false
                        optionNA = false
                    }
                },
                label = "Menos de 3 segundos (0 puntos)"
            )
            
            LabeledCheckbox(
                checked = optionNA,
                onCheckedChange = {
                    optionNA = it
                    if (it) {
                        option10 = false
                        option3to9 = false
                        optionLt3 = false
                    }
                },
                label = "No intentado (0 puntos)"
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
                        val t = time.toFloatOrNull()
                        val seconds = when {
                            t != null -> when {
                                t >= 10f -> 10f
                                t >= 3f -> 5f
                                t > 0f -> 2f
                                else -> 0f
                            }
                            option10 -> 10f
                            option3to9 -> 5f
                            optionLt3 -> 2f
                            else -> 0f
                        }
                        viewModel.updateTandem(seconds)
                        onNext()
                    },
                    modifier = Modifier.weight(1f)
                )
            }
        }
    }
}


