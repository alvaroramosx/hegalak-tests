from __future__ import annotations

from datetime import datetime, date
from pathlib import Path
from typing import Optional, Dict

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.app import App
from kivy.utils import get_color_from_hex as rgba
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Line

from ..models.sppb_logic import compute_scores
try:
	from kivy_garden.graph import Graph, MeshLinePlot
except Exception:
	Graph = None
	MeshLinePlot = None
from ..services.pdf_generator import generate_pdf
from ..services.explanations import short_summary
from ..services.excel_exporter import export_to_excel
from ..services.drive_uploader import upload_file_to_drive
from .. import config
from .state import SessionState


class ScoreSummaryLabel(Label):
	def update(self, state: SessionState):
		s = state.current_scores()
		self.text = f"Progreso · Equilibrio {s.balance_score}/4 · Marcha {s.gait_score}/4 · Silla {s.chair_score}/4 · Total {s.total}/12"


class BaseScreen(Screen):
	def __init__(self, root, **kwargs):
		super().__init__(**kwargs)
		self.root_widget = root

	@property
	def state(self) -> SessionState:
		return self.root_widget.state

	def style_input(self, ti: TextInput) -> TextInput:
		# Fuerza color de texto visible
		ti.foreground_color = (0, 0, 0, 1)
		try:
			# Ajustes coherentes con el tema (no crítico si falla)
			from kivy.utils import get_color_from_hex as _rgba
			ti.hint_text_color = _rgba('#9CA3AF')
			ti.cursor_color = _rgba('#7C2D12')
		except Exception:
			pass
		return ti

	def set_status(self, msg: str):
		self.root_widget.status_label.text = msg

	def update_progress(self):
		# Actualiza la barra de progreso visual del asistente
		try:
			self.root_widget.update_progress()
		except Exception:
			pass

	def wrapped_label(self, text: str, min_height: int = 40) -> Label:
		lbl = Label(text=text, size_hint_y=None, height=min_height, halign='left', valign='middle')
		# Ajustar el ancho del área de texto al ancho real del widget para que haga wrap
		lbl.bind(width=lambda s, w: setattr(s, 'text_size', (w, None)))
		# Ajustar la altura al tamaño de la textura, con un mínimo
		lbl.bind(texture_size=lambda s, ts: setattr(s, 'height', max(min_height, ts[1] + 4)))
		return lbl

	def centered_label(self, text: str, min_height: int = 40) -> Label:
		lbl = Label(text=text, size_hint_y=None, height=min_height, halign='center', valign='middle')
		lbl.bind(width=lambda s, w: setattr(s, 'text_size', (w, None)))
		lbl.bind(texture_size=lambda s, ts: setattr(s, 'height', max(min_height, ts[1] + 4)))
		return lbl

	def _bind_exclusive(self, *boxes):
		def on_active(box, value):
			if not value:
				return
			for b in boxes:
				if b is not box:
					b.active = False
		for b in boxes:
			b.bind(active=on_active)


class StartScreen(BaseScreen):
	def __init__(self, root, **kwargs):
		super().__init__(root, name="start", **kwargs)
		layout = BoxLayout(orientation="vertical", padding=20, spacing=16)

		card = Factory.Surface(orientation="vertical", padding=16, spacing=12, size_hint=(1, 1))

		form = GridLayout(cols=2, size_hint_y=None, padding=5, spacing=10)
		form.bind(minimum_height=form.setter("height"))

		self.name_input = self.style_input(TextInput(hint_text="Nombre paciente", multiline=False, size_hint_y=None, height=48))
		self.age_input = self.style_input(TextInput(hint_text="Edad", multiline=False, input_filter="int", size_hint_y=None, height=48))
		self.date_input = self.style_input(TextInput(text=date.today().strftime("%Y-%m-%d"), multiline=False, size_hint_y=None, height=48))

		form.add_widget(Label(text="Nombre", size_hint_y=None, height=48)); form.add_widget(self.name_input)
		form.add_widget(Label(text="Edad", size_hint_y=None, height=48)); form.add_widget(self.age_input)
		form.add_widget(Label(text="Fecha", size_hint_y=None, height=48)); form.add_widget(self.date_input)

		scroll = ScrollView(size_hint=(1, 1))
		scroll.add_widget(form)

		btns = BoxLayout(size_hint_y=None, height=56, spacing=10)
		start_btn = Factory.PrimaryButton(text="Empezar")
		start_btn.bind(on_release=lambda *_: self.on_start())
		btns.add_widget(start_btn)

		title = Factory.TitleLabel(text="SPPB · Datos iniciales", size_hint_y=None, height=40)
		card.add_widget(title)
		card.add_widget(scroll)
		card.add_widget(btns)

		layout.add_widget(card)
		self.add_widget(layout)

	def on_start(self):
		self.state.name = self.name_input.text.strip()
		self.state.age = self.age_input.text.strip()
		self.state.test_date = self.date_input.text.strip() or date.today().strftime("%Y-%m-%d")
		self.root_widget.drive_url = (config.DRIVE_FOLDER_URL or "").strip()
		self.root_widget.logo_path = (config.LOGO_PATH or None)
		if not self.state.name or not self.state.age:
			self.set_status("❗ Introduce nombre y edad del paciente.")
			return
		self.set_status("")
		self.root_widget.goto("balance_feet")

