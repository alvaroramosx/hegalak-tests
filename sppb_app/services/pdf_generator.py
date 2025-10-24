from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from .explanations import long_explanations

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def _resolve_logo_path(logo_path: Optional[str]) -> Optional[str]:
	"""Return a best-effort absolute path to a logo image if available."""
	candidates = []
	if logo_path:
		candidates.append(Path(logo_path))
	# Buscar logo por defecto en assets
	default_asset = Path(__file__).resolve().parents[1] / "assets" / "logo.png"
	candidates.append(default_asset)
	for p in candidates:
		try:
			if p.exists():
				return str(p)
		except Exception:
			pass
	return None


def _draw_header(c: canvas.Canvas, logo_path: Optional[str], center_name: str) -> None:
	width, height = A4
	resolved = _resolve_logo_path(logo_path)
	if resolved:
		c.drawImage(resolved, 2 * cm, height - 3.5 * cm, width=3 * cm, height=3 * cm, preserveAspectRatio=True, mask='auto')
	else:
		c.setStrokeColor(colors.black)
		c.rect(2 * cm, height - 3.5 * cm, 3 * cm, 3 * cm)
		c.drawString(2.2 * cm, height - 2.2 * cm, "LOGO")

	c.setFont("Helvetica-Bold", 16)
	c.drawString(6 * cm, height - 2.0 * cm, center_name)
	c.setFont("Helvetica", 12)
	c.drawString(6 * cm, height - 2.7 * cm, "Informe de SPPB (Short Physical Performance Battery)")


def _draw_wrapped_text(c: canvas.Canvas, text: str, x: float, y: float, width_chars: int = 100, line_height: float = 0.5 * cm) -> float:
	"""Dibuja un párrafo simple con salto de línea aproximado por número de caracteres. Devuelve la nueva coordenada y."""
	while text:
		line = text[:width_chars]
		if len(text) > width_chars and " " in text[:width_chars]:
			idx = line.rfind(" ")
			if idx != -1:
				line = line[:idx]
		c.drawString(x, y, line)
		text = text[len(line):].lstrip()
		y -= line_height
	return y


def generate_pdf(
	output_path: str,
	patient_info: Dict[str, str],
	results: Dict[str, object],
	logo_path: Optional[str] = None,
	center_name: str = "Centro de Fisioterapia",
) -> str:
	"""Create the SPPB PDF report. Returns the absolute path to the file."""
	output_file = Path(output_path)
	output_file.parent.mkdir(parents=True, exist_ok=True)

	c = canvas.Canvas(str(output_file), pagesize=A4)
	width, height = A4

	_draw_header(c, logo_path, center_name=center_name)

	y = height - 4.5 * cm
	c.setFont("Helvetica-Bold", 12)
	c.drawString(2 * cm, y, "Datos del paciente")
	c.setFont("Helvetica", 11)
	y -= 0.7 * cm
	c.drawString(2 * cm, y, f"Nombre: {patient_info.get('name', '')}")
	y -= 0.6 * cm
	c.drawString(2 * cm, y, f"Edad: {patient_info.get('age', '')}")
	y -= 0.6 * cm
	c.drawString(2 * cm, y, f"Fecha: {patient_info.get('date', '')}")
	y -= 0.6 * cm
	c.drawString(2 * cm, y, f"Fisioterapeuta: {patient_info.get('therapist', '')}")

	y -= 1.0 * cm
	c.setFont("Helvetica-Bold", 12)
	c.drawString(2 * cm, y, "Equilibrio")
	c.setFont("Helvetica", 11)
	y -= 0.6 * cm
	c.drawString(2 * cm, y, f"Pies juntos (s): {results.get('feet_together_s', '')}")
	y -= 0.5 * cm
	c.drawString(2 * cm, y, f"Semitándem (s): {results.get('semi_tandem_s', '')}")
	y -= 0.5 * cm
	c.drawString(2 * cm, y, f"Tándem (s): {results.get('tandem_s', '')}")
	y -= 0.5 * cm
	balance_score = int(results.get('balance_score', 0) or 0)
	c.drawString(2 * cm, y, f"Puntuación equilibrio: {balance_score} / 4")

	y -= 0.9 * cm
	c.setFont("Helvetica-Bold", 12)
	c.drawString(2 * cm, y, "Velocidad de la marcha (4 m)")
	c.setFont("Helvetica", 11)
	y -= 0.6 * cm
	gait_unable = results.get('gait_unable', False)
	gait_time = results.get('gait_time_s', '')
	gait_time_str = "No pudo completar" if gait_unable else f"{gait_time} s"
	c.drawString(2 * cm, y, f"Tiempo: {gait_time_str}")
	y -= 0.5 * cm
	gait_score = int(results.get('gait_score', 0) or 0)
	c.drawString(2 * cm, y, f"Puntuación marcha: {gait_score} / 4")

	y -= 0.9 * cm
	c.setFont("Helvetica-Bold", 12)
	c.drawString(2 * cm, y, "Levantarse de la silla (5 repeticiones)")
	c.setFont("Helvetica", 11)
	y -= 0.6 * cm
	chair_unable = results.get('chair_unable', False)
	chair_time = results.get('chair_time_s', '')
	chair_time_str = "No pudo completar" if chair_unable else f"{chair_time} s"
	c.drawString(2 * cm, y, f"Tiempo: {chair_time_str}")
	y -= 0.5 * cm
	chair_score = int(results.get('chair_score', 0) or 0)
	c.drawString(2 * cm, y, f"Puntuación silla: {chair_score} / 4")

	y -= 1.0 * cm
	c.setFont("Helvetica-Bold", 13)
	c.drawString(2 * cm, y, f"Total SPPB: {results.get('total', '')} / 12")
	y -= 0.6 * cm
	c.setFont("Helvetica", 12)
	c.drawString(2 * cm, y, f"Conclusión: {results.get('interpretation', '')}")

	# Interpretación fisioterapéutica (misma página)
	y -= 0.9 * cm
	c.setFont("Helvetica-Bold", 12)
	c.drawString(2 * cm, y, "Interpretación detallada")
	c.setFont("Helvetica", 11)
	y -= 0.6 * cm
	exps = long_explanations(balance_score, gait_score, chair_score, int(results.get('total', 0) or 0))
	for title in ("Equilibrio", "Marcha", "Silla", "Total"):
		key = title.lower()
		text = exps.get(key, "")
		if not text:
			continue
		c.setFont("Helvetica-Bold", 11)
		c.drawString(2 * cm, y, title)
		c.setFont("Helvetica", 11)
		y -= 0.5 * cm
		y = _draw_wrapped_text(c, text, 2 * cm, y, width_chars=95, line_height=0.48 * cm)
		y -= 0.3 * cm

	# Pie de página

	c.setFont("Helvetica", 9)
	c.setFillColor(colors.grey)
	c.drawRightString(width - 2 * cm, 1.5 * cm, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

	c.showPage()
	c.save()
	return str(output_file.resolve())







