import pygame
import sys


def check_event(ship):
    # 判断是哪个键被按下并开始移动
    def check_keydown_events(this_event, this_ship):
        if this_event.key == pygame.K_RIGHT:
            this_ship.moving_right = True
        elif this_event.key == pygame.K_LEFT:
            this_ship.moving_left = True

    # 判断是哪个键被抬起并停止移动
    def check_keyup_events(this_event, this_ship):
        if this_event.key == pygame.K_RIGHT:
            this_ship.moving_right = False
        elif this_event.key == pygame.K_LEFT:
            this_ship.moving_left = False

    # 读取键鼠输入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def update_screen(ai_settings, screen, ship):
    # 填入背景
    screen.fill(ai_settings.bg_color)
    # 放入飞船
    ship.blitme()
    # 显示窗口
    pygame.display.flip()
