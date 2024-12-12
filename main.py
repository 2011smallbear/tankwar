import random
import sys
import time

import pygame
import pygame.font
from pygame.sprite import Sprite

__author__ = 'XSY'
dic = 'up'


class Settings:
    """存储游戏所有设置的类"""

    def __init__(self):
        self.screen_width = 900
        self.screen_height = 900
        self.bg_color = (0, 0, 0)
        self.tank_speed = 1.2
        self.bad_tank_speed = self.tank_speed / 2
        self.bullet_speed = 2.0
        self.bullet_width = 7
        self.bullet_height = 7
        self.bullet_color = (128, 128, 128)
        self.text_color = (255, 255, 255)
        self.default_direction = 'up'
        self.bad_tank_num = 6
        self.ship_left = 3
        self.bad_tank1_blood = 7
        self.bad_tank2_blood = 5
        self.every_shoot_score_1 = 10
        self.every_shoot_score_2 = 20
        self.yellow_shoot_damage = 1
        self.red_shoot_damage = 2
        self.blood_color = (128, 0, 128)
        self.blood_image = pygame.image.load('image/blood.png')
        self.bullet_image = pygame.image.load('image/bullet1.png')
        self.blast = pygame.mixer.Sound('music/爆炸.mp3')
        self.shoot = pygame.mixer.Sound('music/射击.mp3')
        self.strike = pygame.mixer.Sound('music/撞击.mp3')


class BloodDisplay:
    def __init__(self, game):
        self.screen = game.screen
        self.settings = game.settings
        self.blood_image = self.settings.blood_image
        self.blood_rect = self.blood_image.get_rect()
        self.blood_rect.topleft = (10, 10)  # 设置血量显示的位置

    def draw(self):
        """绘制剩余的血量"""
        for i in range(self.settings.ship_left):
            blood_position = self.blood_rect.topleft
            blood_position = (blood_position[0] + i * (self.blood_rect.width + 5), blood_position[1])
            self.screen.blit(self.blood_image, blood_position)


class ScoreBoard:
    def __init__(self, game):
        self.settings = game.settings
        self.screen = game.screen
        self.sreen_rect = self.screen.get_rect()
        self.text_color = self.settings.text_color
        self.score = 0
        self.font = pygame.font.SysFont(None, 48)
        self.prep_score()

    def prep_score(self):
        self.score_str = str(self.score)
        self.score_image = self.font.render(self.score_str, True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.sreen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)


class Explosion(Sprite):
    """管理爆炸效果的类"""

    def __init__(self, game, center):
        super().__init__()
        self.screen = game.screen
        self.explosion_images = [pygame.image.load(f'image/{i}.gif') for i in range(11)]
        self.rect = self.explosion_images[0].get_rect()
        self.rect.center = center
        self.frame = 0
        self.time_created = pygame.time.get_ticks()
        self.image = self.explosion_images[0]
        self.alpha = 255  # 初始透明度

    def update(self):
        """更新爆炸效果"""
        current_time = pygame.time.get_ticks()
        if current_time - self.time_created > 50:
            self.time_created = current_time
            self.frame += 1
            if self.frame == len(self.explosion_images):
                self.kill()
            else:
                self.image = self.explosion_images[self.frame]
                self.alpha -= 25  # 每次更新减少透明度
                if self.alpha < 0:
                    self.alpha = 0
                self.image.set_alpha(self.alpha)  # 设置图像透明度

    def draw(self):
        """在屏幕上绘制爆炸效果"""
        self.screen.blit(self.image, self.rect)


class Bullet1(Sprite):
    """管理子弹的类"""

    def __init__(self, game):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pygame.image.load('image/bullet1.png')  # 加载子弹图片
        self.rect = self.image.get_rect()  # 初始化rect属性
        self.color = 'yellow'
        self.rect.midtop = game.good_tank.rect.midtop  # 设置子弹初始位置
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
        self.screen.blit(self.image, self.rect)  # 使用图像绘制子弹


class Bullet2(Bullet1):
    """管理子弹的类"""

    def __init__(self, game):
        super(Bullet2, self).__init__(game)
        self.image = pygame.image.load('image/bullet2.png')  # 修改图像属性
        self.rect = self.image.get_rect()
        self.color = 'red'


