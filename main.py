import random
import sys

import pygame
from pygame.sprite import Sprite

__author__ = 'XSY'
dic = 'up'


class Settings:
    """存储游戏所有设置的类"""

    def __init__(self):
        self.screen_width = 900
        self.screen_height = 900
        self.bg_color = (255, 255, 255)
        self.tank_speed = 1.2
        self.bad_tank_speed = self.tank_speed / 2
        self.bullet_speed = 2.0
        self.bullet_width = 7
        self.bullet_height = 7
        self.bullet_color = (60, 60, 60)
        self.default_direction = 'up'
        self.bad_tank_num = 3
        self.ship_left = 3


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
        # 方向标识
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


class BadTank(Sprite):
    """管理坏坦克的类"""

    def __init__(self, game):
        super(BadTank, self).__init__()
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load('image/turn0bad.png')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.settings = game.settings
        self.tank_speed = self.settings.bad_tank_speed  # 修改
        self.dic = self.settings.default_direction  # 修改
        self.last_move_time = 0

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def random_move(self):
        directions = ['up', 'down', 'left', 'right']
        self.dic = random.choice(directions)

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > 1000:  # 检查当前时间与last_move_time的差值是否大于1000毫秒
            if self.dic == 'up':
                if self.rect.top > 0:  # 检查是否超出上边界
                    self.y -= self.tank_speed * 100
                    self.image = pygame.image.load('image\\turn0bad.png')
                else:
                    self.random_move()  # 碰到边缘时随机改变方向
            elif self.dic == 'down':
                if self.rect.bottom < self.screen_rect.bottom:  # 检查是否超出下边界
                    self.y += self.tank_speed * 100
                    self.image = pygame.image.load('image\\turn180bad.png')
                else:
                    self.random_move()
            elif self.dic == 'right':
                if self.rect.right < self.screen_rect.right:  # 检查是否超出右边界
                    self.x += self.tank_speed * 100
                    self.image = pygame.image.load('image\\turn90bad.png')
                else:
                    self.random_move()
            elif self.dic == 'left':
                if self.rect.left > 0:  # 检查是否超出左边界
                    self.x -= self.tank_speed * 100
                    self.image = pygame.image.load('image\\turn270bad.png')
                else:
                    self.random_move()

            self.rect.y = self.y
            self.rect.x = self.x
            self.last_move_time = current_time


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
        # 移动标志
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
        self.settings = Settings()
        self.dic = self.settings.default_direction  # 修改
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.good_tank = GoodTank(self, self.settings)
        self.bad_tanks = pygame.sprite.Group()
        self.bullet = Bullet(self)
        self._create_fleet()

    def run_game(self):
        while True:
            self._check_collision()
            self._check_events()
            self.good_tank.update()
            self._update_bullets()
            self._update_bad_tanks()
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0 or bullet.rect.right <= 0 or bullet.rect.left >= self.settings.screen_width:
                    self.bullets.remove(bullet)
            self._update_screen()

    def _check_collision(self):
        """检查好坦克与坏坦克的碰撞"""
        if pygame.sprite.spritecollideany(self.good_tank, self.bad_tanks):
            self.settings.ship_left -= 1
            if self.settings.ship_left == 0:
                self._game_over()

    def _game_over(self):
        """游戏结束"""
        pygame.quit()
        sys.exit()
    def _update_bad_tanks(self):
        """更新坏坦克的位置"""
        for bad_tank in self.bad_tanks.sprites():
            bad_tank.random_move()
            bad_tank.update()

    def _create_fleet(self):
        for i in range(self.settings.bad_tank_num):
            bad_tank = BadTank(self)
            self.bad_tanks.add(bad_tank)

    def _update_bullets(self):
        """更新子弹的位置，并删除消失的子弹"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.right <= 0 or bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(self.bullets, self.bad_tanks, True, True)

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
