from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class PatientInfo:
	name: str
	age: int
	test_date: date


@dataclass
class SppbInputs:
	# Balance seconds held for each stance (0-10s)
	feet_together_s: float
	semi_tandem_s: float
	tandem_s: float

	# Gait speed: time to walk 4 meters (seconds)
	gait_time_s: Optional[float]
	gait_unable: bool = False

	# Chair rise: time to rise 5 times (seconds)
	chair_time_s: Optional[float] = None
	chair_unable: bool = False


@dataclass
class SppbScores:
	balance_score: int
	gait_score: int
	chair_score: int

	@property
	def total(self) -> int:
		return self.balance_score + self.gait_score + self.chair_score

	@property
	def interpretation(self) -> str:
		return interpret_total(self.total)


def clamp_seconds(value: Optional[float], minimum: float = 0.0, maximum: float = 9999.0) -> Optional[float]:
	if value is None:
		return None
	try:
		v = float(value)
	except (TypeError, ValueError):
		return None
	if v < minimum:
		return minimum
	if v > maximum:
		return maximum
	return v


def score_balance(feet_together_s: float, semi_tandem_s: float, tandem_s: float) -> int:
	"""Score balance according to standard SPPB rules (0-4)."""
	f = clamp_seconds(feet_together_s, 0, 10) or 0
	s = clamp_seconds(semi_tandem_s, 0, 10) or 0
	t = clamp_seconds(tandem_s, 0, 10) or 0

	if f < 10:
		return 0
	if s < 10:
		return 1
	if t < 3:
		return 2
	if t < 10:
		return 3
	return 4


def score_gait(time_seconds: Optional[float], unable: bool = False) -> int:
	"""Score gait speed over 4m (0-4) using common SPPB thresholds."""
	if unable:
		return 0
	t = clamp_seconds(time_seconds)
	if t is None or t <= 0:
		return 0
	if t > 8.70:
		return 1
	if t >= 6.21:
		return 2
	if t >= 4.83:
		return 3
	return 4


def score_chair(time_seconds: Optional[float], unable: bool = False) -> int:
	"""Score 5-chair-stands time (0-4) using SPPB thresholds."""
	if unable:
		return 0
	t = clamp_seconds(time_seconds)
	if t is None or t <= 0:
		return 0
	if t >= 16.70:
		return 1
	if t >= 13.70:
		return 2
	if t >= 11.20:
		return 3
	return 4


def interpret_total(total_score: int) -> str:
	# 0–4 alta, 5–8 moderada, 9–12 baja
	if total_score <= 4:
		return "Fragilidad alta"
	if total_score <= 8:
		return "Fragilidad moderada"
	return "Fragilidad baja"


def compute_scores(inputs: SppbInputs) -> SppbScores:
	balance = score_balance(inputs.feet_together_s, inputs.semi_tandem_s, inputs.tandem_s)
	gait = score_gait(inputs.gait_time_s, inputs.gait_unable)
	chair = score_chair(inputs.chair_time_s, inputs.chair_unable)
	return SppbScores(balance_score=balance, gait_score=gait, chair_score=chair)







