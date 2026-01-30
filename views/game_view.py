import arcade
import constants
import time
import math
from entities.Car import Car
from .finish_view import FinishView

class GameView(arcade.View):
    def __init__(self, level_index):
        super().__init__()
        self.level_index = level_index
        self.level_data = constants.LEVELS[level_index]
        
        self.world_camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()
        
        self.race_started = False
        self.is_wrong_way_blocked = False  # Флаг, если заехал сзади
        self.start_time = 0.0
        self.final_time = 0.0
        
        self.pressed_keys = set()
        self.on_line_last_frame = False # Для фиксации момента пересечения
        
        self.setup()

    def setup(self):
        self.car = Car(self.level_data["track_id"])
        self.car_list = arcade.SpriteList()
        self.car_list.append(self.car)

        self.lap_complete = arcade.load_sound('sounds/lap_complete.mp3')
        self.map = arcade.load_tilemap(self.level_data["map_path"], 0.5)
        
        self.race_track = self.map.sprite_lists.get('race_track', arcade.SpriteList())
        self.objects = self.map.sprite_lists.get('objects', arcade.SpriteList())
        self.finish_line = self.map.sprite_lists.get('finish_line', arcade.SpriteList())
        
        self.walls = arcade.SpriteList(use_spatial_hash=True)
        if 'walls' in self.map.sprite_lists:
            self.walls.extend(self.map.sprite_lists['walls'])

        self.engine = arcade.PhysicsEngineSimple(self.car, self.walls)
        
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

    def on_draw(self):
        self.clear()
        
        self.world_camera.use()
        self.race_track.draw()
        self.objects.draw()
        self.car_list.draw()
        
        self.gui_camera.use()
        self.draw_hud()

    def draw_hud(self):
        if self.race_started:
            elapsed = time.time() - self.start_time
            text = f"ВРЕМЯ: {elapsed:.2f} сек"
        else:
            text = "ПЕРЕСЕКИТЕ ЛИНИЮ ДЛЯ СТАРТА"
            
        arcade.draw_text(text, 20, self.window.height - 40, 
                         arcade.color.WHITE, 20, font_name="Kenney Future")
        
        if self.is_wrong_way_blocked:
            arcade.draw_text("НЕВЕРНОЕ НАПРАВЛЕНИЕ!", self.window.width/2, 50,
                             arcade.color.RED, 30, anchor_x="center")

    def on_update(self, dt):
        up = arcade.key.UP in self.pressed_keys or arcade.key.W in self.pressed_keys
        down = arcade.key.DOWN in self.pressed_keys or arcade.key.S in self.pressed_keys
        left = arcade.key.LEFT in self.pressed_keys or arcade.key.A in self.pressed_keys
        right = arcade.key.RIGHT in self.pressed_keys or arcade.key.D in self.pressed_keys

        self.car.update_input(up, down, left, right)
        self.car.update_car()
        self.engine.update()

        on_line_now = arcade.check_for_collision_with_list(self.car, self.finish_line)
        
        if on_line_now and not self.on_line_last_frame:
            self.handle_finish_line_collision()
            
        self.on_line_last_frame = bool(on_line_now)

        if arcade.check_for_collision_with_list(self.car, self.checkpoints):
            self.passed_checkpoint = True

        self.update_camera()

    def handle_finish_line_collision(self):
        """Логика старта, финиша и проверки направления"""
        angle_rad = math.radians(self.car.angle)
        car_dir_x = math.sin(angle_rad)
        car_dir_y = math.cos(angle_rad)
        
        finish_dir = self.level_data.get("finish_dir", (0, 1))
        
        dot_product = (car_dir_x * finish_dir[0]) + (car_dir_y * finish_dir[1])

        if dot_product > 0:
            if not self.race_started:
                # ПЕРВЫЙ СТАРТ
                self.race_started = True
                self.start_time = time.time()
                self.is_wrong_way_blocked = False
            elif self.is_wrong_way_blocked:
                self.is_wrong_way_blocked = False
            elif self.passed_checkpoint:
                self.final_time = time.time() - self.start_time
                self.lap_complete.play()
                self.next_level()
        else:
            if self.race_started:
                self.is_wrong_way_blocked = True

    def next_level(self):
        next_idx = self.level_index + 1
        if next_idx < len(constants.LEVELS):
            new_view = GameView(next_idx)
            self.window.show_view(new_view)
        else:
            self.window.show_view(FinishView(self.final_time))

    def update_camera(self):
        map_width = self.map.width * self.map.tile_width * self.map.scaling
        map_height = self.map.height * self.map.tile_height * self.map.scaling

        # Плавное следование за машиной
        cam_x, cam_y = self.world_camera.position
        new_x = cam_x + (self.car.center_x - cam_x) * constants.CAMERA_LERP
        new_y = cam_y + (self.car.center_y - cam_y) * constants.CAMERA_LERP

        # Динамический зум
        speed_ratio = min(abs(self.car.speed) / self.car.max_forward_speed, 1.0)
        target_zoom = constants.MAX_ZOOM - (speed_ratio * (constants.MAX_ZOOM - constants.MIN_ZOOM))
        self.world_camera.zoom = self.world_camera.zoom + (target_zoom - self.world_camera.zoom) * constants.ZOOM_LERP

        # Ограничение границ
        half_w = (self.window.width / 2) / self.world_camera.zoom
        half_h = (self.window.height / 2) / self.world_camera.zoom
        
        self.world_camera.position = (
            max(half_w, min(map_width - half_w, new_x)),
            max(half_h, min(map_height - half_h, new_y))
        )

    def on_key_press(self, key, modifiers):
        self.pressed_keys.add(key)

    def on_key_release(self, key, modifiers):
        self.pressed_keys.discard(key)