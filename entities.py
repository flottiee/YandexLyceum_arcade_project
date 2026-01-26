# entities.py
import math
import arcade
import constants

class Car(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.load_texture("images/car_black_1r.png")
        self.scale = constants.PLAYER_SCALE
        self.center_x = constants.PLAYER_START_X
        self.center_y = constants.PLAYER_START_Y

        self.input_up = False
        self.input_down = False
        self.input_left = False
        self.input_right = False

    def update_input(self, up, down, left, right):
        """Обновляет состояние кнопок"""
        self.input_up = up
        self.input_down = down
        self.input_left = left
        self.input_right = right

    def update_car(self):
        # Нужно попробовать сделать поворот более плавным, т.е не жестко 45, 90, 180 и 360 градусов,
        # а изменять угол поворота машины при нажатии на клавишу, как было в моем прошлом коде.
        # Завтра после школы попробую сделать это.
        self.change_x = 0
        self.change_y = 0

        if self.input_up:
            self.change_y = constants.PLAYER_SPEED
        elif self.input_down:
            self.change_y = -constants.PLAYER_SPEED

        if self.input_right:
            self.change_x = constants.PLAYER_SPEED
        elif self.input_left:
            self.change_x = -constants.PLAYER_SPEED

        if self.change_x != 0 or self.change_y != 0:
            rad = math.atan2(self.change_y, self.change_x)
            print(rad) 
            deg = math.degrees(rad)
            if deg == 90:
                print("вверх")
            elif deg == -90:
                print("вниз")
            elif deg == 0:
                print("вправо")
            elif deg == 180 or deg == -180:
                print("влево")
            
            self.angle = -deg 