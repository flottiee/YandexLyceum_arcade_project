# # entities.py
import math
import arcade
import constants


class Car(arcade.Sprite):
    def __init__(self, track):
        super().__init__()
        self.initial_texture = arcade.load_texture("images/black_car/car_black_1.png")
        self.texture = self.initial_texture
        self.scale = constants.PLAYER_SCALE

        if track == 1:
            self.center_x = constants.PLAYER_START_X_TRACK_1
            self.center_y = constants.PLAYER_START_Y_TRACK_1
            self.angle = 90
        elif track == 2:
            self.center_x = constants.PLAYER_START_X_TRACK_2
            self.center_y = constants.PLAYER_START_Y_TRACK_2
            self.angle = 270

        self.is_slides_on_oil = False
        self.timer_after_slide = 0
        self.timer_slide = 0
        self.texture_change_time = 0

        self.acceleration = 0.5
        self.speed = 0
        self.brake_deceleration = 0.8
        self.natural_deceleration = 0.2
        self.max_forward_speed = constants.PLAYER_SPEED
        self.max_reverse_speed = -constants.PLAYER_SPEED * 0.5

        self.turn_speed = 10
        self.steering_direction = 0

        self.input_up = False
        self.input_down = False
        self.input_left = False
        self.input_right = False

    def start_slide(self):
        self.is_slides_on_oil = True
        self.timer_after_slide = 2
        self.timer_slide = 0


    def update_input(self, up, down, left, right):
        """Обновляет состояние кнопок"""
        self.input_up = up
        self.input_down = down
        self.input_left = left
        self.input_right = right

    def update_car(self, dt):
        if not self.is_slides_on_oil and self.timer_after_slide <= 0:
            self.steering_direction = 0
            if self.input_right:
                self.steering_direction = 1
            elif self.input_left:
                self.steering_direction = -1

            if abs(self.speed) > 0.1:
                turn_multiplier = 1.0 - min(abs(self.speed) / self.max_forward_speed, 0.7)
                self.angle += self.steering_direction * self.turn_speed * turn_multiplier

            if self.input_up:
                self.speed += self.acceleration
                if self.speed > self.max_forward_speed:
                    self.speed = self.max_forward_speed
            elif self.input_down:
                if self.speed > 0:
                    self.speed -= self.brake_deceleration
                    if self.speed < 0:
                        self.speed = 0
                else:
                    self.speed -= self.acceleration * 0.7
                    if self.speed < self.max_reverse_speed:
                        self.speed = self.max_reverse_speed
            else:
                if self.speed > 0:
                    self.speed -= self.natural_deceleration
                    if self.speed < 0:
                        self.speed = 0
                elif self.speed < 0:
                    self.speed += self.natural_deceleration
                    if self.speed > 0:
                        self.speed = 0

            angle_rad = math.radians(self.angle)
            self.change_x = self.speed * math.sin(angle_rad)
            self.change_y = self.speed * math.cos(angle_rad)

        else:
            if self.is_slides_on_oil:
                self.timer_slide += dt
                if self.timer_slide >= 2:
                    self.is_slides_on_oil = False
                    self.timer_slide = 0

            if self.timer_after_slide > 0:
                self.timer_after_slide -= dt

            self.speed = 3 * dt

            self.center_x += self.speed
            self.center_y += self.speed

    def update_animation_car(self, dt):
        if self.is_slides_on_oil:
            self.texture_change_time += dt
            if self.texture_change_time >= constants.TEXTURE_CHANGE_DELAY:
                self.texture_change_time = 0
                self.angle = (self.angle + 45) % 360