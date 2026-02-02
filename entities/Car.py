# # entities.py
import math
import random

import arcade
import constants


class Car(arcade.Sprite):
    def __init__(self, track, player_id=1): # Изменено: добавлен player_id
        super().__init__()
        # Выбор текстуры в зависимости от игрока
        texture_path = "assets/images/car_black_1.png" if player_id == 1 else "assets/images/car_red_1.png"
        self.texture = arcade.load_texture(texture_path)
        self.scale = constants.PLAYER_SCALE
        self.player_id = player_id

        if track == 1:
            self.center_x = constants.PLAYER_START_X_TRACK_1
            self.center_y = constants.PLAYER_START_Y_TRACK_1
        elif track == 2:
            self.center_x = constants.PLAYER_START_X_TRACK_2
            self.center_y = constants.PLAYER_START_Y_TRACK_2
        elif track == 3:
            self.center_x = constants.PLAYER_START_X_TRACK_3
            self.center_y = constants.PLAYER_START_Y_TRACK_3

        self.angle = 90

        self.is_oversteering = False  # Флаг эффекта масла
        self.oversteer_timer = 0.0    # Таймер эффекта масла
        self.acceleration = 0.2
        self.speed = 0
        self.brake_deceleration = 0.8
        self.natural_deceleration = 0.2
        self.max_forward_speed = constants.PLAYER_SPEED
        self.max_reverse_speed = -constants.PLAYER_SPEED * 0.5

        self.turn_speed = 10
        self.steering_direction = 0

        self.is_slides_on_oil = False
        self.timer_after_slide = 0
        self.timer_slide = 0
        self.texture_change_time = 0

        self.input_up = False
        self.input_down = False
        self.input_left = False
        self.input_right = False

        self.slide_particles = []
        self.slide_particle_count = 0
        self.max_slide_particles = 100
        self.slide_particle_spawn_timer = 0
        self.slide_particle_spawn_rate = 0.05

        self.exhaust_particles = []
        self.exhaust_particles_count = 0
        self.exhaust_particles_spawn_timer = 0
        self.exhaust_particles_spawn_rate = 0.01

    def start_slide(self):
        self.is_slides_on_oil = True
        self.timer_after_slide = 2
        self.timer_slide = 0
        for _ in range(10):
            self.spawn_slide_particle()

    def spawn_shooting_particles(self):
        """Отстрелы от выхлопа"""
        angle_rad = math.radians(self.angle + 180)
        offset_x = 15 * math.sin(angle_rad)
        offset_y = 15 * math.cos(angle_rad)

    def spawn_exhaust_particles(self):
        """Выхлопные газы сзади машины"""
        angle_rad = math.radians(self.angle + 180)
        offset_x = 15 * math.sin(angle_rad)
        offset_y = 15 * math.cos(angle_rad)

        particle = {
            'x': self.center_x - offset_x,
            'y': self.center_y - offset_y,
            'dx': -math.sin(angle_rad) * 2,
            'dy': -math.cos(angle_rad) * 2,
            'life': 1,
            'max_life': 1.5,
            'color': arcade.color.DARK_GRAY,
            'size': random.uniform(2, 5)
        }
        self.exhaust_particles.append(particle)
        self.exhaust_particles_count += 1

    def spawn_slide_particle(self):
        """Создает одну частицу скольжения"""
        if len(self.slide_particles) >= self.max_slide_particles:
            return

        angle_offset = random.uniform(0, 2 * math.pi)
        distance = random.uniform(10, 25)

        particle_x = self.center_x + math.cos(angle_offset) * distance
        particle_y = self.center_y + math.sin(angle_offset) * distance

        car_angle_rad = math.radians(self.angle)
        spread_angle = car_angle_rad + random.uniform(-math.pi / 4, math.pi / 4)

        speed = random.uniform(0.5, 2.0)

        particle = {
            'x': particle_x,
            'y': particle_y,
            'dx': math.cos(spread_angle) * speed,
            'dy': math.sin(spread_angle) * speed,
            'life': random.uniform(0.5, 1.5),
            'max_life': 1.5,
            'size': random.uniform(5, 9),
            'color': random.choice([
                (200, 180, 160),
                (180, 160, 140),
                (160, 140, 120),
                (220, 200, 180)]),
            'rotation': random.uniform(0, 360),
            'rotation_speed': random.uniform(-5, 5)
        }

        self.slide_particles.append(particle)
        self.slide_particle_count += 1

    def update_slide_particles(self, dt):
        """Обновляет частицы скольжения"""
        particles_to_remove = []

        for i, particle in enumerate(self.slide_particles):
            particle['life'] -= dt

            if particle['life'] <= 0:
                particles_to_remove.append(i)
                continue

            particle['x'] += particle['dx']
            particle['y'] += particle['dy']

            particle['dx'] *= 0.98
            particle['dy'] *= 0.98

            particle['rotation'] += particle['rotation_speed']

            particle['size'] *= 0.99

        for i in reversed(particles_to_remove):
            self.slide_particles.pop(i)
            self.slide_particle_count -= 1

    def update_exhaust_particles(self, dt):
        particles_to_remove = []
        for i, particle in enumerate(self.exhaust_particles):
            particle['life'] -= dt
            if particle['life'] <= 0:
                particles_to_remove.append(i)
                continue

            particle['x'] += particle['dx']
            particle['y'] += particle['dy']

            particle['size'] *= 0.99

        for i in reversed(particles_to_remove):
            self.exhaust_particles.pop(i)
            self.exhaust_particles_count -= 1

    def draw_particles(self):
        """Отрисовывает частицы скольжения"""
        for particle in self.slide_particles:
            alpha = int(255 * (particle['life'] / particle['max_life']))

            color_with_alpha = (
                particle['color'][0],
                particle['color'][1],
                particle['color'][2],
                alpha
            )

            arcade.draw_rect_filled(arcade.rect.XYWH(
                particle['x'], particle['y'],
                particle['size'], particle['size']),
                color_with_alpha,
                particle['rotation']
            )
        for particle in self.exhaust_particles:
            alpha = int(255 * (particle['life'] / particle['max_life']))

            color_with_alpha = (
                particle['color'][0],
                particle['color'][1],
                particle['color'][2],
                alpha
            )

            arcade.draw_circle_filled(
                particle['x'], particle['y'],
                particle['size'],
                color_with_alpha
            )


    def update_input(self, up, down, left, right):
        """Обновляет состояние кнопок"""
        self.input_up = up
        self.input_down = down
        self.input_left = left
        self.input_right = right

    def update_car(self, dt):
        # 1. ЛОГИКА МАСЛА (ТЗ: Таймер и флаг)
        if self.timer_slide > 0:
            self.timer_slide -= dt
            self.is_slides_on_oil = True
        else:
            self.is_slides_on_oil = False

        # 2. ОГРАНИЧЕНИЕ ПОВОРОТА (ТЗ: Зависимость от скорости)
        # Рассчитываем множитель от 0.0 до 1.0
        speed_ratio = abs(self.speed) / self.max_forward_speed
        
        if speed_ratio < 0.1:
            # Слишком медленно или стоим — не поворачиваем вообще
            turn_mod = 0.0
        elif speed_ratio < 0.5:
            # Набираем маневренность (от 0.1 до 0.5 скорости)
            turn_mod = speed_ratio * 2.0
        else:
            # После 50% скорости руль становится "тяжелым"
            turn_mod = max(0.4, 1.3 - speed_ratio)

        # 3. РАСЧЕТ СИЛЫ ПОВОРОТА
        # Определяем базовое направление: влево (+1), вправо (-1)
        direction = 0
        if self.input_left:
            direction = 1
        elif self.input_right:
            direction = -1

        # Множитель масла (только если нажат поворот!)
        oil_boost = 3.0 if self.is_slides_on_oil else 1.0
        
        # Итоговое количество градусов, на которое повернем
        turn_amount = direction * self.turn_speed * turn_mod * oil_boost

        # ПРИМЕНЕНИЕ ПОВОРОТА
        # ВНИМАНИЕ: Если руль инвертирован, просто смени += на -= здесь и ВСЁ.
        self.angle -= turn_amount 

        # 4. ФИЗИКА ГАЗА И ТОРМОЗА (Очищенная от старых else)
        if self.input_up:
            self.speed += self.acceleration
            if self.speed > self.max_forward_speed:
                self.speed = self.max_forward_speed
        elif self.input_down:
            self.speed -= self.brake_deceleration
            if self.speed < self.max_reverse_speed:
                self.speed = self.max_reverse_speed
        else:
            # Трение (естественная остановка)
            if self.speed > 0:
                self.speed = max(0, self.speed - self.natural_deceleration)
            elif self.speed < 0:
                self.speed = min(0, self.speed + self.natural_deceleration)

        # 5. ОБНОВЛЕНИЕ ВЕКТОРОВ (Твои рабочие sin/cos)
        angle_rad = math.radians(self.angle)
        self.change_x = self.speed * math.sin(angle_rad)
        self.change_y = self.speed * math.cos(angle_rad)

        # Частицы и визуализация
        self.update_exhaust_particles(dt)
        if self.is_slides_on_oil:
            self.spawn_slide_particle()
        self.update_slide_particles(dt)

    def hit_oil(self):
        """Реализация ТЗ: включаем оверстиринг на 1.5 секунды"""
        self.timer_slide = 1.5 
        # self.is_slides_on_oil станет True автоматически в update_car, пока тикает таймер
    
    def on_wall_hit(self):
        """Реализация ТЗ: Гашение скорости при ударе об стену"""
        self.speed *= 0.5  # Коэффициент можно настроить (0.5 = потеря половины скорости)

    