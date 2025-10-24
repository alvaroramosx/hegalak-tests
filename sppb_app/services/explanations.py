from __future__ import annotations

from typing import Dict


def _level_from_score(score: int, max_score: int) -> str:
	if score <= 0:
		return "muy bajo"
	if score >= max_score:
		return "muy alto"
	mid = max_score // 2
	if score <= mid - 1:
		return "bajo"
	if score == mid:
		return "medio"
	return "alto"


def long_explanations(balance: int, gait: int, chair: int, total: int) -> Dict[str, str]:
	# Textos largos para el informe PDF. Mantener neutrales y accionables.
	texts: Dict[str, str] = {}

	# Equilibrio (0-4)
	if balance == 0:
		texts["balance"] = (
			"Equilibrio 0/4: el paciente no mantiene posturas básicas (pies juntos/semitándem/tándem). "
			"Sugiere inestabilidad significativa. Recomendado: entrenamiento de apoyo amplio, ejercicios de transferencia y trabajo de base de sustentación." 
		)
	elif balance == 1:
		texts["balance"] = (
			"Equilibrio 1/4: mantiene solo la postura más sencilla. "
			"Indica riesgo de pérdida de equilibrio en bipedestación prolongada. Sugerir progresión gradual a semitándem con apoyos de seguridad."
		)
	elif balance == 2:
		texts["balance"] = (
			"Equilibrio 2/4: tolera hasta semitándem pero no la posición en tándem 10 s. "
			"Planificar tareas de control postural estático y dinámico y reducción progresiva de apoyos."
		)
	elif balance == 3:
		texts["balance"] = (
			"Equilibrio 3/4: buen control postural, con ligera limitación en tándem. "
			"Mantener y progresar con tareas de alcance y cambios de apoyo."
		)
	else:
		texts["balance"] = (
			"Equilibrio 4/4: control postural óptimo en posturas probadas. "
			"Continuar con entrenamiento de prevención de caídas y tareas duales para mantener capacidad."
		)

	# Marcha (0-4)
	if gait == 0:
		texts["gait"] = (
			"Marcha 0/4: no completó la prueba o velocidad muy lenta. "
			"Riesgo elevado de limitación funcional. Recomendado: trabajo de fuerza de MMII, práctica de marcha con ayudas si precisa y educación en seguridad."
		)
	elif gait == 1:
		texts["gait"] = (
			"Marcha 1/4: velocidad marcadamente reducida (> 8,70 s/4 m). "
			"Priorizar fuerza y cadencia, con series cortas y descansos."
		)
	elif gait == 2:
		texts["gait"] = (
			"Marcha 2/4: velocidad baja (6,21–8,70 s/4 m). "
			"Progresar distancia y ritmo; introducir virajes y doble tarea cuando sea seguro."
		)
	elif gait == 3:
		texts["gait"] = (
			"Marcha 3/4: velocidad funcional (4,82–6,20 s/4 m). "
			"Mantener y trabajar resistencia aeróbica ligera y cambios de ritmo."
		)
	else:
		texts["gait"] = (
			"Marcha 4/4: velocidad adecuada para la comunidad (< 4,82 s/4 m). "
			"Reforzar resistencia y variabilidad de marcha para prevención."
		)

	# Silla (0-4)
	if chair == 0:
		texts["chair"] = (
			"Silla 0/4: no pudo completar 5 levantamientos o > 60 s. "
			"Sugiere debilidad de extensores de rodilla y cadera. Trabajar sentadillas asistidas, despegue y control excéntrico, con progresión segura."
		)
	elif chair == 1:
		texts["chair"] = (
			"Silla 1/4: tiempo ≥ 16,70 s. "
			"Enfocar fortalecimiento y práctica de levantarse con técnica, series cortas y descansos."
		)
	elif chair == 2:
		texts["chair"] = (
			"Silla 2/4: tiempo 13,70–16,69 s. "
			"Progresar fuerza y velocidad, elevando superficie a menor, y aumentando repeticiones."
		)
	elif chair == 3:
		texts["chair"] = (
			"Silla 3/4: tiempo 11,20–13,69 s. "
			"Mantener fuerza y trabajo de potencia baja con seguridad."
		)
	else:
		texts["chair"] = (
			"Silla 4/4: < 11,19 s. "
			"Capacidad adecuada; mantener programas de fuerza y prevenir desentrenamiento."
		)

	# Total (0-12)
	if total <= 4:
		texts["total"] = (
			f"Total {total}/12 (fragilidad alta): riesgo funcional elevado. Recomendado plan intensivo y supervisado centrado en fuerza, equilibrio y marcha, con revisión de ayudas técnicas."
		)
	elif total <= 8:
		texts["total"] = (
			f"Total {total}/12 (fragilidad moderada): capacidad intermedia; priorizar progresión de resistencia y fuerza, prevención de caídas y actividad diaria."
		)
	else:
		texts["total"] = (
			f"Total {total}/12 (fragilidad baja): buen rendimiento global; mantener actividad física habitual, variar tareas e incorporar retos seguros."
		)

	return texts


def short_summary(balance: int, gait: int, chair: int, total: int) -> str:
	b_txt = _level_from_score(balance, 4)
	g_txt = _level_from_score(gait, 4)
	c_txt = _level_from_score(chair, 4)
	if total <= 4:
		glob = "riesgo global alto"
	elif total <= 8:
		glob = "riesgo global moderado"
	else:
		glob = "buen rendimiento global"
	return (
		f"Equilibrio {b_txt}, marcha {g_txt}, silla {c_txt}; {glob}."
	)


