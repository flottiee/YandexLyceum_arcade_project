import math

import arcade

CAMERA_LERP = 0.12

class Car(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("images/car_black_1r.png")
        self.angle = 0
        self.center_x = 1056
        self.center_y = 80
        self.scale = 0.5

        self.vel_x = 0
        self.vel_y = 0

        self.max_f_speed = 8
        self.max_r_speed = 3
        self.friction = 0.96
        self.drift = 0.95
        self.engine_power = 0.3
        self.brake_power = 0.5
        self.turn_speed = 4.0

        self.brake = False
        self.forward = False
        self.steer = False

    def control(self, forward, brake, steer):
        self.forward = True if forward else False
        self.brake = brake if brake else False
        self.steer = -1 if steer == "left" else (1 if steer == "right" else 0)

    def update_car(self):
        if self.forward:
            self.vel_x += math.cos(math.radians(self.angle)) * self.engine_power
            self.vel_y += math.sin(math.radians(self.angle)) * self.engine_power
        if self.brake:
            self.vel_x *= self.brake_power
            self.vel_y *= self.brake_power
        if self.steer != 0:
            current_speed = math.sqrt(self.vel_x ** 2 + self.vel_y ** 2)
            turn_effectiveness = 1.0 / (1.0 + current_speed * 0.1)
            self.angle += self.steer * self.turn_speed * turn_effectiveness

        self.vel_x *= self.drift
        self.vel_y *= self.drift

        self.vel_x *= self.friction
        self.vel_y *= self.friction

        current_speed = math.sqrt(self.vel_x ** 2 + self.vel_y ** 2)
        if current_speed > 0:
            if self.vel_x > 0 and self.vel_y > 0:
                max_speed = self.max_f_speed
            else:
                max_speed = self.max_r_speed

            if current_speed > max_speed:
                scale = max_speed / current_speed
                self.vel_x *= scale
                self.vel_y *= scale

        self.change_x = self.vel_x
        self.change_y = self.vel_y


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
        self.car.update_car()

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