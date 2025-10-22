from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


def _draw_header(c: canvas.Canvas, logo_path: Optional[str], center_name: str) -> None:
	width, height = A4
	if logo_path and Path(logo_path).exists():
		c.drawImage(logo_path, 2 * cm, height - 3.5 * cm, width=3 * cm, height=3 * cm, preserveAspectRatio=True, mask='auto')
	else:
		c.setStrokeColor(colors.black)
		c.rect(2 * cm, height - 3.5 * cm, 3 * cm, 3 * cm)
		c.drawString(2.2 * cm, height - 2.2 * cm, "LOGO")

	c.setFont("Helvetica-Bold", 16)
	c.drawString(6 * cm, height - 2.0 * cm, center_name)
	c.setFont("Helvetica", 12)
	c.drawString(6 * cm, height - 2.7 * cm, "Informe de SPPB (Short Physical Performance Battery)")


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
	c.drawString(2 * cm, y, f"Puntuación equilibrio: {results.get('balance_score', '')} / 4")

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
	c.drawString(2 * cm, y, f"Puntuación marcha: {results.get('gait_score', '')} / 4")

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
	c.drawString(2 * cm, y, f"Puntuación silla: {results.get('chair_score', '')} / 4")

	y -= 1.0 * cm
	c.setFont("Helvetica-Bold", 13)
	c.drawString(2 * cm, y, f"Total SPPB: {results.get('total', '')} / 12")
	y -= 0.6 * cm
	c.setFont("Helvetica", 12)
	c.drawString(2 * cm, y, f"Conclusión: {results.get('interpretation', '')}")

	c.setFont("Helvetica", 9)
	c.setFillColor(colors.grey)
	c.drawRightString(width - 2 * cm, 1.5 * cm, f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

	c.showPage()
	c.save()
	return str(output_file.resolve())






