import arcade
from arcade.gui import UIManager, UIAnchorLayout, UIBoxLayout, UILabel, UIInputText, UITextureButton
from pyglet.graphics import Batch

import constants
from .game_view import GameView

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.main_lay = UIBoxLayout(vertical=True, space_between=10)
        self.players_lay = UIBoxLayout(vertical=False, space_between=10)

        self.setup_widgets()

        self.anchor_layout.add(self.main_lay)
        self.manager.add(self.anchor_layout)

        self.player1_name = "Player 1"
        self.player2_name = "Player 2"

        self.now_idx = 0

    def setup_widgets(self):
        label = UILabel(text="Аркадные гонки",
                        font_size=50,
                        text_color=arcade.color.WHITE,
                        bold=True,
                        font_name="Kenney Future",
                        align="center")
        self.main_lay.add(label)

        self.p1_input = UIInputText(
            width=200,
            height=30,
            text="Player 1",
            font_name="Kenney Future",
            font_size=15
        )
        self.p1_input.on_change = lambda event: self.change_p1_name()
        self.players_lay.add(self.p1_input)

        self.p2_input = UIInputText(
            width=200,
            height=30,
            text="Player 2",
            font_name="Kenney Future",
            font_size=15
        )
        self.p2_input.on_change = lambda event: self.change_p2_name()
        self.players_lay.add(self.p2_input)

        self.main_lay.add(self.players_lay)

        texture_normal = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")
        texture_hovered = arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png")
        texture_pressed = arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png")
        texture_button = UITextureButton(texture=texture_normal,
                                         texture_hovered=texture_hovered,
                                         texture_pressed=texture_pressed,
                                         text='Начать игру',
                                         scale=1.0)
        texture_button.on_click = lambda event: self.start_game()
        self.main_lay.add(texture_button)

    def change_p1_name(self):
        """Обработчик изменения имени игрока 1"""
        self.player1_name = self.p1_input.text
        if len(self.player1_name) > 10:
            self.player1_name = self.player1_name[:10]
        print(f"Игрок 1: {self.player1_name}")

    def change_p2_name(self):
        """Обработчик изменения имени игрока 2"""
        self.player2_name = self.p2_input.text
        if len(self.player2_name) > 10:
            self.player2_name = self.player2_name[:10]
        print(f"Игрок 2: {self.player2_name}")

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_SLATE_BLUE)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def start_game(self):
        game_view = GameView(level_index=self.now_idx, menu=self, name_p1=self.player1_name, name_p2=self.player2_name)
        if self.now_idx < 2:
            self.now_idx += 1
        else:
            self.now_idx = 0
        self.window.show_view(game_view)