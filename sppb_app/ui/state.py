from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from ..models.sppb_logic import SppbInputs, compute_scores


@dataclass
class SessionState:
	# Paciente
	name: str = ""
	age: str = ""
	test_date: str = date.today().strftime("%Y-%m-%d")

	# Balance (en segundos 0-10 para A/B/C)
	feet_together_s: float = 0.0
	semi_tandem_s: float = 0.0
	tandem_s: float = 0.0

	# Marcha (dos mediciones de 4 m)
	gait_time1_s: Optional[float] = None
	gait_time2_s: Optional[float] = None
	gait_unable1: bool = False
	gait_unable2: bool = False

	# Silla
	chair_pretest_unable: bool = False  # no puede levantarse sin apoyarse -> test silla no se realiza
	chair_time_s: Optional[float] = None
	chair_unable: bool = False

	def to_inputs(self) -> SppbInputs:
		# Para marcha usamos el mejor tiempo válido
		valid_times = [t for t in [self.gait_time1_s, self.gait_time2_s] if t is not None]
		gait_unable = (self.gait_unable1 and self.gait_unable2) or (len(valid_times) == 0)
		best_time = min(valid_times) if valid_times else None

		# Para silla, si pretest indica que no puede, marcamos como unable
		chair_unable = self.chair_unable or self.chair_pretest_unable or (self.chair_time_s is None)

		return SppbInputs(
			feet_together_s=float(self.feet_together_s or 0.0),
			semi_tandem_s=float(self.semi_tandem_s or 0.0),
			tandem_s=float(self.tandem_s or 0.0),
			gait_time_s=best_time,
			gait_unable=gait_unable,
			chair_time_s=None if chair_unable else self.chair_time_s,
			chair_unable=chair_unable,
		)

	def current_scores(self):
		return compute_scores(self.to_inputs())

	def reset(self):
		self.name = ""
		self.age = ""
		self.test_date = date.today().strftime("%Y-%m-%d")
		self.feet_together_s = 0.0
		self.semi_tandem_s = 0.0
		self.tandem_s = 0.0
		self.gait_time1_s = None
		self.gait_time2_s = None
		self.gait_unable1 = False
		self.gait_unable2 = False
		self.chair_pretest_unable = False
		self.chair_time_s = None
		self.chair_unable = False





