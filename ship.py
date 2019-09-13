import pygame


class Ship(object):
    # 初始化Ship类
    def __init__(self, screen, ai_settings):
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载图像
        self.image = pygame.image.load('image/spacecraft.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 设置飞船位置于屏幕底部
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 初始化移动属性
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        # 放置飞船
        self.screen.blit(self.image, self.rect)

    # 移动部分
    def move(self):
        if self.moving_right and self.rect.right < self.ai_settings.screen_width:
            self.rect.centerx += self.ai_settings.ship_speed
        elif self.moving_left and self.rect.left > 0:
            self.rect.centerx -= self.ai_settings.ship_speed
