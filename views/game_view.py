import datetime
import json
import arcade
from pyglet.graphics import Batch

import constants
import math
from entities.Car import Car
from .game_factory import ViewFactory


class GameView(arcade.View):
    def __init__(self, level_index, name_p1, name_p2, menu):
        super().__init__()
        arcade.set_background_color(arcade.color.BLUEBERRY)
        self.name_p1 = name_p1
        self.name_p2 = name_p2
        self.menu = menu

        self.level_index = level_index

        self.p1_time = 0.0
        self.p2_time = 0.0
        self.start_time = 0.0
        self.final_time = 0.0
        self.race_active = False
        self.time_before_start = 3

        self.level_data = constants.LEVELS[self.level_index]

        self.world_camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()

        self.pressed_keys = set()

        self.batch = Batch()

        self.p1_started = False
        self.p2_started = False
        self.p1_passed_checkpoint = False
        self.p2_passed_checkpoint = False
        self.p1_on_line_last_frame = False
        self.p2_on_line_last_frame = False
        self.p1_wrong_way = False
        self.p2_wrong_way = False
        self.setup()

    def setup(self):
        self.p1 = Car(self.level_data["track_id"], player_id=1, control_type="arrows")
        self.p2 = Car(self.level_data["track_id"], player_id=2, control_type="wasd")

        self.car_list = arcade.SpriteList()
        self.car_list.append(self.p1)
        self.car_list.append(self.p2)

        self.lap_complete = arcade.load_sound('assets/sounds/lap_complete.mp3')
        self.map = arcade.load_tilemap(self.level_data["map_path"], 0.5)

        self.race_track = self.map.sprite_lists.get('race_track', arcade.SpriteList())
        self.objects = self.map.sprite_lists.get('objects', arcade.SpriteList())
        self.finish_line = self.map.sprite_lists.get('finish_line', arcade.SpriteList())
        self.fon = self.map.sprite_lists.get('fon', arcade.SpriteList())
        self.block_wall = self.map.sprite_lists.get('block_wall', arcade.SpriteList())
        self.oil_list = self.map.sprite_lists.get('oil', arcade.SpriteList())

        self.walls_car1 = arcade.SpriteList(use_spatial_hash=True)
        self.walls_car2 = arcade.SpriteList(use_spatial_hash=True)
        if 'walls' in self.map.sprite_lists:
            self.walls_car1.extend(self.map.sprite_lists['walls'])
            self.walls_car2.extend(self.map.sprite_lists['walls'])

        self.engine1 = arcade.PhysicsEngineSimple(self.p1, self.walls_car1)
        self.engine2 = arcade.PhysicsEngineSimple(self.p2, self.walls_car2)

        layer_options = {
            "checkpoints": {
                "use_spatial_hash": True,
            },
            "finish_line": {
                "use_spatial_hash": True,
            }
        }

        self.map = arcade.load_tilemap(
            self.level_data["map_path"],
            scaling=0.5,
            layer_options=layer_options
        )

        self.passed_checkpoint = False
        self.race_started = False
        self.is_wrong_way_blocked = False

        self.checkpoints = self.map.sprite_lists.get('checkpoints', arcade.SpriteList())
        self.finish_line = self.map.sprite_lists.get('finish_line', arcade.SpriteList())

        if len(self.checkpoints) == 0:
            print("ПРЕДУПРЕЖДЕНИЕ: Слой checkpoints все еще пуст!")

        self.checkpoints = self.map.sprite_lists.get('checkpoints', arcade.SpriteList())
        print(f"DEBUG: Количество объектов в слое checkpoints: {len(self.checkpoints)}")

        for obj in self.checkpoints:
            print(f"DEBUG: Обнаружен объект в {obj.center_x}, {obj.center_y}")


        self.instructions = arcade.Text(f'<^>V - {self.name_p1}, WASD - {self.name_p2}', 15,
                                        25, arcade.color.WHITE, 15,
                                        font_name="Kenney Future", batch=self.batch)

    def on_draw(self):
        self.clear()

        self.world_camera.use()
        self.fon.draw()
        self.race_track.draw()
        self.objects.draw()
        self.oil_list.draw()
        for car in self.car_list:
            car.draw_particles()
        self.car_list.draw()

        self.gui_camera.use()
        self.batch.draw()

    def update_hud(self):
        self.t1 = arcade.Text(f"{self.name_p1}: {self.p1_time:.2f}" if self.p1_started else f"{self.name_p1}: ЖДЕТ СТАРТА", 20,
                              self.window.height - 70, arcade.color.RED, 16,
                              font_name="Kenney Future", batch=self.batch)
        self.t2 = arcade.Text(f"{self.name_p2}: {self.p2_time:.2f}" if self.p2_started else f"{self.name_p2}: ЖДЕТ СТАРТА", 20,
                              self.window.height - 100, arcade.color.GOLD, 16,
                              font_name="Kenney Future", batch=self.batch)

        if not self.race_started:
            text = "ПЕРЕСЕКИТЕ ЛИНИЮ ДЛЯ СТАРТА"
            self.phrase = arcade.Text(text, 20, self.window.height - 40,
                                      arcade.color.WHITE, 20, font_name="Kenney Future", batch=self.batch)
        else:
            self.phrase = None

        if self.time_before_start != 0:
            self.time_before_start_text = arcade.Text(f'{self.time_before_start:.0f}', self.window.width / 2,
                                                  self.window.height / 2, arcade.color.WHITE, 20,
                                                  font_name="Kenney Future", anchor_x="center",
                                                  batch=self.batch)
        else:
            self.time_before_start_text = None

        if self.p1_wrong_way or self.p2_wrong_way:
            self.wrong_direction = arcade.Text("НЕВЕРНОЕ НАПРАВЛЕНИЕ!", self.window.width / 2, 50,
                                               arcade.color.RED, 30, font_name="Kenney Future",
                                               anchor_x="center", batch=self.batch)
        else:
            self.wrong_direction = None

    def on_update(self, dt):
        self.p1.update_input(
            arcade.key.UP in self.pressed_keys, arcade.key.DOWN in self.pressed_keys,
            arcade.key.LEFT in self.pressed_keys, arcade.key.RIGHT in self.pressed_keys
        )
        self.p2.update_input(
            arcade.key.W in self.pressed_keys, arcade.key.S in self.pressed_keys,
            arcade.key.A in self.pressed_keys, arcade.key.D in self.pressed_keys
        )
        if not self.race_active:
            self.time_before_start = max(self.time_before_start - dt, 0)
            if self.time_before_start == 0:
                self.race_active = True
        else:

            if not self.p1.is_finished:
                if self.p1_started: self.p1_time += dt
                self.p1.update_car(dt)
                self.engine1.update()

            if not self.p2.is_finished:
                if self.p2_started: self.p2_time += dt
                self.p2.update_car(dt)
                self.engine2.update()

            if self.p1_started and self.p2_started:
                self.race_started = True

            # ЦИКЛ ОБРАБОТКИ ЛОГИКИ ДЛЯ ОБОИХ ИГРОКОВ
            for i, car in enumerate(self.car_list):
                # масло и препятствия
                if arcade.check_for_collision_with_list(car, self.oil_list): car.hit_oil()
                if i == 0:
                    if arcade.check_for_collision_with_list(car, self.walls_car1): car.on_wall_hit()
                elif i == 1:
                    if arcade.check_for_collision_with_list(car, self.walls_car1): car.on_wall_hit()
                # чекпоинты
                if arcade.check_for_collision_with_list(car, self.checkpoints):
                    if i == 0:
                        self.p1_passed_checkpoint = True
                    else:
                        self.p2_passed_checkpoint = True
                    self.unlock_block_walls()

                # финишная линия (логика пересечения)
                on_line = arcade.check_for_collision_with_list(car, self.finish_line)
                last_frame = self.p1_on_line_last_frame if i == 0 else self.p2_on_line_last_frame

                if on_line and not last_frame:
                    self.handle_finish_line_collision(car, i)

                if i == 0:
                    self.p1_on_line_last_frame = bool(on_line)
                else:
                    self.p2_on_line_last_frame = bool(on_line)

            # Проверка завершения уровня
            if self.p1.is_finished and self.p2.is_finished:
                self.save_results()
                self.next_level()

        self.update_camera()
        self.update_hud()

    def unlock_block_walls(self):
        # Блокировочная стена возникает только если оба пересекли чекпоинт
        if self.p1_passed_checkpoint:
            if self.block_wall and len(self.block_wall) > 0:
                for sprite in self.block_wall:
                    if sprite not in self.walls_car1:
                        self.walls_car1.append(sprite)
        if self.p2_passed_checkpoint:
            if self.block_wall and len(self.block_wall) > 0:
                for sprite in self.block_wall:
                    if sprite not in self.walls_car2:
                        self.walls_car2.append(sprite)
                self.block_wall.clear()

    def handle_finish_line_collision(self, car, player_idx):
        angle_rad = math.radians(car.angle)
        dot = (math.sin(angle_rad) * self.level_data.get("finish_dir", (0, 1))[0]) + \
              (math.cos(angle_rad) * self.level_data.get("finish_dir", (0, 1))[1])

        if dot > 0:
            if player_idx == 0:
                if not self.p1_started:
                    self.p1_started = True
                elif self.p1_passed_checkpoint:
                    car.is_finished = True; self.lap_complete.play()
                self.p1_wrong_way = False
            else:
                if not self.p2_started:
                    self.p2_started = True
                elif self.p2_passed_checkpoint:
                    car.is_finished = True; self.lap_complete.play()
                self.p2_wrong_way = False
        else:
            if player_idx == 0 and self.p1_started:
                self.p1_wrong_way = True
            elif player_idx == 1 and self.p2_started:
                self.p2_wrong_way = True

    def next_level(self):
        finish_view = ViewFactory.create_finish_view(
            self.level_index,
            self.p1_time,
            self.p2_time,
            self.name_p1,
            self.name_p2,
            self.menu
        )
        self.window.show_view(finish_view)

    def update_camera(self):
        # ИЗМЕНЕНО: Камера следит за двумя игроками
        mid_x = (self.p1.center_x + self.p2.center_x) / 2
        mid_y = (self.p1.center_y + self.p2.center_y) / 2

        dist = math.sqrt((self.p1.center_x - self.p2.center_x) ** 2 + (self.p1.center_y - self.p2.center_y) ** 2)

        # Динамический зум под двоих
        target_zoom = max(constants.MIN_ZOOM, min(constants.MAX_ZOOM, 1000 / (dist + 500)))
        self.world_camera.zoom = arcade.math.lerp(self.world_camera.zoom, target_zoom, constants.ZOOM_LERP)

        cam_x, cam_y = self.world_camera.position
        self.world_camera.position = (
            arcade.math.lerp(cam_x, mid_x, constants.CAMERA_LERP),
            arcade.math.lerp(cam_y, mid_y, constants.CAMERA_LERP)
        )

    def on_key_press(self, key, modifiers):
        self.pressed_keys.add(key)

    def on_key_release(self, key, modifiers):
        self.pressed_keys.discard(key)

    def save_results(self):
        new_result = {
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "level": self.level_index,
            "p1_time": round(self.p1_time, 2),
            "p2_time": round(self.p2_time, 2),
            "winner": "P1" if self.p1_time < self.p2_time else "P2"
        }

        try:
            with open("race_history.json", "r", encoding="utf-8") as f:
                history = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []

        history.append(new_result)

        with open("race_history.json", "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
