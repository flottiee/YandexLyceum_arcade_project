import json
import arcade
import constants

class FinishView(arcade.View):
    def __init__(self, final_time=0.0):
        super().__init__()
        self.camera = arcade.Camera2D()
        self.final_time = final_time

    def on_show_view(self):
        arcade.set_background_color(arcade.color.GOLD)

    def on_draw(self):
        self.clear()
        self.camera.use()
        arcade.draw_text("ФИНИШ!", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        time_text = f"Время: {self.final_time:.2f} сек" if self.final_time > 0 else "Время не записано"
        arcade.draw_text(time_text, 
                         constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 60,
                         arcade.color.BLACK, font_size=20, anchor_x="center")
        arcade.draw_text("Вы прошли все уровни. Нажмите ESC для выхода.", 
                         constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 120,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()

    def get_total_stats(self):
        try:
            with open("race_history.json", "r") as f:
                history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0, 0

        total_p1 = sum(item["p1_time"] for item in history)
        total_p2 = sum(item["p2_time"] for item in history)
        
        return total_p1, total_p2