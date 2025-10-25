package com.sppb.services

/**
 * Servicio de explicaciones para el test SPPB
 * Genera textos interpretativos según las puntuaciones obtenidas
 */
object ExplanationService {
    
    /**
     * Genera un resumen corto para mostrar en pantalla
     */
    fun shortSummary(balanceScore: Int, gaitScore: Int, chairScore: Int, total: Int): String {
        val interpretation = when {
            total <= 4 -> "Fragilidad alta"
            total <= 8 -> "Fragilidad moderada"
            else -> "Fragilidad baja"
        }
        
        return buildString {
            appendLine("Equilibrio: $balanceScore/4")
            appendLine("Marcha: $gaitScore/4")
            appendLine("Silla: $chairScore/4")
            appendLine("Total: $total/12")
            appendLine()
            appendLine("$interpretation")
        }
    }
    
    /**
     * Genera explicaciones detalladas para el PDF
     */
    fun longExplanations(
        balanceScore: Int,
        gaitScore: Int,
        chairScore: Int,
        total: Int
    ): Map<String, String> {
        return mapOf(
            "equilibrio" to explainBalance(balanceScore),
            "marcha" to explainGait(gaitScore),
            "silla" to explainChair(chairScore),
            "total" to explainTotal(total)
        )
    }
    
    private fun explainBalance(score: Int): String {
        return when (score) {
            0 -> "Equilibrio muy limitado. No puede mantener la posición de pies juntos durante 10 segundos. " +
                 "Se recomienda entrenamiento específico de equilibrio estático y prevención de caídas."
            
            1 -> "Equilibrio limitado. Mantiene pies juntos 10s pero no semitándem. " +
                 "Requiere trabajo de equilibrio progresivo con ejercicios de base de sustentación reducida."
            
            2 -> "Equilibrio moderado. Mantiene semitándem 10s pero tándem < 3s. " +
                 "Se sugiere continuar con ejercicios de equilibrio en tándem y superficies inestables."
            
            3 -> "Buen equilibrio. Mantiene tándem entre 3-10 segundos. " +
                 "Continuar con mantenimiento y desafíos progresivos de equilibrio dinámico."
            
            4 -> "Excelente equilibrio estático. Mantiene tándem completo 10 segundos. " +
                 "Nivel óptimo para su grupo de edad. Mantener actividad regular."
            
            else -> "Puntuación fuera de rango (0-4)."
        }
    }
    
    private fun explainGait(score: Int): String {
        return when (score) {
            0 -> "No puede completar la prueba de marcha. Movilidad muy limitada. " +
                 "Se recomienda valoración médica y programa de rehabilitación intensivo."
            
            1 -> "Velocidad de marcha muy reducida (> 8.70 s para 4 metros). " +
                 "Indica alto riesgo de caídas y pérdida de independencia. " +
                 "Necesario programa de fortalecimiento de miembros inferiores y entrenamiento de marcha."
            
            2 -> "Velocidad de marcha moderadamente reducida (6.21-8.70 s). " +
                 "Se observa limitación funcional. Trabajo de resistencia, fuerza y técnica de marcha recomendado."
            
            3 -> "Velocidad de marcha aceptable (4.83-6.20 s). " +
                 "Capacidad funcional preservada. Mantener programa de ejercicio regular."
            
            4 -> "Velocidad de marcha óptima (< 4.82 s). " +
                 "Excelente capacidad funcional. Continuar con actividad física habitual."
            
            else -> "Puntuación fuera de rango (0-4)."
        }
    }
    
    private fun explainChair(score: Int): String {
        return when (score) {
            0 -> "No puede levantarse de la silla sin ayuda de los brazos o completar 5 repeticiones. " +
                 "Debilidad significativa en miembros inferiores. " +
                 "Programa de fortalecimiento de cuádriceps, glúteos y trabajo funcional prioritario."
            
            1 -> "Tiempo elevado para 5 levantamientos (≥ 16.70 s). " +
                 "Fuerza de miembros inferiores reducida. " +
                 "Entrenamiento de fuerza y potencia necesario para mejorar independencia funcional."
            
            2 -> "Tiempo moderado para 5 levantamientos (13.70-16.69 s). " +
                 "Fuerza aceptable pero mejorable. " +
                 "Ejercicios de fortalecimiento y transferencias recomendados."
            
            3 -> "Buen tiempo para 5 levantamientos (11.20-13.69 s). " +
                 "Buena fuerza de miembros inferiores. Mantener programa de ejercicio."
            
            4 -> "Excelente tiempo para 5 levantamientos (≤ 11.19 s). " +
                 "Fuerza óptima de miembros inferiores. Continuar con actividad regular."
            
            else -> "Puntuación fuera de rango (0-4)."
        }
    }
    
    private fun explainTotal(total: Int): String {
        return when {
            total <= 4 -> {
                "FRAGILIDAD ALTA (puntuación 0-4): El paciente presenta un alto nivel de fragilidad física. " +
                "Existe riesgo elevado de caídas, hospitalización y pérdida de independencia. " +
                "Se recomienda intervención fisioterapéutica intensiva con programa multicomponente que incluya: " +
                "entrenamiento de equilibrio específico, fortalecimiento muscular progresivo, " +
                "trabajo de resistencia cardiovascular y entrenamiento funcional de actividades de la vida diaria. " +
                "Es importante también la valoración médica y nutricional completa."
            }
            
            total <= 8 -> {
                "FRAGILIDAD MODERADA (puntuación 5-8): El paciente presenta fragilidad física moderada. " +
                "Existe riesgo de deterioro funcional progresivo si no se interviene. " +
                "Se recomienda programa de ejercicio terapéutico que incluya: " +
                "entrenamiento de equilibrio y marcha, ejercicios de fortalecimiento de miembros inferiores, " +
                "trabajo aeróbico moderado y actividades funcionales. " +
                "Seguimiento regular para prevenir mayor deterioro y mejorar capacidad funcional."
            }
            
            else -> {
                "FRAGILIDAD BAJA (puntuación 9-12): El paciente presenta bajo nivel de fragilidad física. " +
                "La capacidad funcional está relativamente preservada. " +
                "Se recomienda mantener un programa de ejercicio físico regular que incluya: " +
                "actividad aeróbica, fortalecimiento muscular, ejercicios de equilibrio y flexibilidad. " +
                "Seguimiento periódico para asegurar el mantenimiento de la capacidad funcional " +
                "y promover un estilo de vida activo y saludable."
            }
        }
    }
}


