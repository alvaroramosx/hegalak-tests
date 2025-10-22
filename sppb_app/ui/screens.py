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
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.app import App
from kivy.utils import get_color_from_hex as rgba
from kivy.factory import Factory

from ..models.sppb_logic import compute_scores
from ..services.pdf_generator import generate_pdf
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
		self.root_widget.progress.update(self.state)


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
		self.logo_input = self.style_input(TextInput(text=(config.LOGO_PATH or ""), multiline=False, size_hint_y=None, height=48))

		form.add_widget(Label(text="Nombre", size_hint_y=None, height=48)); form.add_widget(self.name_input)
		form.add_widget(Label(text="Edad", size_hint_y=None, height=48)); form.add_widget(self.age_input)
		form.add_widget(Label(text="Fecha", size_hint_y=None, height=48)); form.add_widget(self.date_input)
		form.add_widget(Label(text="Logo (opcional)", size_hint_y=None, height=48)); form.add_widget(self.logo_input)

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
		self.root_widget.logo_path = (self.logo_input.text or None)
		if not self.state.name or not self.state.age:
			self.set_status("❗ Introduce nombre y edad del paciente.")
			return
		self.set_status("")
		self.root_widget.goto("balance_feet")


class BalanceFeetScreen(BaseScreen):
	def __init__(self, root, **kwargs):
		super().__init__(root, name="balance_feet", **kwargs)
		layout = BoxLayout(orientation="vertical", padding=20, spacing=16)

		card = Factory.Surface(orientation="vertical", padding=16, spacing=12)

		form = GridLayout(cols=2, size_hint_y=None, padding=5, spacing=10)
		form.bind(minimum_height=form.setter("height"))

		self.opt_yes = CheckBox(size_hint_y=None, height=40)
		self.opt_no = CheckBox(size_hint_y=None, height=40)
		self.opt_na = CheckBox(size_hint_y=None, height=40)
		form.add_widget(Label(text="A) Pies juntos · Mantuvo 10 s (1 punto)", size_hint_y=None, height=40)); form.add_widget(self.opt_yes)
		form.add_widget(Label(text="A) No mantuvo 10 s (0 puntos)", size_hint_y=None, height=40)); form.add_widget(self.opt_no)
		form.add_widget(Label(text="A) No intentado (0 puntos)", size_hint_y=None, height=40)); form.add_widget(self.opt_na)

		self._bind_exclusive(self.opt_yes, self.opt_no, self.opt_na)

		scroll = ScrollView(size_hint=(1, 1))
		scroll.add_widget(form)

		btns = BoxLayout(size_hint_y=None, height=56, spacing=10)
		back_btn = Factory.SecondaryButton(text="← Anterior")
		back_btn.bind(on_release=lambda *_: self.root_widget.goto("start"))
		next_btn = Factory.PrimaryButton(text="Siguiente →")
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

	def on_next(self):
		self.state.feet_together_s = 10.0 if self.opt_yes.active else 0.0
		self.update_progress()
		self.root_widget.goto("balance_semi")


class BalanceSemiScreen(BaseScreen):
	def __init__(self, root, **kwargs):
		super().__init__(root, name="balance_semi", **kwargs)
		layout = BoxLayout(orientation="vertical", padding=20, spacing=16)

		card = Factory.Surface(orientation="vertical", padding=16, spacing=12)

		form = GridLayout(cols=2, size_hint_y=None, padding=5, spacing=10)
		form.bind(minimum_height=form.setter("height"))

		self.opt_yes = CheckBox(size_hint_y=None, height=40)
		self.opt_no = CheckBox(size_hint_y=None, height=40)
		self.opt_na = CheckBox(size_hint_y=None, height=40)
		form.add_widget(Label(text="B) Semitándem · Mantuvo 10 s", size_hint_y=None, height=40)); form.add_widget(self.opt_yes)
		form.add_widget(Label(text="B) No mantuvo 10 s", size_hint_y=None, height=40)); form.add_widget(self.opt_no)
		form.add_widget(Label(text="B) No intentado", size_hint_y=None, height=40)); form.add_widget(self.opt_na)

		self._bind_exclusive(self.opt_yes, self.opt_no, self.opt_na)

		scroll = ScrollView(size_hint=(1, 1))
		scroll.add_widget(form)

		btns = BoxLayout(size_hint_y=None, height=56, spacing=10)
		back_btn = Factory.SecondaryButton(text="← Anterior")
		back_btn.bind(on_release=lambda *_: self.root_widget.goto("balance_feet"))
		next_btn = Factory.PrimaryButton(text="Siguiente →")
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

	def on_next(self):
		self.state.semi_tandem_s = 10.0 if self.opt_yes.active else 0.0
		self.update_progress()
		self.root_widget.goto("balance_tandem")