class DonutCanvas(AnchorLayout):
	value: float = NumericProperty(0.0)
	max_value: float = NumericProperty(4.0)
	color_rgba: list = ListProperty([0.49, 0.18, 0.07, 1])

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.bind(size=lambda *_: self._redraw())
		self.bind(pos=lambda *_: self._redraw())
		self.bind(value=lambda *_: self._redraw())
		self.bind(max_value=lambda *_: self._redraw())

	def _redraw(self):
		self.canvas.clear()
		w, h = self.size
		cx, cy = self.center
		base_r = min(w, h) / 2 - 8
		th = max(10, min(26, base_r * 0.22))
		r = max(0, base_r - th / 2 - 2)
		ang = 360.0 * (0 if self.max_value <= 0 else max(0.0, min(1.0, float(self.value) / float(self.max_value))))
		with self.canvas:
			Color(0.8, 0.78, 0.74, 1)
			Line(circle=(cx, cy, r), width=th)
			Color(*self.color_rgba)
			Line(circle=(cx, cy, r), width=th, angle_start=-90, angle_end=-90+ang)


class DonutGauge(BoxLayout):
	def __init__(self, title: str, max_value: float, color_rgba=None, auto_color: bool = False, **kwargs):
		super().__init__(orientation="vertical", **kwargs)
		default_color = rgba('#0EA5E9')
		self.auto_color = bool(auto_color)
		self.title_base = title
		self.chart_area = AnchorLayout(size_hint=(1, None), height=120)
		self.canvas_widget = DonutCanvas(size_hint=(1, 1), color_rgba=list(color_rgba or default_color), max_value=max_value)
		self.value_label = Label(text="0%", size_hint=(None, None), size=(0, 0))
		self.chart_area.add_widget(self.canvas_widget)
		self.chart_area.add_widget(self.value_label)
		self.add_widget(self.chart_area)
		# Caption inicial con 0/x
		self.caption = Label(text=f"{self.title_base} (0/{int(max_value)})", size_hint=(1, None), height=24)
		self.add_widget(self.caption)

	def set_value(self, v: float):
		val = float(v or 0)
		self.canvas_widget.value = val
		max_v = float(self.canvas_widget.max_value or 1)
		ratio = max(0.0, min(1.0, val / max_v))
		pct = int(round(ratio * 100))
		self.value_label.text = f"{pct}%"
		if self.auto_color:
			# Escala por tramos: rojo → naranja → amarillo → verde claro → verde
			if ratio < 0.20:
				col = rgba('#B91C1C')  # rojo
			elif ratio < 0.40:
				col = rgba('#F97316')  # naranja
			elif ratio < 0.60:
				col = rgba('#EAB308')  # amarillo
			elif ratio < 0.80:
				col = rgba('#86EFAC')  # verde claro
			else:
				col = rgba('#16A34A')  # verde
			self.canvas_widget.color_rgba = list(col)
		# Caption con valor actual v/x
		self.caption.text = f"{self.title_base} ({int(val)}/{int(max_v)})"

class BalanceFeetScreen(BaseScreen):
	def __init__(self, root, **kwargs):
		super().__init__(root, name="balance_feet", **kwargs)
		layout = BoxLayout(orientation="vertical", padding=20, spacing=16)

		card = Factory.Surface(orientation="vertical", padding=16, spacing=12)

		form = GridLayout(cols=2, size_hint_y=None, padding=5, spacing=10)
		form.bind(minimum_height=form.setter("height"))

		self.time_ft = self.style_input(TextInput(hint_text="Tiempo (s)", multiline=False, input_filter="float", size_hint_y=None, height=48))
		self.opt_yes = CheckBox(size_hint_y=None, height=40)
		self.opt_no = CheckBox(size_hint_y=None, height=40)
		self.opt_na = CheckBox(size_hint_y=None, height=40)
		form.add_widget(self.centered_label("Tiempo (s)", 48)); form.add_widget(self.time_ft)
		form.add_widget(Label(text="Pies juntos · Mantuvo 10 s (1 punto)", size_hint_y=None, height=40)); form.add_widget(self.opt_yes)
		form.add_widget(Label(text="No mantuvo 10 s (0 puntos)", size_hint_y=None, height=40)); form.add_widget(self.opt_no)
		form.add_widget(Label(text="No intentado (0 puntos)", size_hint_y=None, height=40)); form.add_widget(self.opt_na)

		self._bind_exclusive(self.opt_yes, self.opt_no, self.opt_na)
		self.time_ft.bind(text=lambda *_: self._on_time_change_feet())
		self.time_ft.bind(focus=lambda *_: self._on_time_change_feet())

		scroll = ScrollView(size_hint=(1, 1))
		scroll.add_widget(form)

		btns = BoxLayout(size_hint_y=None, height=56, spacing=10)
		back_btn = Factory.SecondaryButton(text="Anterior")
		back_btn.bind(on_release=lambda *_: self.root_widget.goto("start"))
		next_btn = Factory.PrimaryButton(text="Siguiente")
		next_btn.bind(on_release=lambda *_: self.on_next())
		btns.add_widget(back_btn)
		btns.add_widget(next_btn)

		title = Factory.TitleLabel(text="1A. Pies juntos", size_hint_y=None, height=40)
		card.add_widget(title)
		card.add_widget(scroll)
		card.add_widget(btns)

		layout.add_widget(card)
		self.add_widget(layout)

	def _bind_exclusive(self, *boxes):
		def on_active(box, value):
			if not value:
				return
			for b in boxes:
				if b is not box:
					b.active = False
		for b in boxes:
			b.bind(active=on_active)

	def on_pre_enter(self):
		self.update_progress()
		self._on_time_change_feet()

	def on_next(self):
		def sfloat(t):
			try:
				return float((t or "").replace(",", "."))
			except Exception:
				return None
		t = sfloat(self.time_ft.text)
		if t is not None:
			self.state.feet_together_s = max(0.0, min(t, 10.0))
		else:
			self.state.feet_together_s = 10.0 if self.opt_yes.active else 0.0
		self.update_progress()
		self.root_widget.goto("balance_semi")

	def _on_time_change_feet(self):
		def sfloat(t):
			try:
				return float((t or "").replace(",", "."))
			except Exception:
				return None
		t = sfloat(self.time_ft.text)
		if t is None:
			return
		self.opt_na.active = False
		if t >= 10.0:
			self.opt_yes.active = True
			self.opt_no.active = False
		else:
			self.opt_no.active = True
			self.opt_yes.active = False


