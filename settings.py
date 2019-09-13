# 设置类,用于游戏的基本设置
class Settings(object):
    # 初始化Settings类
    def __init__(self):
        # 屏幕部分
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (230, 230, 230)

        # 飞船部分
        self.ship_speed = 1

        # 子弹部分
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (230, 0, 0)
        self.bullet_speed = 1
        self.bullets_max_existence_number = 10
