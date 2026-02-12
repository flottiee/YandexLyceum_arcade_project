import arcade
from pyglet.graphics import Batch
from .game_factory import ViewFactory

import constants

class FinishView(arcade.View):
    def __init__(self, results_history, menu, p1_name, p2_name, is_final, current_level_idx):
        super().__init__()
        self.results_history = results_history
        self.menu = menu
        self.p1_name = p1_name
        self.p2_name = p2_name
        self.is_final = is_final
        self.current_level_idx = current_level_idx

        self.batch = Batch()
        self.text_objects = []
        
        self.camera = arcade.Camera2D()
        self.ui_text_list = arcade.SpriteList()

        self.create_texts()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.GOLD if self.is_final else arcade.color.DARK_SLATE_GRAY)

    def create_texts(self):
        """Создает все текстовые объекты и добавляет их в batch"""
        self.text_objects.clear()

        cx = constants.SCREEN_WIDTH / 2
        cy = constants.SCREEN_HEIGHT - 100

        if not self.is_final:
            last = self.results_history[-1]

            self.text_objects.append(arcade.Text(
                f"ЭТАП {last['level']} ЗАВЕРШЕН",
                cx, cy,
                arcade.color.BLACK, 40,
                anchor_x="center",
                font_name="Kenney Future",
                batch=self.batch
            ))

            self.text_objects.append(arcade.Text(
                f"{self.p1_name}: {last['p1_time']:.2f} сек",
                cx, cy - 80,
                arcade.color.WHITE, 20,
                anchor_x="center",
                batch=self.batch
            ))

            self.text_objects.append(arcade.Text(
                f"{self.p2_name}: {last['p2_time']:.2f} сек",
                cx, cy - 120,
                arcade.color.WHITE, 20,
                anchor_x="center",
                batch=self.batch
            ))

            self.text_objects.append(arcade.Text(
                "Нажмите ENTER, чтобы продолжить",
                cx, cy - 250,
                arcade.color.BLACK, 15,
                anchor_x="center",
                batch=self.batch
            ))
        else:
            self.text_objects.append(arcade.Text(
                "ИТОГОВЫЙ ПРОТОКОЛ",
                cx, cy,
                arcade.color.BLACK, 35,
                anchor_x="center",
                font_name="Kenney Future",
                batch=self.batch
            ))

            start_y = cy - 80

            self.text_objects.append(arcade.Text(
                f"{'Уровень':<10} | {self.p1_name:<15} | {self.p2_name:<15}",
                cx, start_y,
                arcade.color.BLACK, 18,
                anchor_x="center",
                font_name="Courier New",
                bold=True,
                batch=self.batch
            ))

            total_p1 = 0
            total_p2 = 0

            for i, res in enumerate(self.results_history):
                row_y = start_y - 40 - (i * 30)
                total_p1 += res['p1_time']
                total_p2 += res['p2_time']

                self.text_objects.append(arcade.Text(
                    f"Заезд {res['level']:<3} | {res['p1_time']:>13.2f}с | {res['p2_time']:>13.2f}с",
                    cx, row_y,
                    arcade.color.DARK_BLUE, 16,
                    anchor_x="center",
                    font_name="Courier New",
                    batch=self.batch
                ))

            sep_y = start_y - 40 - (len(self.results_history) * 30) - 20

            self.text_objects.append(arcade.Text(
                "-" * 50,
                cx, sep_y + 15,
                arcade.color.BLACK, 16,
                anchor_x="center",
                batch=self.batch
            ))

            self.text_objects.append(arcade.Text(
                f"СУММА:    {total_p1:>14.2f}с | {total_p2:>14.2f}с",
                cx, sep_y,
                arcade.color.BLACK, 16,
                anchor_x="center",
                bold=True,
                batch=self.batch
            ))

            avg_p1 = total_p1 / len(self.results_history)
            avg_p2 = total_p2 / len(self.results_history)

            self.text_objects.append(arcade.Text(
                f"СРЕДНЕЕ:  {avg_p1:>14.2f}с | {avg_p2:>14.2f}с",
                cx, sep_y - 30,
                arcade.color.BLACK, 16,
                anchor_x="center",
                batch=self.batch
            ))

            self.text_objects.append(arcade.Text(
                "Нажмите ESC для выхода в меню",
                cx, 50,
                arcade.color.BLACK, 15,
                anchor_x="center",
                batch=self.batch
            ))

    def on_draw(self):
        self.clear()
        self.camera.use()
        #
        # cx = constants.SCREEN_WIDTH / 2
        # cy = constants.SCREEN_HEIGHT - 100
        #
        # if not self.is_final:
        #     # Окно между уровнями
        #     last = self.results_history[-1]
        #     arcade.Text(f"ЭТАП {last['level']} ЗАВЕРШЕН", cx, cy, arcade.color.BLACK, 40, anchor_x="center", font_name="Kenney Future", batch=self.batch)
        #     arcade.Text(f"{self.p1_name}: {last['p1_time']:.2f} сек", cx, cy - 80, arcade.color.WHITE, 20, anchor_x="center", batch=self.batch)
        #     arcade.Text(f"{self.p2_name}: {last['p2_time']:.2f} сек", cx, cy - 120, arcade.color.WHITE, 20, anchor_x="center", batch=self.batch)
        #     arcade.Text("Нажмите ENTER, чтобы продолжить", cx, cy - 250, arcade.color.BLACK, 15, anchor_x="center", batch=self.batch)
        #
        # else:
        #     # Финальная таблица
        #     arcade.Text("ИТОГОВЫЙ ПРОТОКОЛ", cx, cy, arcade.color.BLACK, 35, anchor_x="center", font_name="Kenney Future", batch=self.batch)
        #
        #     start_y = cy - 80
        #     # Заголовки таблицы
        #     arcade.Text(f"{'Уровень':<10} | {self.p1_name:<15} | {self.p2_name:<15}", cx, start_y, arcade.color.BLACK, 18, anchor_x="center", font_name="Courier New", bold=True, batch=self.batch)
        #
        #     total_p1 = 0
        #     total_p2 = 0
        #
        #     for i, res in enumerate(self.results_history):
        #         row_y = start_y - 40 - (i * 30)
        #         total_p1 += res['p1_time']
        #         total_p2 += res['p2_time']
        #         arcade.Text(f"Заезд {res['level']:<3} | {res['p1_time']:>13.2f}с | {res['p2_time']:>13.2f}с",
        #                          cx, row_y, arcade.color.DARK_BLUE, 16, anchor_x="center", font_name="Courier New", batch=self.batch)
        #
        #     # Сумма и среднее
        #     sep_y = start_y - 40 - (len(self.results_history) * 30) - 20
        #     arcade.Text("-" * 50, cx, sep_y + 15, arcade.color.BLACK, 16, anchor_x="center", batch=self.batch)
        #     arcade.Text(f"СУММА:    {total_p1:>14.2f}с | {total_p2:>14.2f}с", cx, sep_y, arcade.color.BLACK, 16, anchor_x="center", bold=True, batch=self.batch)
        #
        #     avg_p1 = total_p1 / len(self.results_history)
        #     avg_p2 = total_p2 / len(self.results_history)
        #     arcade.Text(f"СРЕДНЕЕ:  {avg_p1:>14.2f}с | {avg_p2:>14.2f}с", cx, sep_y - 30, arcade.color.BLACK, 16, anchor_x="center", batch=self.batch)
        #
        #     arcade.Text("Нажмите ESC для выхода в меню", cx, 50, arcade.color.BLACK, 15, anchor_x="center", batch=self.batch)

        self.batch.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ENTER and not self.is_final:
            # Запуск следующего уровня
            from .game_view import GameView
            next_view = GameView(
                level_index=self.current_level_idx + 1, 
                menu=self.menu, 
                name_p1=self.p1_name, 
                name_p2=self.p2_name,
                results_history=self.results_history
            )
            self.window.show_view(next_view)
            
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.menu)
