import arcade
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
        
        self.camera = arcade.Camera2D()
        self.ui_text_list = arcade.SpriteList()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.GOLD if self.is_final else arcade.color.DARK_SLATE_GRAY)

    def on_draw(self):
        self.clear()
        self.camera.use()
        
        cx = constants.SCREEN_WIDTH / 2
        cy = constants.SCREEN_HEIGHT - 100

        if not self.is_final:
            # Окно между уровнями
            last = self.results_history[-1]
            arcade.draw_text(f"ЭТАП {last['level']} ЗАВЕРШЕН", cx, cy, arcade.color.BLACK, 40, anchor_x="center", font_name="Kenney Future")
            arcade.draw_text(f"{self.p1_name}: {last['p1_time']:.2f} сек", cx, cy - 80, arcade.color.WHITE, 20, anchor_x="center")
            arcade.draw_text(f"{self.p2_name}: {last['p2_time']:.2f} сек", cx, cy - 120, arcade.color.WHITE, 20, anchor_x="center")
            arcade.draw_text("Нажмите ENTER, чтобы продолжить", cx, cy - 250, arcade.color.BLACK, 15, anchor_x="center")
        else:
            # Финальная таблица
            arcade.draw_text("ИТОГОВЫЙ ПРОТОКОЛ", cx, cy, arcade.color.BLACK, 35, anchor_x="center", font_name="Kenney Future")
            
            start_y = cy - 80
            # Заголовки таблицы
            arcade.draw_text(f"{'Уровень':<10} | {self.p1_name:<15} | {self.p2_name:<15}", cx, start_y, arcade.color.BLACK, 18, anchor_x="center", font_name="Courier New", bold=True)
            
            total_p1 = 0
            total_p2 = 0
            
            for i, res in enumerate(self.results_history):
                row_y = start_y - 40 - (i * 30)
                total_p1 += res['p1_time']
                total_p2 += res['p2_time']
                arcade.draw_text(f"Заезд {res['level']:<3} | {res['p1_time']:>13.2f}с | {res['p2_time']:>13.2f}с", 
                                 cx, row_y, arcade.color.DARK_BLUE, 16, anchor_x="center", font_name="Courier New")

            # Сумма и среднее
            sep_y = start_y - 40 - (len(self.results_history) * 30) - 20
            arcade.draw_text("-" * 50, cx, sep_y + 15, arcade.color.BLACK, 16, anchor_x="center")
            arcade.draw_text(f"СУММА:    {total_p1:>14.2f}с | {total_p2:>14.2f}с", cx, sep_y, arcade.color.BLACK, 16, anchor_x="center", bold=True)
            
            avg_p1 = total_p1 / len(self.results_history)
            avg_p2 = total_p2 / len(self.results_history)
            arcade.draw_text(f"СРЕДНЕЕ:  {avg_p1:>14.2f}с | {avg_p2:>14.2f}с", cx, sep_y - 30, arcade.color.BLACK, 16, anchor_x="center")
            
            arcade.draw_text("Нажмите ESC для выхода в меню", cx, 50, arcade.color.BLACK, 15, anchor_x="center")

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