class BalanceTandemScreen(BaseScreen):
	def __init__(self, root, **kwargs):
		super().__init__(root, name="balance_tandem", **kwargs)
		layout = BoxLayout(orientation="vertical", padding=20, spacing=16)

		card = Factory.Surface(orientation="vertical", padding=16, spacing=12)

		form = GridLayout(cols=2, size_hint_y=None, padding=5, spacing=10)
		form.bind(minimum_height=form.setter("height"))

		self.opt_10 = CheckBox(size_hint_y=None, height=40)
		self.opt_3to9 = CheckBox(size_hint_y=None, height=40)
		self.opt_lt3 = CheckBox(size_hint_y=None, height=40)
		self.opt_na = CheckBox(size_hint_y=None, height=40)
		form.add_widget(Label(text="C) Tándem · Mantuvo 10 s (2 puntos)", size_hint_y=None, height=40)); form.add_widget(self.opt_10)
		form.add_widget(Label(text="C) Mantuvo 3–9.99 s (1 punto)", size_hint_y=None, height=40)); form.add_widget(self.opt_3to9)
		form.add_widget(Label(text="C) < 3 s (0 puntos)", size_hint_y=None, height=40)); form.add_widget(self.opt_lt3)
		form.add_widget(Label(text="C) No intentado (0 puntos)", size_hint_y=None, height=40)); form.add_widget(self.opt_na)

		self._bind_exclusive(self.opt_10, self.opt_3to9, self.opt_lt3, self.opt_na)

		scroll = ScrollView(size_hint=(1, 1))
		scroll.add_widget(form)

		btns = BoxLayout(size_hint_y=None, height=56, spacing=10)
		back_btn = Factory.SecondaryButton(text="← Anterior")
		back_btn.bind(on_release=lambda *_: self.root_widget.goto("balance_semi"))
		next_btn = Factory.PrimaryButton(text="Siguiente →")
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

		form.add_widget(Label(text="Primera medición", size_hint_y=None, height=48)); form.add_widget(self.g1); form.add_widget(Label(text="No pudo", size_hint_y=None, height=48)); form.add_widget(self.g1_un)
		form.add_widget(Label(text="Segunda medición", size_hint_y=None, height=48)); form.add_widget(self.g2); form.add_widget(Label(text="No pudo", size_hint_y=None, height=48)); form.add_widget(self.g2_un)

		scroll = ScrollView(size_hint=(1, 1))
		scroll.add_widget(form)

		btns = BoxLayout(size_hint_y=None, height=56, spacing=10)
		next_btn = Factory.PrimaryButton(text="Siguiente")
		next_btn.bind(on_release=lambda *_: self.on_next())
		btns.add_widget(next_btn)

		title = Factory.TitleLabel(text="2. Velocidad de marcha (4 m)", size_hint_y=None, height=40)
		card.add_widget(title)
		card.add_widget(scroll)
		card.add_widget(btns)

		layout.add_widget(card)
		self.add_widget(layout)

	def on_pre_enter(self):
		self.update_progress()

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

		form.add_widget(Label(text="A) ¿Puede levantarse sin apoyarse?", size_hint_y=None, height=48)); form.add_widget(self.pre_unable)
		form.add_widget(Label(text="B) Tiempo 5x (s)", size_hint_y=None, height=48)); form.add_widget(self.time)
		form.add_widget(Label(text="No pudo completar", size_hint_y=None, height=48)); form.add_widget(self.unable)

		scroll = ScrollView(size_hint=(1, 1))
		scroll.add_widget(form)

		btns = BoxLayout(size_hint_y=None, height=56, spacing=10)
		next_btn = Factory.PrimaryButton(text="Ver resumen")
		next_btn.bind(on_release=lambda *_: self.on_next())
		btns.add_widget(next_btn)

		title = Factory.TitleLabel(text="3. Levantarse de la silla", size_hint_y=None, height=40)
		card.add_widget(title)
		card.add_widget(scroll)
		card.add_widget(btns)

		layout.add_widget(card)
		self.add_widget(layout)

	def on_pre_enter(self):
		self.update_progress()

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


class SummaryScreen(BaseScreen):
	def __init__(self, root, **kwargs):
		super().__init__(root, name="summary", **kwargs)
		layout = BoxLayout(orientation="vertical", padding=20, spacing=16)

		card = Factory.Surface(orientation="vertical", padding=16, spacing=12)
		self.summary_label = Label(text="", size_hint_y=None, height=160)
		btns = BoxLayout(size_hint_y=None, height=56, spacing=10)
		send_btn = Factory.PrimaryButton(text="Enviar a Drive")
		send_btn.bind(on_release=lambda *_: self.on_send())
		btns.add_widget(send_btn)

		title = Factory.TitleLabel(text="Resumen final", size_hint_y=None, height=40)
		card.add_widget(title)
		card.add_widget(self.summary_label)
		card.add_widget(btns)

		layout.add_widget(card)
		self.add_widget(layout)

	def on_pre_enter(self):
		s = self.state.current_scores()
		self.summary_label.text = (
			f"Equilibrio: {s.balance_score}/4\n"
			f"Marcha: {s.gait_score}/4\n"
			f"Silla: {s.chair_score}/4\n"
			f"Total: {s.total}/12 - {s.interpretation}"
		)
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
	progress: ScoreSummaryLabel
	drive_url: str = ""
	logo_path: Optional[str] = None

	def __init__(self, **kwargs):
		super().__init__(orientation="vertical", **kwargs)
		self.state = SessionState()

		self.progress = ScoreSummaryLabel(text="Progreso · Equilibrio 0/4 · Marcha 0/4 · Silla 0/4 · Total 0/12", size_hint=(1, None), height=36)

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

		self.add_widget(self.progress)
		self.add_widget(self.sm)
		self.add_widget(actions)
		self.add_widget(self.status_label)

		self.goto("start")

	def goto(self, name: str):
		self.sm.current = name
		self.cancel_btn.text = "Salir" if name == "start" else "Cancelar"
		self.progress.update(self.state)

	def on_cancel(self):
		if self.sm.current == "start":
			App.get_running_app().stop()
			return
		self.state.reset()
		self.status_label.text = "Operación cancelada"
		self.goto("start")
