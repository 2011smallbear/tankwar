import random  # 导入random模块
import sys

import pygame
from pygame.sprite import Sprite

__author__ = 'XSY'
dic = 'up'
bad_tank_number = 1


class Settings:
    """存储游戏所有设置的类"""

    def __init__(self):
        self.screen_width = 900
        self.screen_height = 900
        self.bg_color = (230, 230, 230)
        self.tank_speed = 1.2
        self.bullet_speed = 2.0
        self.bullet_width = 7
        self.bullet_height = 7
        self.bullet_color = (60, 60, 60)
        self.bad_tank_speed = 0.1  # 增加坏坦克的速度属性


class BadTank(Sprite):
    """管理坏坦克的类"""

    def __init__(self, game, speed):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pygame.image.load('image/turn0bad.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.speed = speed  # 使用传入的速度参数

    def update(self):
        """随机移动坏坦克"""
        move_direction = random.choice(['up', 'down', 'left', 'right'])
        random_number = random.randint(700, 800)
        for _ in range(random_number):
            # 移动和改变坦克图片
            if move_direction == 'up' and self.rect.top > 0:
                self.y -= self.speed
                self.image = pygame.image.load('image/turn0bad.png')
            elif move_direction == 'down' and self.rect.bottom < self.screen.get_rect().bottom:
                self.y += self.speed
                self.image = pygame.image.load('image/turn180bad.png')
            elif move_direction == 'left' and self.rect.left > 0:
                self.x -= self.speed
                self.image = pygame.image.load('image/turn270bad.png')
            elif move_direction == 'right' and self.rect.right < self.screen.get_rect().right:
                self.x += self.speed
                self.image = pygame.image.load('image/turn90bad.png')

        self.rect.x = self.x
        self.rect.y = self.y


class Bullet(Sprite):
    """管理子弹的类"""

    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.color = self.settings.bullet_color
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = game.good_tank.rect.midtop
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.dic = game.dic

    def update(self):
        if self.dic == 'up':
            self.y -= self.settings.bullet_speed
        elif self.dic == 'down':
            self.y += self.settings.bullet_speed
        elif self.dic == 'right':
            self.x += self.settings.bullet_speed
        elif self.dic == 'left':
            self.x -= self.settings.bullet_speed
        self.rect.y = self.y
        self.rect.x = self.x

    def draw(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)


class GoodTank:
    """管理好坦克的类"""

    def __init__(self, game, settings):
        self.screen = game.screen
        self.settings = game.settings
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load('image/turn0good.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """根据移动标志调整坦克的位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.tank_speed
            self.image = pygame.image.load('image/turn90good.png')
        elif self.moving_left and self.rect.left > 0:
            self.rect.x -= self.settings.tank_speed
            self.image = pygame.image.load('image/turn270good.png')
        elif self.moving_up and self.rect.top > 0:
            self.rect.y -= self.settings.tank_speed
            self.image = pygame.image.load('image/turn0good.png')
        elif self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += self.settings.tank_speed
            self.image = pygame.image.load('image/turn180good.png')

    def blitme(self):
        """在指定位置绘制好坦克"""
        self.screen.blit(self.image, self.rect)


class Game:
    """管理游戏资源和行为的类"""

    def __init__(self):
        pygame.init()
        self.bullets = pygame.sprite.Group()
        self.dic = dic
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.good_tank = GoodTank(self, self.settings)
        self.bullet = Bullet(self)
        self.bad_tanks = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        a = 1
        while True:
            a += 1
            self._check_events()
            self.good_tank.update()
            self._update_bullets()
            if a % 500 == 0:
                a = 0
                # 更新坏坦克的位置
                self.bad_tanks.update()
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0 or bullet.rect.right <= 0 or bullet.rect.left >= self.settings.screen_width:
                    self.bullets.remove(bullet)
            self._update_screen()

    def _update_bullets(self):
        """更新子弹的位置，并删除消失的子弹"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.right <= 0 or bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    sys.exit()
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_RIGHT:
                            self.good_tank.moving_right = True
                            self.dic = 'right'
                        case pygame.K_LEFT:
                            self.good_tank.moving_left = True
                            self.dic = 'left'
                        case pygame.K_UP:
                            self.good_tank.moving_up = True
                            self.dic = 'up'
                        case pygame.K_DOWN:
                            self.good_tank.moving_down = True
                            self.dic = 'down'
                        case pygame.K_SPACE:
                            self._fire_bullet()
                case pygame.KEYUP:
                    match event.key:
                        case pygame.K_RIGHT:
                            self.good_tank.moving_right = False
                        case pygame.K_LEFT:
                            self.good_tank.moving_left = False
                        case pygame.K_UP:
                            self.good_tank.moving_up = False
                        case pygame.K_DOWN:
                            self.good_tank.moving_down = False

    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _create_fleet(self):
        """创建坏坦克群"""
        for _ in range(bad_tank_number):
            bad_tank = BadTank(self, self.settings.bad_tank_speed)  # 使用Settings类中的坏坦克速度属性
            self.bad_tanks.add(bad_tank)

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.good_tank.blitme()  # 在屏幕上绘制好坦克
        for bullet in self.bullets.sprites():
            bullet.draw()
        self.bad_tanks.draw(self.screen)
        pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run_game()
