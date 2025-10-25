package com.sppb.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

// Colores basados en la app original (tema cálido marrón/beige)
private val primary = Color(0xFF7C2D12)      // Marrón oscuro (primary de la app Python)
private val secondary = Color(0xFFEA580C)    // Naranja/marrón
private val tertiary = Color(0xFF92400E)     // Marrón medio
private val background = Color(0xFFF8F3EA)   // Beige claro (background original)
private val surface = Color(0xFFFFFFFF)      // Blanco
private val onPrimary = Color(0xFFFFFFFF)    // Blanco sobre primary
private val onSecondary = Color(0xFFFFFFFF)  // Blanco sobre secondary
private val onBackground = Color(0xFF1C1B1F) // Casi negro sobre background
private val onSurface = Color(0xFF1C1B1F)    // Casi negro sobre surface

// Colores para estados de fragilidad
val FragilityHigh = Color(0xFFB91C1C)        // Rojo (fragilidad alta)
val FragilityModerate = Color(0xFFEAB308)    // Amarillo (fragilidad moderada)
val FragilityLow = Color(0xFF16A34A)         // Verde (fragilidad baja)

private val LightColorScheme = lightColorScheme(
    primary = primary,
    secondary = secondary,
    tertiary = tertiary,
    background = background,
    surface = surface,
    onPrimary = onPrimary,
    onSecondary = onSecondary,
    onTertiary = onPrimary,
    onBackground = onBackground,
    onSurface = onSurface
)

private val DarkColorScheme = darkColorScheme(
    primary = Color(0xFFFFB4A9),
    secondary = Color(0xFFFFDAD4),
    tertiary = Color(0xFFD7C3A8),
    background = Color(0xFF201A17),
    surface = Color(0xFF2B2420),
    onPrimary = Color(0xFF5F1513),
    onSecondary = Color(0xFF5F1513),
    onTertiary = Color(0xFF462B1D),
    onBackground = Color(0xFFECE0DB),
    onSurface = Color(0xFFECE0DB)
)

@Composable
fun SPPBTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) {
        DarkColorScheme
    } else {
        LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}


