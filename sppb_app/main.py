from __future__ import annotations

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.utils import get_color_from_hex as rgba

from .ui.screens import WizardRoot
from . import config


class SPPBApp(App):
	def build(self):
		self.title = "SPPB"
		# Detecta si es dispositivo móvil (Android/iOS) o escritorio
		try:
			from kivy.utils import platform as _platform
		except Exception:
			_platform = None

		def _auto_kind():
			if _platform in ("android", "ios"):
				return "phone"  # pantalla completa; el gestor del SO decide
			# En escritorio, distinguimos por DPI y tamaño físico aproximado
			try:
				w, h = Window.size
				dpi = Window.dpi or 96
				# diagonal en pulgadas aproximada
				diagonal_inches = ((w / dpi) ** 2 + (h / dpi) ** 2) ** 0.5
				return "tablet" if diagonal_inches >= 9.0 else "phone"
			except Exception:
				return "phone"

		device_kind = (config.DEVICE_KIND or _auto_kind()).lower()
		if _platform not in ("android", "ios"):
			# Solo fijamos tamaño en escritorio
			if device_kind == "tablet":
				Window.size = tuple(config.TABLET_WINDOW_SIZE)
			else:
				Window.size = tuple(config.PHONE_WINDOW_SIZE)
		Window.clearcolor = rgba('#F8F3EA')
		try:
			Builder.load_file('sppb_app/ui/theme.kv')
		except Exception:
			pass
		return WizardRoot()


def main():
	SPPBApp().run()


if __name__ == "__main__":
	main()
