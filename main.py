import os
from kivy.config import Config
Config.set('kivy', 'window_icon', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons', 'icon.png'))

from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from loading import *
from database.models import db, Product


class WorkCalculatorApp(MDApp):
    title = 'Work Calculator'

    def build(self):
        self.theme_cls = ThemeManager()
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue = "600"

        # Создаём таблицы при старте
        db.connect()
        db.create_tables([Product])
        db.close()

        return Box()


if __name__ == '__main__':
    WorkCalculatorApp().run()