class BalanceSemiScreen(BaseScreen):
	def __init__(self, root, **kwargs):
		super().__init__(root, name="balance_semi", **kwargs)
		layout = BoxLayout(orientation="vertical", padding=20, spacing=16)

		card = Factory.Surface(orientation="vertical", padding=16, spacing=12)

		form = GridLayout(cols=2, size_hint_y=None, padding=5, spacing=10)
		form.bind(minimum_height=form.setter("height"))

		self.time_semi = self.style_input(TextInput(hint_text="Tiempo (s)", multiline=False, input_filter="float", size_hint_y=None, height=48))
		self.opt_yes = CheckBox(size_hint_y=None, height=40)
		self.opt_no = CheckBox(size_hint_y=None, height=40)
		self.opt_na = CheckBox(size_hint_y=None, height=40)
		form.add_widget(self.centered_label("Tiempo (s)", 48)); form.add_widget(self.time_semi)
		form.add_widget(Label(text="Semitándem · Mantuvo 10 s (1 punto)", size_hint_y=None, height=40)); form.add_widget(self.opt_yes)
		form.add_widget(Label(text="No mantuvo 10 s (0 puntos)", size_hint_y=None, height=40)); form.add_widget(self.opt_no)
		form.add_widget(Label(text="No intentado (0 puntos)", size_hint_y=None, height=40)); form.add_widget(self.opt_na)

		self._bind_exclusive(self.opt_yes, self.opt_no, self.opt_na)
		self.time_semi.bind(text=lambda *_: self._on_time_change_semi())
		self.time_semi.bind(focus=lambda *_: self._on_time_change_semi())

		scroll = ScrollView(size_hint=(1, 1))
		scroll.add_widget(form)

		btns = BoxLayout(size_hint_y=None, height=56, spacing=10)
		back_btn = Factory.SecondaryButton(text="Anterior")
		back_btn.bind(on_release=lambda *_: self.root_widget.goto("balance_feet"))
		next_btn = Factory.PrimaryButton(text="Siguiente")
		next_btn.bind(on_release=lambda *_: self.on_next())
		btns.add_widget(back_btn)
		btns.add_widget(next_btn)

		title = Factory.TitleLabel(text="1B. Semitándem", size_hint_y=None, height=40)
		card.add_widget(title)
		card.add_widget(scroll)
		card.add_widget(btns)

		layout.add_widget(card)
		self.add_widget(layout)

	def _bind_exclusive(self, *boxes):
		def on_active(box, value):
			if not value:
				return
			for b in boxes:
				if b is not box:
					b.active = False
		for b in boxes:
			b.bind(active=on_active)

	def on_pre_enter(self):
		self.update_progress()
		self._on_time_change_semi()

	def on_next(self):
		def sfloat(t):
			try:
				return float((t or "").replace(",", "."))
			except Exception:
				return None
		t = sfloat(self.time_semi.text)
		if t is not None:
			self.state.semi_tandem_s = max(0.0, min(t, 10.0))
		else:
			self.state.semi_tandem_s = 10.0 if self.opt_yes.active else 0.0
		self.update_progress()
		self.root_widget.goto("balance_tandem")

	def _on_time_change_semi(self):
		def sfloat(t):
			try:
				return float((t or "").replace(",", "."))
			except Exception:
				return None
		t = sfloat(self.time_semi.text)
		if t is None:
			return
		self.opt_na.active = False
		if t >= 10.0:
			self.opt_yes.active = True
			self.opt_no.active = False
		else:
			self.opt_no.active = True
			self.opt_yes.active = False