class BadTank1(Sprite):
    """管理坏坦克的类"""

    def __init__(self, game):
        super(BadTank1, self).__init__()
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load('image/turn0bad.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, self.screen_rect.width - self.rect.width)
        self.rect.y = random.randint(0, self.screen_rect.height - self.rect.height)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.settings = game.settings
        self.tank_speed = self.settings.bad_tank_speed
        self.dic = self.settings.default_direction
        self.last_move_time = 0
        self.blood = self.settings.bad_tank1_blood

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        # 绘制血条
        blood_bar_width = (self.blood / self.settings.bad_tank1_blood) * self.rect.width
        pygame.draw.rect(self.screen, self.settings.blood_color, (self.rect.x, self.rect.y, blood_bar_width, 5))

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


class BadTank2(BadTank1):
    """管理第二种坏坦克的类"""

    def __init__(self, game):
        super(BadTank2, self).__init__(game)
        self.image = pygame.image.load('image/tankU.gif')
        self.blood = self.settings.bad_tank2_blood  # 添加血量属性

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > 1000:  # 检查当前时间与last_move_time的差值是否大于1000毫秒
            if self.dic == 'up':
                if self.rect.top > 0:  # 检查是否超出上边界
                    self.y -= self.tank_speed * 100
                    self.image = pygame.image.load('image\\tankU.gif')
                else:
                    self.random_move()  # 碰到边缘时随机改变方向
            elif self.dic == 'down':
                if self.rect.bottom < self.screen_rect.bottom:  # 检查是否超出下边界
                    self.y += self.tank_speed * 100
                    self.image = pygame.image.load('image\\tankD.gif')
                else:
                    self.random_move()
            elif self.dic == 'right':
                if self.rect.right < self.screen_rect.right:  # 检查是否超出右边界
                    self.x += self.tank_speed * 100
                    self.image = pygame.image.load('image\\tankR.gif')
                else:
                    self.random_move()
            elif self.dic == 'left':
                if self.rect.left > 0:  # 检查是否超出左边界
                    self.x -= self.tank_speed * 100
                    self.image = pygame.image.load('image\\tankL.gif')
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
        self.rect.center = self.screen_rect.center

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

    def center_tank(self):
        """将坦克居中"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)


class Game:
    """管理游戏资源和行为的类"""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('坦克大战')
        pygame.mixer.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.sb = ScoreBoard(self)
        self.dic = self.settings.default_direction
        self.good_tank = GoodTank(self, self.settings)
        self.bad_tanks = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.blood_display = BloodDisplay(self)
        self._create_fleet()

    def run_game(self):

        self._exercise()

    def _exercise(self):
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
            self._ship_hit()
            if self.settings.ship_left == 0:
                self._one_game_over()

    def _ship_hit(self):
        """响应好坦克被撞到"""
        self.settings.ship_left -= 1
        self.bad_tanks.empty()
        self.bullets.empty()
        self._create_fleet()
        self.good_tank.center_tank()
        self.blood_display.draw()
        time.sleep(0.5)

    def _one_game_over(self):
        """ 单次游戏结束"""
        pygame.quit()
        sys.exit()

    def _update_bad_tanks(self):
        """更新坏坦克的位置"""
        for bad_tank in self.bad_tanks.sprites():
            if isinstance(bad_tank, BadTank1):
                bad_tank.random_move()
            bad_tank.update()

    def _create_fleet(self):
        for i in range(self.settings.bad_tank_num):
            result = random.choice(['bad1', 'bad2', 'bad2'])
            if result == 'bad1':
                bad_tank = BadTank1(self)
                self.bad_tanks.add(bad_tank)
            elif result == 'bad2':
                bad_tank = BadTank2(self)
                self.bad_tanks.add(bad_tank)

    def _update_bullets(self):
        """更新子弹的位置，并删除消失的子弹"""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0 or bullet.rect.right <= 0 or bullet.rect.left >= self.settings.screen_width:
                self.bullets.remove(bullet)
        self._check_bullet_bad_tanks_collision()

    def _check_bullet_bad_tanks_collision(self):
        """检查子弹与坏坦克的碰撞"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.bad_tanks, True, False)  # 修改为False，不删除坏坦克
        if collisions:
            self.settings.strike.play()
            self.sb.prep_score()
            for bad_tank_list in collisions.values():
                for tank in bad_tank_list:
                    if isinstance(tank, (BadTank1, BadTank2)):
                        if isinstance(tank, BadTank1):
                            tank.blood -= self.settings.yellow_shoot_damage
                            self.sb.score += self.settings.every_shoot_score_1
                        elif isinstance(tank, BadTank2):
                            tank.blood -= self.settings.self.red_shoot_damage
                            self.sb.score += self.settings.every_shoot_score_2

                        # 检查血量
                        if tank.blood <= 0:
                            self.settings.blast.play()
                            explosion = Explosion(self, tank.rect.center)
                            self.bad_tanks.add(explosion)
                            self.bad_tanks.remove(tank)

        if not self.bad_tanks:
            self.bullets.empty()
            self._create_fleet()

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.good_tank.moving_right = True
                    self.dic = 'right'
                elif event.key == pygame.K_LEFT:
                    self.good_tank.moving_left = True
                    self.dic = 'left'
                elif event.key == pygame.K_UP:
                    self.good_tank.moving_up = True
                    self.dic = 'up'
                elif event.key == pygame.K_DOWN:
                    self.good_tank.moving_down = True
                    self.dic = 'down'
                elif event.key == pygame.K_SPACE:
                    self._fire_bullet('yellow')
                if event.key == pygame.K_TAB:
                    self._fire_bullet('red')

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.good_tank.moving_right = False
                elif event.key == pygame.K_LEFT:
                    self.good_tank.moving_left = False
                elif event.key == pygame.K_UP:
                    self.good_tank.moving_up = False
                elif event.key == pygame.K_DOWN:
                    self.good_tank.moving_down = False

    def _fire_bullet(self, pattern='yellow'):
        if pattern == 'yellow':
            new_bullet = Bullet1(self)
            self.bullets.add(new_bullet)
            self.settings.shoot.play()
        elif pattern == 'red':
            new_bullet = Bullet2(self)
            self.bullets.add(new_bullet)
            self.settings.shoot.play()

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.good_tank.blitme()  # 在屏幕上绘制好坦克
        for bullet in self.bullets.sprites():
            bullet.draw()
        for explosion in self.bad_tanks.sprites():
            if isinstance(explosion, Explosion):
                explosion.draw()
            else:
                explosion.blitme()
        self.sb.show_score()
        self.blood_display.draw()
        pygame.display.flip()


if __name__ == '__main__':
    game = Game()
    game.run_game()
