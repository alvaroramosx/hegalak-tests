from __future__ import annotations

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.utils import get_color_from_hex as rgba

from .ui.screens import WizardRoot


class SPPBApp(App):
	def build(self):
		self.title = "SPPB"
		Window.size = (480, 800)
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
