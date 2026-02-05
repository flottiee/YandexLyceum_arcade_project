import json
import arcade
from pyglet.graphics import Batch

import constants


class FinishView(arcade.View):
    def __init__(self, p1_time=0.0, p2_time=0.0, menu=None):
        super().__init__()
        self.menu = menu

        self.camera = arcade.Camera2D()
        self.p1_time = p1_time
        self.p2_time = p2_time

        self.batch = Batch()
        self.finish = arcade.Text("ФИНИШ!", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2,
                                  arcade.color.BLACK, font_size=50, anchor_x="center", batch=self.batch)
        self.text_1 = arcade.Text(f"Время игрока 1: {self.p1_time:.2f} сек", constants.SCREEN_WIDTH / 2,
                                  constants.SCREEN_HEIGHT / 2 - 60,
                                  arcade.color.BLACK, font_size=20, anchor_x="center",
                                  batch=self.batch) if self.p1_time > 0 else "Время не записано"
        self.text_2 = arcade.Text(f"Время игрока 2: {self.p1_time:.2f} сек", constants.SCREEN_WIDTH / 2,
                                  constants.SCREEN_HEIGHT / 2 - 100,
                                  arcade.color.BLACK, font_size=20, anchor_x="center",
                                  batch=self.batch) if self.p2_time > 0 else "Время не записано"
        self.exit = arcade.Text("Нажмите ESC для выхода в меню.",
                                constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 160,
                                arcade.color.BLACK, font_size=20, anchor_x="center", batch=self.batch)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.GOLD)

    def on_draw(self):
        self.clear()
        self.camera.use()

        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.menu)

    def get_total_stats(self):
        try:
            with open("race_history.json", "r") as f:
                history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0, 0

        total_p1 = sum(item["p1_time"] for item in history)
        total_p2 = sum(item["p2_time"] for item in history)
        
        return total_p1, total_p2