class BalanceTandemScreen(BaseScreen):
	def __init__(self, root, **kwargs):
		super().__init__(root, name="balance_tandem", **kwargs)
		layout = BoxLayout(orientation="vertical", padding=20, spacing=16)

		card = Factory.Surface(orientation="vertical", padding=16, spacing=12)

		form = GridLayout(cols=2, size_hint_y=None, padding=5, spacing=10)
		form.bind(minimum_height=form.setter("height"))

		self.time_tandem = self.style_input(TextInput(hint_text="Tiempo (s)", multiline=False, input_filter="float", size_hint_y=None, height=48))
		self.opt_10 = CheckBox(size_hint_y=None, height=40)
		self.opt_3to9 = CheckBox(size_hint_y=None, height=40)
		self.opt_lt3 = CheckBox(size_hint_y=None, height=40)
		self.opt_na = CheckBox(size_hint_y=None, height=40)
		form.add_widget(self.centered_label("Tiempo (s)", 48)); form.add_widget(self.time_tandem)
		form.add_widget(Label(text="Tándem · Mantuvo 10 s (2 puntos)", size_hint_y=None, height=40)); form.add_widget(self.opt_10)
		form.add_widget(Label(text="Mantuvo 3–9.99 s (1 punto)", size_hint_y=None, height=40)); form.add_widget(self.opt_3to9)
		form.add_widget(Label(text="< 3 s (0 puntos)", size_hint_y=None, height=40)); form.add_widget(self.opt_lt3)
		form.add_widget(Label(text="No intentado (0 puntos)", size_hint_y=None, height=40)); form.add_widget(self.opt_na)

		self._bind_exclusive(self.opt_10, self.opt_3to9, self.opt_lt3, self.opt_na)
		self.time_tandem.bind(text=lambda *_: self._on_time_change_tandem())

		scroll = ScrollView(size_hint=(1, 1))
		scroll.add_widget(form)

		btns = BoxLayout(size_hint_y=None, height=56, spacing=10)
		back_btn = Factory.SecondaryButton(text="Anterior")
		back_btn.bind(on_release=lambda *_: self.root_widget.goto("balance_semi"))
		next_btn = Factory.PrimaryButton(text="Siguiente")
		next_btn.bind(on_release=lambda *_: self.on_next())
		btns.add_widget(back_btn)
		btns.add_widget(next_btn)

		title = Factory.TitleLabel(text="1C. Tándem", size_hint_y=None, height=40)
		card.add_widget(title)
		card.add_widget(scroll)
		card.add_widget(btns)

		layout.add_widget(card)
		self.add_widget(layout)

	def _bind_exclusive(self, *boxes):
		def on_active(box, value):
			if not value:
				return
			for b in boxes:
				if b is not box:
					b.active = False
		for b in boxes:
			b.bind(active=on_active)

	def on_pre_enter(self):
		self.update_progress()

	def on_next(self):
		def sfloat(t):
			try:
				return float((t or "").replace(",", "."))
			except Exception:
				return None
		t = sfloat(self.time_tandem.text)
		if t is not None:
			# Guardamos una codificación simple: 10, 5, 2, 0 según el rango
			if t >= 10.0:
				self.state.tandem_s = 10.0
			elif t >= 3.0:
				self.state.tandem_s = 5.0
			elif t > 0.0:
				self.state.tandem_s = 2.0
			else:
				self.state.tandem_s = 0.0
		else:
			if self.opt_10.active:
				self.state.tandem_s = 10.0
			elif self.opt_3to9.active:
				self.state.tandem_s = 5.0
			elif self.opt_lt3.active:
				self.state.tandem_s = 2.0
			else:
				self.state.tandem_s = 0.0
		self.update_progress()
		self.root_widget.goto("gait")

	def _on_time_change_tandem(self):
		def sfloat(t):
			try:
				return float((t or "").replace(",", "."))
			except Exception:
				return None
		t = sfloat(self.time_tandem.text)
		if t is None:
			return
		self.opt_na.active = False
		if t >= 10.0:
			self.opt_10.active = True; self.opt_3to9.active = self.opt_lt3.active = False
		elif t >= 3.0:
			self.opt_3to9.active = True; self.opt_10.active = self.opt_lt3.active = False
		elif t > 0.0:
			self.opt_lt3.active = True; self.opt_10.active = self.opt_3to9.active = False


