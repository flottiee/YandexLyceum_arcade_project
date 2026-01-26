# main.py
import arcade
import constants
from entities import Car

class Level1(arcade.View):
    car: Car
    car_list: arcade.SpriteList
    map: arcade.TileMap
    walls: arcade.SpriteList
    engine: arcade.PhysicsEngineSimple
    world_camera: arcade.Camera2D
    race_track: arcade.SpriteList
    objects: arcade.SpriteList
    def __init__(self):
        super().__init__()
        
        self.pressed_keys = set()
        
        self.setup()

    def setup(self):
        self.car = Car()
        self.car_list = arcade.SpriteList()
        self.car_list.append(self.car)

        self.map = arcade.load_tilemap('tmx_files/track1.tmx', 0.5)
        
        self.race_track = self.map.sprite_lists.get('race_track', arcade.SpriteList())
        self.objects = self.map.sprite_lists.get('objects', arcade.SpriteList())
        
        self.walls = arcade.SpriteList(use_spatial_hash=True)
        if 'walls' in self.map.sprite_lists:
            self.walls.extend(self.map.sprite_lists['walls'])

        self.engine = arcade.PhysicsEngineSimple(self.car, self.walls)

        self.world_camera = arcade.Camera2D()

    def on_draw(self):
        self.clear()
        
        self.world_camera.use()
        
        self.race_track.draw()
        # self.walls.draw()
        # стены рисовать не нужно, они нужны только для коллизии
        self.objects.draw()
        self.car_list.draw()

    def on_update(self, dt):
        up = (arcade.key.UP in self.pressed_keys or arcade.key.W in self.pressed_keys)
        down = (arcade.key.DOWN in self.pressed_keys or arcade.key.S in self.pressed_keys)
        left = (arcade.key.LEFT in self.pressed_keys or arcade.key.A in self.pressed_keys)
        right = (arcade.key.RIGHT in self.pressed_keys or arcade.key.D in self.pressed_keys)

        self.car.update_input(up, down, left, right)
        
        self.car.update_car()

 
        self.engine.update()

        self.update_camera()

    def update_camera(self):
        target_x = self.car.center_x
        target_y = self.car.center_y
        
        cam_x, cam_y = self.world_camera.position
        lerp = constants.CAMERA_LERP
        new_x = cam_x + (target_x - cam_x) * lerp
        new_y = cam_y + (target_y - cam_y) * lerp
        half_w = self.window.width / 2
        half_h = self.window.height / 2
        world_w = 6400
        world_h = 3840
        
        final_x = max(half_w, min(world_w - half_w, new_x))
        final_y = max(half_h, min(world_h - half_h, new_y))

        self.world_camera.position = (final_x, final_y)

    def on_key_press(self, key, modifiers):
        self.pressed_keys.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.pressed_keys:
            self.pressed_keys.remove(key)

def main():
    window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)
    view = Level1()
    window.show_view(view)
    arcade.run()

if __name__ == "__main__":
    main()