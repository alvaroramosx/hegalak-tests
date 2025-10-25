package com.sppb.data.models

import java.time.LocalDate

/**
 * Información del paciente
 */
data class PatientInfo(
    val name: String,
    val age: Int,
    val testDate: LocalDate,
    val therapist: String = ""
)

/**
 * Datos de entrada del test SPPB
 */
data class SppbInputs(
    // Balance: segundos mantenidos en cada postura (0-10s)
    val feetTogetherS: Float,
    val semiTandemS: Float,
    val tandemS: Float,
    
    // Velocidad de marcha: tiempo para caminar 4 metros (segundos)
    val gaitTimeS: Float? = null,
    val gaitUnable: Boolean = false,
    
    // Levantarse de la silla: tiempo para 5 repeticiones (segundos)
    val chairTimeS: Float? = null,
    val chairUnable: Boolean = false
)

/**
 * Puntuaciones del test SPPB
 */
data class SppbScores(
    val balanceScore: Int,
    val gaitScore: Int,
    val chairScore: Int
) {
    val total: Int
        get() = balanceScore + gaitScore + chairScore
    
    val interpretation: String
        get() = interpretTotal(total)
}

/**
 * Estado de la sesión actual
 */
data class SessionState(
    // Datos del paciente
    var name: String = "",
    var age: String = "",
    var testDate: String = "",
    var therapist: String = "",
    
    // Equilibrio
    var feetTogetherS: Float = 0f,
    var semiTandemS: Float = 0f,
    var tandemS: Float = 0f,
    
    // Marcha
    var gaitTime1S: Float? = null,
    var gaitUnable1: Boolean = false,
    var gaitTime2S: Float? = null,
    var gaitUnable2: Boolean = false,
    
    // Silla
    var chairPretestUnable: Boolean = false,
    var chairTimeS: Float? = null,
    var chairUnable: Boolean = false
) {
    fun toInputs(): SppbInputs {
        // Seleccionar el mejor tiempo de marcha
        val gaitTimes = listOfNotNull(
            if (!gaitUnable1) gaitTime1S else null,
            if (!gaitUnable2) gaitTime2S else null
        )
        val bestGaitTime = gaitTimes.minOrNull()
        val gaitUnable = gaitTimes.isEmpty()
        
        // Manejar la incapacidad de silla
        val chairTime = if (chairPretestUnable || chairUnable) null else chairTimeS
        val chairUnableResult = chairPretestUnable || chairUnable
        
        return SppbInputs(
            feetTogetherS = feetTogetherS,
            semiTandemS = semiTandemS,
            tandemS = tandemS,
            gaitTimeS = bestGaitTime,
            gaitUnable = gaitUnable,
            chairTimeS = chairTime,
            chairUnable = chairUnableResult
        )
    }
    
    fun currentScores(): SppbScores {
        return computeScores(toInputs())
    }
}

// ============================================================================
// Funciones de cálculo de puntuaciones (lógica del test SPPB)
// ============================================================================

/**
 * Limita un valor opcional entre un mínimo y máximo
 */
fun clampSeconds(value: Float?, minimum: Float = 0f, maximum: Float = 9999f): Float? {
    return value?.coerceIn(minimum, maximum)
}

/**
 * Calcula la puntuación de equilibrio (0-4) según las reglas estándar del SPPB
 */
fun scoreBalance(feetTogetherS: Float, semiTandemS: Float, tandemS: Float): Int {
    val f = clampSeconds(feetTogetherS, 0f, 10f) ?: 0f
    val s = clampSeconds(semiTandemS, 0f, 10f) ?: 0f
    val t = clampSeconds(tandemS, 0f, 10f) ?: 0f
    
    return when {
        f < 10f -> 0
        s < 10f -> 1
        t < 3f -> 2
        t < 10f -> 3
        else -> 4
    }
}

/**
 * Calcula la puntuación de velocidad de marcha (0-4)
 */
fun scoreGait(timeSeconds: Float?, unable: Boolean = false): Int {
    if (unable) return 0
    
    val t = clampSeconds(timeSeconds) ?: return 0
    if (t <= 0f) return 0
    
    return when {
        t > 8.70f -> 1
        t >= 6.21f -> 2
        t >= 4.83f -> 3
        else -> 4
    }
}

/**
 * Calcula la puntuación de levantarse de la silla (0-4)
 */
fun scoreChair(timeSeconds: Float?, unable: Boolean = false): Int {
    if (unable) return 0
    
    val t = clampSeconds(timeSeconds) ?: return 0
    if (t <= 0f) return 0
    
    return when {
        t >= 16.70f -> 1
        t >= 13.70f -> 2
        t >= 11.20f -> 3
        else -> 4
    }
}

/**
 * Interpreta la puntuación total
 */
fun interpretTotal(totalScore: Int): String {
    return when {
        totalScore <= 4 -> "Fragilidad alta"
        totalScore <= 8 -> "Fragilidad moderada"
        else -> "Fragilidad baja"
    }
}

/**
 * Calcula todas las puntuaciones a partir de los inputs
 */
fun computeScores(inputs: SppbInputs): SppbScores {
    val balance = scoreBalance(inputs.feetTogetherS, inputs.semiTandemS, inputs.tandemS)
    val gait = scoreGait(inputs.gaitTimeS, inputs.gaitUnable)
    val chair = scoreChair(inputs.chairTimeS, inputs.chairUnable)
    
    return SppbScores(
        balanceScore = balance,
        gaitScore = gait,
        chairScore = chair
    )
}

