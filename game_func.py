import pygame
import sys


def check_event(ship, bullet):
    # 判断是哪个键被按下
    def check_keydown_events(this_event, this_ship, this_bullet):
        if this_event.key == pygame.K_RIGHT:
            this_ship.moving_right = True
        elif this_event.key == pygame.K_LEFT:
            this_ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            this_bullet.fire = True
        elif this_event.key == pygame.K_q:
            sys.exit()

    # 判断是哪个键被抬起
    def check_keyup_events(this_event, this_ship, this_bullet):
        if this_event.key == pygame.K_RIGHT:
            this_ship.moving_right = False
        elif this_event.key == pygame.K_LEFT:
            this_ship.moving_left = False
        elif event.key == pygame.K_SPACE:
            this_bullet.fire = False

    # 读取键鼠输入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, bullet)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship, bullet)


def update_screen(ai_settings, screen, ship, bullets):
    # 填入背景
    screen.fill(ai_settings.bg_color)

    # 放入飞船
    ship.blitme()

    # 更新飞船位置
    ship.move()

    # 显示子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 显示窗口
    pygame.display.flip()


