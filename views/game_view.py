import arcade
import constants
from entities.Car import Car
from .finish_view import FinishView

class GameView(arcade.View):
    def __init__(self, level_index):
        super().__init__()
        self.level_index = level_index
        self.level_data = constants.LEVELS[level_index]
        self.world_camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()
        self.pressed_keys = set()
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
        self.world_camera = arcade.Camera2D()
        self.is_on_finish_line = False

        self.checkpoints = self.map.sprite_lists.get('checkpoints', arcade.SpriteList())
        self.passed_checkpoint = False

    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.race_track.draw()
        self.car_list.draw()
        self.gui_camera.use()

    def on_update(self, dt):
        up = arcade.key.UP in self.pressed_keys or arcade.key.W in self.pressed_keys
        down = arcade.key.DOWN in self.pressed_keys or arcade.key.S in self.pressed_keys
        left = arcade.key.LEFT in self.pressed_keys or arcade.key.A in self.pressed_keys
        right = arcade.key.RIGHT in self.pressed_keys or arcade.key.D in self.pressed_keys

        self.car.update_input(up, down, left, right)
        self.car.update_car()
        self.engine.update()

        if arcade.check_for_collision_with_list(self.car, self.finish_line):
            if not self.is_on_finish_line:
                self.is_on_finish_line = True
                self.lap_complete.play()
                self.next_level()
        else:
            self.is_on_finish_line = False

        if arcade.check_for_collision_with_list(self.car, self.checkpoints):
            self.passed_checkpoint = True

        if arcade.check_for_collision_with_list(self.car, self.finish_line):
            if not self.is_on_finish_line:
                self.is_on_finish_line = True
                if self.passed_checkpoint:
                    self.lap_complete.play()
                    self.next_level()
        else:
            self.is_on_finish_line = False

        self.update_camera()

    def next_level(self):
        next_idx = self.level_index + 1
        if next_idx < len(constants.LEVELS):
            new_view = GameView(next_idx)
            self.window.show_view(new_view)
        else:
            finish_view = FinishView()
            self.window.show_view(finish_view)

    def update_camera(self):
        map_width = self.map.width * self.map.tile_width * self.map.scaling
        map_height = self.map.height * self.map.tile_height * self.map.scaling

        target_x = self.car.center_x
        target_y = self.car.center_y

        cam_x, cam_y = self.world_camera.position
        
        new_x = cam_x + (target_x - cam_x) * constants.CAMERA_LERP
        new_y = cam_y + (target_y - cam_y) * constants.CAMERA_LERP

        speed_ratio = min(abs(self.car.speed) / self.car.max_forward_speed, 1.0)
        
        target_zoom = constants.MAX_ZOOM - (speed_ratio * (constants.MAX_ZOOM - constants.MIN_ZOOM))
        
        current_zoom = self.world_camera.zoom
        new_zoom = current_zoom + (target_zoom - current_zoom) * constants.ZOOM_LERP
        self.world_camera.zoom = new_zoom

        half_w = (self.window.width / 2) / new_zoom
        half_h = (self.window.height / 2) / new_zoom

        final_x = max(half_w, min(map_width - half_w, new_x))
        final_y = max(half_h, min(map_height - half_h, new_y))

        self.world_camera.position = (final_x, final_y)

    def on_key_press(self, key, modifiers):
        self.pressed_keys.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)