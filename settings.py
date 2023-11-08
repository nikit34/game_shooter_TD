from pygame.sprite import Sprite
from pygame.image import load


class Settings():
    def __init__(self):
        self.screen_width = 1300
        self.screen_height = 700
        self.bg_color = (230, 230, 230)
        self.weapon_limit = 3
        self.bullet_width = 5
        self.bullet_height = 20
        self.bullet_color = 255, 0, 0
        self.bullets_allowed = 3
        self.fleet_drop_speed = 20
        self.speedup_scale = 1.3
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.weapon_speed_factor = 10
        self.bullet_speed_factor = 15
        self.tank_speed_factor = 5
        self.fleet_direction = 1  # -1 -move left    1 -move right
        self.tank_points = 50

    def increase_speed(self):
        self.weapon_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.tank_speed_factor *= self.speedup_scale
        self.tank_points = int(self.tank_points * self.score_scale)


class Background(Sprite):
    def __init__(self, image_file, location):
        Sprite.__init__(self)
        self.image = load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
