import pygame
from pygame.sprite import Group
from settings import Settings
from settings import Background
from game_stats import GameStats
from button import Button
from weapon import Weapon
import game_functions as gf
from scoreboard import Scoreboard


def run_game():
    pygame.init()
    ai_settings = Settings()

    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    weapon = Weapon(ai_settings, screen)
    BG = Background("images/fon.png", [0, 0])
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, weapon, aliens)

    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, weapon, aliens, bullets)
        if stats.game_active:
            weapon.update()
            gf.update_bullets(ai_settings, screen, stats, sb, weapon, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, weapon, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, weapon, aliens, bullets, play_button, BG)

run_game()
