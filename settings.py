from pygame.sprite import Sprite
from pygame.image import load


class Settings():
    def __init__(self):
        self.screen_width = 1300
        self.screen_height = 700
        self.bg_color = (230, 230, 230)
        self.ship_limit = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        self.fleet_drop_speed = 20
        self.speedup_scale = 1.3
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 10
        self.bullet_speed_factor = 15
        self.alien_speed_factor = 5
        self.fleet_direction = 1  # -1 -move left    1 -move right
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)


class Background(Sprite):
    def __init__(self, image_file, location):
        Sprite.__init__(self)
        self.image = load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