class GaitScreen(BaseScreen):
	def __init__(self, root, **kwargs):
		super().__init__(root, name="gait", **kwargs)
		layout = BoxLayout(orientation="vertical", padding=20, spacing=16)

		card = Factory.Surface(orientation="vertical", padding=16, spacing=12)

		form = GridLayout(cols=4, size_hint_y=None, padding=5, spacing=10)
		form.bind(minimum_height=form.setter("height"))

		self.g1 = self.style_input(TextInput(hint_text="Tiempo 1 (s)", multiline=False, input_filter="float", size_hint_y=None, height=48))
		self.g1_un = CheckBox(size_hint_y=None, height=48)
		self.g2 = self.style_input(TextInput(hint_text="Tiempo 2 (s)", multiline=False, input_filter="float", size_hint_y=None, height=48))
		self.g2_un = CheckBox(size_hint_y=None, height=48)

		form.add_widget(self.centered_label("Primera medición", 48)); form.add_widget(self.g1); form.add_widget(self.centered_label("No pudo", 48)); form.add_widget(self.g1_un)
		form.add_widget(self.centered_label("Segunda medición", 48)); form.add_widget(self.g2); form.add_widget(self.centered_label("No pudo", 48)); form.add_widget(self.g2_un)

		# Contenedor desplazable que incluye formulario y categorías
		container = GridLayout(cols=1, size_hint_y=None, padding=0, spacing=10)
		container.bind(minimum_height=container.setter('height'))
		container.add_widget(form)

		# Categorías de puntuación (solo informativas, se marcan automáticamente)
		self.cat_gt_870 = CheckBox(size_hint_y=None, height=40)
		self.cat_621_870 = CheckBox(size_hint_y=None, height=40)
		self.cat_482_620 = CheckBox(size_hint_y=None, height=40)
		self.cat_lt_482 = CheckBox(size_hint_y=None, height=40)

		self.cats_grid = GridLayout(cols=4, size_hint_y=None, padding=5, spacing=10)
		self.cats_grid.bind(minimum_height=self.cats_grid.setter('height'))
		self.cats_grid.add_widget(self.centered_label("Si el tiempo es > 8.70 s: 1 punto")); self.cats_grid.add_widget(self.cat_gt_870)
		self.cats_grid.add_widget(self.centered_label("Si el tiempo es 6.21–8.70 s: 2 puntos")); self.cats_grid.add_widget(self.cat_621_870)
		self.cats_grid.add_widget(self.centered_label("Si el tiempo es 4.82–6.20 s: 3 puntos")); self.cats_grid.add_widget(self.cat_482_620)
		self.cats_grid.add_widget(self.centered_label("Si el tiempo es < 4.82 s: 4 puntos")); self.cats_grid.add_widget(self.cat_lt_482)

		container.add_widget(self.cats_grid)

		scroll = ScrollView(size_hint=(1, 1))
		scroll.add_widget(container)

		btns = BoxLayout(size_hint_y=None, height=56, spacing=10)
		back_btn = Factory.SecondaryButton(text="Anterior")
		back_btn.bind(on_release=lambda *_: self.root_widget.goto("balance_tandem"))
		next_btn = Factory.PrimaryButton(text="Siguiente")
		next_btn.bind(on_release=lambda *_: self.on_next())
		btns.add_widget(back_btn)
		btns.add_widget(next_btn)

		title = Factory.TitleLabel(text="2. Velocidad de marcha (4 m)", size_hint_y=None, height=40)
		card.add_widget(title)
		card.add_widget(scroll)
		card.add_widget(btns)

		layout.add_widget(card)
		self.add_widget(layout)

		# Exclusividad y actualización de categorías
		self._bind_exclusive(self.cat_gt_870, self.cat_621_870, self.cat_482_620, self.cat_lt_482)
		# Actualiza categorías y diseño cuando cambia cualquier entrada o el tamaño
		self.g1.bind(text=lambda *_: self.update_gait_categories())
		self.g2.bind(text=lambda *_: self.update_gait_categories())
		self.g1.bind(focus=lambda *_: self.update_gait_categories())
		self.g2.bind(focus=lambda *_: self.update_gait_categories())
		self.g1_un.bind(active=lambda *_: self.update_gait_categories())
		self.g2_un.bind(active=lambda *_: self.update_gait_categories())
		Window.bind(size=lambda *_: self.update_gait_layout())

	def on_pre_enter(self):
		self.update_progress()
		self.update_gait_categories()
		self.update_gait_layout()

	def update_gait_categories(self):
		def sfloat(t):
			try:
				return float((t or "").replace(",", "."))
			except Exception:
				return None
		t1 = sfloat(self.g1.text)
		t2 = sfloat(self.g2.text)
		unable = bool(self.g1_un.active) and bool(self.g2_un.active)
		valid = [t for t in [t1, t2] if t is not None]
		best = min(valid) if valid else None
		# Limpia selección
		for cb in (self.cat_gt_870, self.cat_621_870, self.cat_482_620, self.cat_lt_482):
			cb.active = False
		if unable or best is None:
			return
		if best > 8.70:
			self.cat_gt_870.active = True
		elif 6.21 <= best <= 8.70:
			self.cat_621_870.active = True
		elif 4.82 <= best <= 6.20:
			self.cat_482_620.active = True
		elif best < 4.82:
			self.cat_lt_482.active = True

	def update_gait_layout(self):
		# En pantallas estrechas, mostrar una categoría por fila (2 columnas: texto + checkbox)
		# En pantallas anchas, usar 2x2 (4 columnas)
		threshold = 700
		self.cats_grid.cols = 2 if Window.width < threshold else 4

	def on_next(self):
		def sfloat(t):
			try:
				return float((t or "").replace(",", "."))
			except Exception:
				return None
		self.state.gait_time1_s = sfloat(self.g1.text)
		self.state.gait_unable1 = bool(self.g1_un.active)
		self.state.gait_time2_s = sfloat(self.g2.text)
		self.state.gait_unable2 = bool(self.g2_un.active)
		self.update_progress()
		self.root_widget.goto("chair")


