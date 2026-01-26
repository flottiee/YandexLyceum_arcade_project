import math

import arcade

CAMERA_LERP = 0.12

class Car(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("images/car_black_1r.png")
        self.scale = 0.5
        self.center_x = 1056
        self.center_y = 80

        self.speed = 5  # Константная скорость движения

    def control(self, forward, brake, steer):
        # В этой упрощенной модели мы игнорируем эти параметры
        # и будем считывать нажатия напрямую в update или через Level1
        pass

    def update_with_keys(self, keys):
        """
        Метод для прямого управления.
        Принимает set() нажатых клавиш из Level1.
        """
        self.change_x = 0
        self.change_y = 0

        # Логика движения по осям
        if arcade.key.UP in keys or arcade.key.W in keys:
            self.change_y = self.speed
            self.angle = 0  # Смотрит вверх
        elif arcade.key.DOWN in keys or arcade.key.S in keys:
            self.change_y = -self.speed
            self.angle = 180 # Смотрит вниз
        elif arcade.key.LEFT in keys or arcade.key.A in keys:
            self.change_x = -self.speed
            self.angle = 90  # Смотрит влево
        elif arcade.key.RIGHT in keys or arcade.key.D in keys:
            self.change_x = self.speed
            self.angle = -90 # Смотрит вправо (или 270)


class Level1(arcade.View):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.car = Car()
        self.car_list = arcade.SpriteList()
        self.car_list.append(self.car)
        self.map = arcade.load_tilemap('tmx_files/track1.tmx', 0.5)
        self.objects = self.map.sprite_lists['objects']
        self.race_track = self.map.sprite_lists['race_track']
        self.walls = arcade.SpriteList(use_spatial_hash=True)
        self.walls.extend(self.map.sprite_lists['walls'])

        self.engine = arcade.PhysicsEngineSimple(self.car, self.walls)
        self.world_camera = arcade.Camera2D()

        self.keys_pressed = set()

    def on_draw(self):
        self.clear()

        self.world_camera.use()
        self.race_track.draw()
        self.objects.draw()
        self.car_list.draw()

    def on_update(self, dt):
        forward = (arcade.key.UP in self.keys_pressed or arcade.key.W in self.keys_pressed)
        brake = (arcade.key.DOWN in self.keys_pressed or arcade.key.S in self.keys_pressed)
        steer = None

        if arcade.key.LEFT in self.keys_pressed or arcade.key.A in self.keys_pressed:
            steer = "left"
        elif arcade.key.RIGHT in self.keys_pressed or arcade.key.D in self.keys_pressed:
            steer = "right"

        self.car.control(forward, brake, steer)
        self.car.update_with_keys(self.keys_pressed)

        self.engine.update()
        target = (self.car.center_x, self.car.center_y)
        cx, cy = self.world_camera.position
        smooth = (cx + (target[0] - cx) * CAMERA_LERP,
                  cy + (target[1] - cy) * CAMERA_LERP)

        half_w = self.world_camera.viewport_width / 2
        half_h = self.world_camera.viewport_height / 2

        world_w = 6400
        world_h = 3840
        cam_x = max(half_w, min(world_w - half_w, smooth[0]))
        cam_y = max(half_h, min(world_h - half_h, smooth[1]))

        self.world_camera.position = (cam_x, cam_y)


    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        print(x, y)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)



def main():
    window = arcade.Window(
        title="гонки"
    )

    start_view = Level1()
    window.show_view(start_view)

    arcade.run()


if __name__ == "__main__":
    main()