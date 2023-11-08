import sys
from time import sleep
import pygame
from bullet import Bullet
from tank import Tank
from datetime import datetime


def get_number_tanks_x(ai_settings, tank_width):
    available_space_x = ai_settings.screen_width - 2 * tank_width
    number_tanks_x = int(available_space_x / (2 * tank_width))
    return number_tanks_x

def create_tank(ai_settings, screen, tanks, tank_number, row_number):
    tank = Tank(ai_settings, screen)
    tank_width = tank.rect.width
    tank.x = tank_width + 2 * tank_width * tank_number
    tank.rect.x = tank.x
    tank.rect.y = tank.rect.height + 2 * tank.rect.height * row_number
    tanks.add(tank)

def get_number_rows(ai_settings, weapon_height, tank_height):
    available_space_y = (ai_settings.screen_height - (3 * tank_height) - weapon_height)
    number_rows = int(available_space_y / (2 * tank_height))
    return number_rows

def create_fleet(ai_settings, screen, weapon, tanks):
    tank = Tank(ai_settings, screen)
    number_tanks_x = get_number_tanks_x(ai_settings, tank.rect.width)
    number_rows = get_number_rows(ai_settings, weapon.rect.height, tank.rect.height)
    for row_number in range(number_rows):
        for tank_number in range(number_tanks_x):
            create_tank(ai_settings, screen, tanks, tank_number, row_number)

def check_keydown_events(event, ai_settings, screen, weapon, bullets):
    if event.key == pygame.K_RIGHT:
        weapon.moving_right = True
    if event.key == pygame.K_LEFT:
        weapon.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, weapon, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, weapon, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, weapon)
        bullets.add(new_bullet)

def check_keyup_events(event, weapon):
    if event.key == pygame.K_RIGHT:
        weapon.moving_right = False
    if event.key == pygame.K_LEFT:
        weapon.moving_left = False

def check_play_button(ai_settings, screen, stats, sb, play_button, weapon, tanks, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_weapons()
        tanks.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, weapon, tanks)
        weapon.center_weapon()

def check_events(ai_settings, screen, stats, sb, play_button, weapon, tanks, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, weapon, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,weapon)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, weapon, tanks, bullets, mouse_x, mouse_y)

def update_screen(ai_settings, screen, stats, sb, weapon, tanks, bullets, play_button, BG):
    screen.fill(ai_settings.bg_color)
    screen.blit(BG.image, BG.rect)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    weapon.blitme()
    tanks.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def check_bullet_tank_collisions(ai_settings, screen, stats, sb, weapon, tanks, bullets):
    collisions = pygame.sprite.groupcollide(bullets, tanks, True, True)
    if collisions:
        for tanks in collisions.values():
            stats.score += ai_settings.tank_points * len(tanks)
        sb.prep_score()
        check_high_score(stats, sb)
    if len(tanks) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, weapon, tanks)

def update_bullets(ai_settings, screen, stats, sb, weapon, tanks, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_tank_collisions(ai_settings, screen, stats, sb, weapon, tanks, bullets)

def change_fleet_direction(ai_settings, tanks):
    for tank in tanks.sprites():
        tank.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings, tanks):
    for tank in tanks.sprites():
        if tank.check_edges():
            change_fleet_direction(ai_settings, tanks)
            break

def weapon_hit(ai_settings, screen, stats, sb, weapon, tanks, bullets):
    if stats.weapons_left > 0:
        stats.weapons_left -= 1
        sb.prep_weapons()
        tanks.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, weapon, tanks)
        weapon.center_weapon()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_tanks_bottom(ai_settings, screen, stats, sb, weapon, tanks, bullets):
    screen_rect = screen.get_rect()
    for tank in tanks.sprites():
        if tank.rect.bottom >= screen_rect.bottom:
            weapon_hit(ai_settings, screen, stats, sb, weapon, tanks, bullets)
            break

def update_tanks(ai_settings, screen, stats, sb, weapon, tanks, bullets):
    check_fleet_edges(ai_settings, tanks)
    tanks.update()
    if pygame.sprite.spritecollideany(weapon, tanks):
        weapon_hit(ai_settings, screen, stats, sb, weapon, tanks, bullets)
    check_tanks_bottom(ai_settings, screen, stats, sb, weapon, tanks, bullets)

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        with open("record.txt", "w") as f:
            f.write(datetime.strftime(datetime.now(), "%Y.%m.%d") + " - " + str(stats.high_score))
            f.close()
        sb.prep_high_score()
