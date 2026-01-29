import arcade
import constants

class FinishView(arcade.View):
    def __init__(self):
        super().__init__()
        self.camera = arcade.Camera2D()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.GOLD)

    def on_draw(self):
        self.clear()
        self.camera.use()
        arcade.draw_text("ФИНИШ!", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Вы прошли все уровни. Нажмите ESC для выхода.", 
                         constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 60,
                         arcade.color.BLACK, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()