# game_factory.py


class ViewFactory:
    @staticmethod
    def create_game_view(level_index, name_p1, name_p2, menu):
        from .game_view import GameView
        return GameView(level_index, name_p1, name_p2, menu)

    @staticmethod
    def create_finish_view(level_idx, p1_time, p2_time, p1_name, p2_name, menu):
        from .finish_view import FinishView
        return FinishView(level_idx, p1_time, p2_time, p1_name, p2_name, menu)