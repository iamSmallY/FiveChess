import pygame
from settings import Settings
from ship import Ship
import game_func as gf


def run_game():
    # 初始化游戏窗口设置和飞船设置
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    ship = Ship(screen, ai_settings)
    pygame.display.set_caption("Alien Invasion")

    # 游戏循环主体
    while True:
        gf.check_event(ship)
        ship.move()
        gf.update_screen(ai_settings, screen, ship)


run_game()
