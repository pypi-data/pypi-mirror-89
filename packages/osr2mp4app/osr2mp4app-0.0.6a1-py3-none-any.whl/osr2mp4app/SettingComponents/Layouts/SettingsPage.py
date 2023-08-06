from BaseComponents.Buttons import Button
from SettingComponents.Layouts.ScrollArea import ScrollArea


def get_arearect(settings):
	area_width = settings.default_width
	area_height = settings.default_height

	middle_x = settings.default_x + settings.default_width/2
	middle_y = settings.default_y + settings.default_height/2

	return 0, 0, area_width, area_height


class SettingsPage(Button):
	def __init__(self, parent):
		super(SettingsPage, self).__init__(parent)

		self.default_x = 20
		self.default_y = 20
		self.default_size = 4

		self.img_idle = "res/WindowShadow.png"
		self.img_hover = "res/WindowShadow.png"
		self.img_click = "res/WindowShadow.png"

		super().setup()

		self.settingsarea = ScrollArea(self, parent)

		self.hide()
		self.load_settings()

	def changesize(self):
		super().changesize()
		self.settingsarea.changesize()

	def load_settings(self):
		self.settingsarea.load_settings()

	def reload_settings(self):
		self.settingsarea.reload_settings()

	def updatevalue(self):
		self.settingsarea.gridLayout.updatevalue()

