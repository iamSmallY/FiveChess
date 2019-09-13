import pygame
from settings import Settings
from ship import Ship
import game_func as gf
from pygame.sprite import Group
from bullet import Bullet


def run_game():
    # 初始化游戏窗口设置和飞船设置
    # pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    ship = Ship(screen, ai_settings)
    bullet = Bullet(ai_settings, screen, ship)
    pygame.display.set_caption("Fire Edwin!")

    # 创建子弹的组
    bullets = Group()

    # 游戏循环主体
    while True:
        gf.check_event(ship, bullet)
        bullet.create_bullet(bullets)
        gf.update_screen(ai_settings, screen, ship, bullets)
        bullet.delete_bullet(bullets)


run_game()