class ChairScreen(BaseScreen):
	def __init__(self, root, **kwargs):
		super().__init__(root, name="chair", **kwargs)
		layout = BoxLayout(orientation="vertical", padding=20, spacing=16)

		card = Factory.Surface(orientation="vertical", padding=16, spacing=12)

		form = GridLayout(cols=2, size_hint_y=None, padding=5, spacing=10)
		form.bind(minimum_height=form.setter("height"))

		self.pre_unable = CheckBox(size_hint_y=None, height=48)
		self.time = self.style_input(TextInput(hint_text="Tiempo 5 repeticiones (s)", multiline=False, input_filter="float", size_hint_y=None, height=48))
		self.unable = CheckBox(size_hint_y=None, height=48)

		form.add_widget(self.wrapped_label("¿Puede levantarse sin apoyarse?", 48)); form.add_widget(self.pre_unable)
		form.add_widget(self.wrapped_label("Tiempo 5 repeticiones (s)", 48)); form.add_widget(self.time)
		form.add_widget(self.wrapped_label("No pudo completar", 48)); form.add_widget(self.unable)

		# Categorías de puntuación (informativas, se marcan automáticamente)
		self.cat_unable_or_gt60 = CheckBox(size_hint_y=None, height=40)
		self.cat_ge_1670 = CheckBox(size_hint_y=None, height=40)
		self.cat_1370_1669 = CheckBox(size_hint_y=None, height=40)
		self.cat_1120_1369 = CheckBox(size_hint_y=None, height=40)
		self.cat_le_1119 = CheckBox(size_hint_y=None, height=40)

		self.cats_grid_chair = GridLayout(cols=2, size_hint_y=None, padding=5, spacing=10)
		self.cats_grid_chair.bind(minimum_height=self.cats_grid_chair.setter('height'))
		self.cats_grid_chair.add_widget(self.centered_label("No puede completar 5 levantamientos o tarda > 60 s: 0 puntos")); self.cats_grid_chair.add_widget(self.cat_unable_or_gt60)
		self.cats_grid_chair.add_widget(self.centered_label("Si el tiempo es ≥ 16.70 s: 1 punto")); self.cats_grid_chair.add_widget(self.cat_ge_1670)
		self.cats_grid_chair.add_widget(self.centered_label("Si el tiempo es 13.70–16.69 s: 2 puntos")); self.cats_grid_chair.add_widget(self.cat_1370_1669)
		self.cats_grid_chair.add_widget(self.centered_label("Si el tiempo es 11.20–13.69 s: 3 puntos")); self.cats_grid_chair.add_widget(self.cat_1120_1369)
		self.cats_grid_chair.add_widget(self.centered_label("Si el tiempo es ≤ 11.19 s: 4 puntos")); self.cats_grid_chair.add_widget(self.cat_le_1119)

		container = GridLayout(cols=1, size_hint_y=None, padding=0, spacing=10)
		container.bind(minimum_height=container.setter('height'))
		container.add_widget(form)
		container.add_widget(self.cats_grid_chair)
		scroll = ScrollView(size_hint=(1, 1))
		scroll.add_widget(container)

		btns = BoxLayout(size_hint_y=None, height=56, spacing=10)
		back_btn = Factory.SecondaryButton(text="Anterior")
		back_btn.bind(on_release=lambda *_: self.root_widget.goto("gait"))
		next_btn = Factory.PrimaryButton(text="Finalizar")
		next_btn.bind(on_release=lambda *_: self.on_next())
		btns.add_widget(back_btn)
		btns.add_widget(next_btn)

		title = Factory.TitleLabel(text="3. Levantarse de la silla", size_hint_y=None, height=40)
		card.add_widget(title)
		card.add_widget(scroll)
		card.add_widget(btns)

		layout.add_widget(card)
		self.add_widget(layout)

		# Exclusividad entre pre_unable y unable (no pueden estar activos a la vez)
		self._bind_exclusive_chair(self.pre_unable, self.unable)
		# Exclusividad entre categorías
		self._bind_exclusive(
			self.cat_unable_or_gt60,
			self.cat_ge_1670,
			self.cat_1370_1669,
			self.cat_1120_1369,
			self.cat_le_1119,
		)

		# Actualiza categorías cuando cambia cualquier entrada
		self.pre_unable.bind(active=lambda *_: self.update_chair_categories())
		self.unable.bind(active=lambda *_: self.update_chair_categories())
		self.time.bind(text=lambda *_: self.update_chair_categories())
		self.time.bind(focus=lambda *_: self.update_chair_categories())
		Window.bind(size=lambda *_: self.update_chair_layout())

	def on_pre_enter(self):
		self.update_progress()
		self.update_chair_categories()
		self.update_chair_layout()

	def on_next(self):
		def sfloat(t):
			try:
				return float((t or "").replace(",", "."))
			except Exception:
				return None
		self.state.chair_pretest_unable = not (not self.pre_unable.active)
		self.state.chair_time_s = sfloat(self.time.text)
		self.state.chair_unable = bool(self.unable.active)
		self.update_progress()
		self.root_widget.goto("summary")

	def update_chair_categories(self):
		def sfloat(t):
			try:
				return float((t or "").replace(",", "."))
			except Exception:
				return None
		t = sfloat(self.time.text)
		unable = bool(self.pre_unable.active) or bool(self.unable.active)
		# Limpia selección
		for cb in (
			self.cat_unable_or_gt60,
			self.cat_ge_1670,
			self.cat_1370_1669,
			self.cat_1120_1369,
			self.cat_le_1119,
		):
			cb.active = False
		if unable or t is None or t > 60.0:
			self.cat_unable_or_gt60.active = True
			return
		if t >= 16.70:
			self.cat_ge_1670.active = True
		elif 13.70 <= t <= 16.69:
			self.cat_1370_1669.active = True
		elif 11.20 <= t <= 13.69:
			self.cat_1120_1369.active = True
		elif t <= 11.19:
			self.cat_le_1119.active = True

	def _bind_exclusive_chair(self, box_a: CheckBox, box_b: CheckBox):
		def on_active(box, value):
			if not value:
				return
			other = box_b if box is box_a else box_a
			other.active = False
			self.update_chair_categories()
		box_a.bind(active=on_active)
		box_b.bind(active=on_active)

	def update_chair_layout(self):
		# Ajusta columnas de categorías según ancho
		threshold = 700
		self.cats_grid_chair.cols = 2  # texto + checkbox por fila siempre


