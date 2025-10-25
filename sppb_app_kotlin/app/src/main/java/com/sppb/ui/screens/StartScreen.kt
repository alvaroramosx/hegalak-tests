package com.sppb.ui.screens

import android.Manifest
import android.os.Build
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.google.accompanist.permissions.*
import com.sppb.ui.components.*
import com.sppb.viewmodels.SppbViewModel
import java.time.LocalDate
import java.time.format.DateTimeFormatter

/**
 * Pantalla inicial - Datos del paciente
 * Análoga a StartScreen en screens.py
 */
@OptIn(ExperimentalPermissionsApi::class)
@Composable
fun StartScreen(
    viewModel: SppbViewModel,
    onNext: () -> Unit
) {
    var name by remember { mutableStateOf("") }
    var age by remember { mutableStateOf("") }
    var date by remember { mutableStateOf(LocalDate.now().format(DateTimeFormatter.ISO_LOCAL_DATE)) }
    var therapist by remember { mutableStateOf("") }
    
    // Solicitar permisos de almacenamiento (solo necesario para Android 10 y anteriores)
    val storagePermissions = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
        // Android 13+ no necesita permisos de almacenamiento para archivos de la app
        emptyList()
    } else if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
        // Android 10-12
        listOf(Manifest.permission.READ_EXTERNAL_STORAGE)
    } else {
        // Android 9 y anteriores
        listOf(
            Manifest.permission.READ_EXTERNAL_STORAGE,
            Manifest.permission.WRITE_EXTERNAL_STORAGE
        )
    }
    
    val permissionsState = if (storagePermissions.isNotEmpty()) {
        rememberMultiplePermissionsState(storagePermissions)
    } else {
        null
    }
    
    // Solicitar permisos al iniciar
    LaunchedEffect(Unit) {
        if (permissionsState != null && !permissionsState.allPermissionsGranted) {
            permissionsState.launchMultiplePermissionRequest()
        }
    }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
    ) {
        SppbCard {
            SectionTitle("SPPB · Datos iniciales")
            
            Spacer(modifier = Modifier.height(8.dp))
            
            TextInputField(
                value = name,
                onValueChange = { name = it },
                label = "Nombre del paciente"
            )
            
            NumberInputField(
                value = age,
                onValueChange = { age = it },
                label = "Edad",
                isDecimal = false
            )
            
            TextInputField(
                value = date,
                onValueChange = { date = it },
                label = "Fecha (YYYY-MM-DD)"
            )
            
            TextInputField(
                value = therapist,
                onValueChange = { therapist = it },
                label = "Fisioterapeuta"
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            PrimaryButton(
                text = "Empezar",
                onClick = {
                    if (name.isBlank() || age.isBlank()) {
                        return@PrimaryButton
                    }
                    
                    viewModel.updatePatientName(name)
                    viewModel.updatePatientAge(age)
                    viewModel.updateTestDate(date)
                    viewModel.updateTherapist(therapist)
                    onNext()
                }
            )
        }
    }
}


