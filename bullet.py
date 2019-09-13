import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    # 关于子弹的类
    def __init__(self, ai_settings, screen, ship):
        # 初始化
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.ship = ship

        # 创建一个子弹,并将其移动到正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings. bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 保存子弹移动时的位置
        self.y = float(self.rect.y)

        # 设置子弹的颜色和速度
        self.color = ai_settings.bullet_color
        self.speed = ai_settings.bullet_speed

        # 初始化发射参数
        self.fire = False

    def update(self):
        # 根据速度改变子弹位置
        self.y -= self.speed

        # 改变子弹图像出现的位置
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)

    def create_bullet(self, bullets):
        if self.fire and len(bullets) < self.ai_settings.bullets_max_existence_number:
            new_bullet = Bullet(self.ai_settings, self.screen, self.ship)
            bullets.append(new_bullet)

    @staticmethod
    def delete_bullet(bullets):
        #  删除超出边界的子弹
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)