class SummaryScreen(BaseScreen):
	def __init__(self, root, **kwargs):
		super().__init__(root, name="summary", **kwargs)
		layout = BoxLayout(orientation="vertical", padding=20, spacing=16)

		card = Factory.Surface(orientation="vertical", padding=16, spacing=12)
		# Zona de gráficos: usa Kivy Garden Graph si está disponible; si no, se usa fallback con barras
		self.graph_container = BoxLayout(orientation="vertical", size_hint=(1, None), height=260, spacing=8)
		self.using_garden_graph = False
		# Donuts individuales
		row1 = BoxLayout(size_hint=(1, None), height=170, spacing=24, padding=(0, 10))
		self.donut_balance = DonutGauge("Equilibrio: ", max_value=4, auto_color=True)
		self.donut_gait = DonutGauge("Marcha: ", max_value=4, auto_color=True)
		self.donut_chair = DonutGauge("Silla: ", max_value=4, auto_color=True)
		row1.add_widget(self.donut_balance)
		row1.add_widget(self.donut_gait)
		row1.add_widget(self.donut_chair)
		self.graph_container.add_widget(row1)
		row2 = BoxLayout(size_hint=(1, None), height=170, spacing=24, padding=(0, 0))
		self.donut_total = DonutGauge("Total: ", max_value=12, auto_color=True)
		row2.add_widget(self.donut_total)
		self.graph_container.add_widget(row2)

		self.summary_label = Label(text="", size_hint_y=None, height=140)
		title = Factory.TitleLabel(text="Resumen final", size_hint_y=None, height=40)
		card.add_widget(title)
		# Separación bajo el título para que los dónuts no lo invadan
		try:
			from kivy.uix.widget import Widget as _Widget
			card.add_widget(_Widget(size_hint_y=None, height=50))
		except Exception:
			pass
		card.add_widget(self.graph_container)
		# Mover resumen arriba del todo
		card.add_widget(self.summary_label)


		# Ancla el contenido arriba y deja que el card crezca según sus hijos
		wrapper = AnchorLayout(anchor_y='top', anchor_x='center')
		card.size_hint = (1, None)
		try:
			card.bind(minimum_height=card.setter('height'))
		except Exception:
			pass
		wrapper.add_widget(card)
		layout.add_widget(wrapper)
		self.add_widget(layout)

	def on_pre_enter(self):
		s = self.state.current_scores()
		# Actualiza gráficos
		# Asegura consistencia: valores no negativos y dentro del máximo; fuerza actualización visual
		b = max(0, min(4, int(s.balance_score)))
		g = max(0, min(4, int(s.gait_score)))
		c = max(0, min(4, int(s.chair_score)))
		t = max(0, min(12, int(s.total)))
		self.donut_balance.set_value(b)
		self.donut_gait.set_value(g)
		self.donut_chair.set_value(c)
		self.donut_total.set_value(t)
		self.summary_label.text = short_summary(s.balance_score, s.gait_score, s.chair_score, s.total)
		self.update_progress()

	def on_send(self):
		patient = {"name": self.state.name, "age": self.state.age, "date": self.state.test_date}
		scores = self.state.current_scores()
		inputs = self.state.to_inputs()
		results = {
			"feet_together_s": inputs.feet_together_s,
			"semi_tandem_s": inputs.semi_tandem_s,
			"tandem_s": inputs.tandem_s,
			"gait_time_s": inputs.gait_time_s,
			"gait_unable": inputs.gait_unable,
			"chair_time_s": inputs.chair_time_s,
			"chair_unable": inputs.chair_unable,
			"balance_score": scores.balance_score,
			"gait_score": scores.gait_score,
			"chair_score": scores.chair_score,
			"total": scores.total,
			"interpretation": scores.interpretation,
		}

		stamp = datetime.now().strftime("%Y%m%d_%H%M")
		base_name = f"SPPB_{self.state.name}_{stamp}"
		out_dir = config.OUTPUT_DIR
		out_dir.mkdir(parents=True, exist_ok=True)
		pdf_path = str(out_dir / f"{base_name}.pdf")
		xlsx_path = str(out_dir / f"{base_name}.xlsx")

		try:
			generate_pdf(pdf_path, patient, results, logo_path=self.root_widget.logo_path, center_name=config.CENTER_NAME)
			export_to_excel(xlsx_path, patient, results)
		except Exception as e:
			print(f"[Generate Files] Error: {e}")
			import traceback as _tb
			_tb.print_exc()
			self.set_status("❗ Error")
			return

		if not self.root_widget.drive_url:
			self.set_status(f"⚠️ Guardado local en {out_dir.resolve()}")
			return
		try:
			upload_file_to_drive(pdf_path, self.root_widget.drive_url, credentials_json_path=config.CREDENTIALS_JSON_PATH, use_service_account=config.USE_SERVICE_ACCOUNT)
			upload_file_to_drive(xlsx_path, self.root_widget.drive_url, credentials_json_path=config.CREDENTIALS_JSON_PATH, use_service_account=config.USE_SERVICE_ACCOUNT)
			self.set_status("✅ Informe subido correctamente a Drive")
		except Exception as e:
			print(f"[Drive Upload] Error: {e}")
			import traceback as _tb
			_tb.print_exc()
			self.set_status("❗ Error")


class WizardRoot(BoxLayout):
	status_label: Label
	progress_bar: ProgressBar
	drive_url: str = ""
	logo_path: Optional[str] = None

	def __init__(self, **kwargs):
		super().__init__(orientation="vertical", **kwargs)
		self.state = SessionState()

		# Barra de progreso (visible fuera de la pantalla inicial)
		self.progress_bar = ProgressBar(max=5, value=0, size_hint=(1, None), height=16)

		actions = BoxLayout(size_hint=(1, None), height=64, spacing=10, padding=(20, 10))
		self.cancel_btn = Factory.SecondaryButton(text="Salir")
		self.cancel_btn.bind(on_release=lambda *_: self.on_cancel())
		actions.add_widget(self.cancel_btn)

		self.sm = ScreenManager(transition=NoTransition())
		self.sm.add_widget(StartScreen(self))
		self.sm.add_widget(BalanceFeetScreen(self))
		self.sm.add_widget(BalanceSemiScreen(self))
		self.sm.add_widget(BalanceTandemScreen(self))
		self.sm.add_widget(GaitScreen(self))
		self.sm.add_widget(ChairScreen(self))
		self.sm.add_widget(SummaryScreen(self))

		self.status_label = Label(text="", size_hint=(1, None), height=30)
		# Botón de enviar a Drive fijo arriba de la barra de acciones en la pantalla summary
		self.send_btn_global = Factory.PrimaryButton(text="Enviar a Drive", size_hint=(1, None), height=56)
		self.send_btn_global.bind(on_release=lambda *_: self._on_send_from_global())

		self.add_widget(self.progress_bar)
		self.add_widget(self.sm)
		# Este botón se mostrará solo en la pantalla summary
		self.add_widget(self.send_btn_global)
		self.add_widget(actions)
		self.add_widget(self.status_label)

		self.goto("start")

	def goto(self, name: str):
		self.sm.current = name
		self.cancel_btn.text = "Salir" if name == "start" else "Cancelar"
		self.update_progress()
		# Oculta la barra en la pantalla inicial
		self.progress_bar.opacity = 0 if name == "start" else 1
		# Botón Enviar a Drive visible solo en summary
		self.send_btn_global.opacity = 1 if name == "summary" else 0
		self.send_btn_global.disabled = False if name == "summary" else True

	def on_cancel(self):
		if self.sm.current == "start":
			App.get_running_app().stop()
			return
		self.state.reset()
		self.status_label.text = "Operación cancelada"
		self.goto("start")

	def _on_send_from_global(self):
		# Reenvía al manejador de SummaryScreen si estamos allí
		if self.sm.current == "summary":
			try:
				self.sm.get_screen("summary").on_send()
			except Exception:
				pass

	def update_progress(self):
		# Cálculo por fases: 5 pasos (A, B, C de equilibrio, marcha, silla)
		name = self.sm.current if self.sm else "start"
		order = ["balance_feet", "balance_semi", "balance_tandem", "gait", "chair"]
		if name not in order:
			# start -> 0, summary -> completo
			value = 0 if name == "start" else 5
		else:
			idx = order.index(name)
			value = idx  # progresión antes de completar la fase actual
		self.progress_bar.value = value
