import random
import sys
import time

import pygame
from pygame.sprite import Sprite

__author__ = 'XSY'
dic = 'up'


class Settings:
    """存储游戏所有设置的类"""

    def __init__(self):
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen_width = self.screen.get_rect().width
        self.screen_height = self.screen.get_rect().height
        self.bg_color = (0, 0, 0)
        self.bg_color2 = (128, 128, 128)
        self.word_interval = 45
        self.font_color = (255, 255, 255)
        self.font_path = 'other/字体.ttf'
        self.tank_speed = 2.0
        self.bad_tank_speed = self.tank_speed / 2
        self.bullet_speed = 3.0
        self.bullets_num = 50
        self.super_bullet_speed = 6.0
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
        self.bullet2_image = pygame.image.load('image/bullet2#.png')
        self.bullet3_image = pygame.image.load('image/bullet3#.png')
        self.dead_image = pygame.image.load('image/dead.png')
        self.exit_image = pygame.image.load('image/exit.png')
        self.button_1_image = pygame.image.load('image/button1.png')
        self.button_2_image = pygame.image.load('image/button2.png')
        self.button_3_image = pygame.image.load('image/button3.png')
        self.button_4_image = pygame.image.load('image/button4.png')
        self.bg_image = pygame.image.load('image/refit_back_ground.png')
        self.blast = pygame.mixer.Sound('music/爆炸.mp3')
        self.shoot = pygame.mixer.Sound('music/射击.mp3')
        self.strike = pygame.mixer.Sound('music/撞击.mp3')
        self.help_text_title = '你好，玩家！'
        self.help_text = ['1.在任何时候按下Q键以退出游戏/回到主界面。',
                          '2.对战中，使用WASD键位移动，使用鼠标左键单击射击。',
                          '3.鼠标左键长按发射强力子弹。',
                          '3.按下CTRL键可以切换强力子弹。',
                          '3.短按左键为普通子弹，长按为强力子弹。']


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
        self.font = pygame.font.SysFont(self.settings.font_path, 48)
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
        self.explosion_images = [pygame.image.load(f'image/e{i}.gif') for i in range(1, 16)]
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

        # 根据坦克d的方向设置子弹的初始位置
        if game.dic == 'up':
            self.rect.midbottom = game.good_tank.rect.midtop
        elif game.dic == 'down':
            self.rect.midtop = game.good_tank.rect.midbottom
        elif game.dic == 'right':
            self.rect.midleft = game.good_tank.rect.midright
        elif game.dic == 'left':
            self.rect.midright = game.good_tank.rect.midleft

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


class Bullet3(Bullet1):
    def __init__(self, game):
        super(Bullet3, self).__init__(game)
        self.image = pygame.image.load('image/bullet3.png')
        self.rect = self.image.get_rect()
        self.color = 'green'

    def update(self):
        if self.dic == 'up':
            self.y -= self.settings.super_bullet_speed
        elif self.dic == 'down':
            self.y += self.settings.super_bullet_speed
        elif self.dic == 'right':
            self.x += self.settings.super_bullet_speed
        elif self.dic == 'left':
            self.x -= self.settings.super_bullet_speed
        self.rect.y = self.y
        self.rect.x = self.x


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
                if self.rect.top > 60:  # 检查是否超出上边界
                    self.y -= self.tank_speed * 100
                    self.image = pygame.image.load('image\\turn0bad.png')
                else:
                    self.random_move()  # 碰到边缘时随机改变方向
            elif self.dic == 'down':
                if self.rect.bottom < self.screen_rect.bottom - 60:  # 检查是否超出下边界
                    self.y += self.tank_speed * 100
                    self.image = pygame.image.load('image\\turn180bad.png')
                else:
                    self.random_move()
            elif self.dic == 'right':
                if self.rect.right < self.screen_rect.right - 60:  # 检查是否超出右边界
                    self.x += self.tank_speed * 100
                    self.image = pygame.image.load('image\\turn90bad.png')
                else:
                    self.random_move()
            elif self.dic == 'left':
                if self.rect.left > 60:  # 检查是否超出左边界
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
        self.chosen_bullet = "bullet3"
        self.b2_num = 0
        self.b3_num = 0
        self.add_bullet = True
        self.blood_display = BloodDisplay(self)
        self._create_fleet()

    def run_game(self):

        self._refit_mode()

    def _refit_mode(self):
        for bullet in self.bullets.copy():
            bullet.kill()
        for bad_tank in self.bad_tanks.copy():
            bad_tank.kill()
        background = self.settings.bg_image
        self.screen.blit(background, (0, 0))
        # 加载按钮图片
        button1_image = self.settings.button_1_image
        button2_image = self.settings.button_2_image

        # 获取按钮的矩形区域，并设置它们的位置
        button1_rect = button1_image.get_rect()
        button1_rect.topleft = (50, 50)  # 设置按钮1的位置
        button2_rect = button2_image.get_rect()
        button2_rect.topright = (self.settings.screen_width - 50, 50)  # 设置按钮2的位置
        button3_rect = self.settings.button_3_image.get_rect()
        button3_rect.bottomleft = (50, self.settings.screen_height - 50)
        button4_rect = self.settings.button_4_image.get_rect()
        button4_rect.bottomright = (self.settings.screen_width - 50, self.settings.screen_height - 50)

        # 在屏幕上绘制按钮
        self.screen.blit(button1_image, button1_rect)
        self.screen.blit(button2_image, button2_rect)
        self.screen.blit(self.settings.button_3_image, button3_rect)
        self.screen.blit(self.settings.button_4_image, button4_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 鼠标左键按下
                        self.mouse_left_pressed_time = pygame.time.get_ticks()
                        mouse_pos = event.pos
                        if button1_rect.collidepoint(mouse_pos):
                            self._exercise_mode()
                        elif button2_rect.collidepoint(mouse_pos):
                            self._upgrade_mode()
                        elif button3_rect.collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit()
                        elif button4_rect.collidepoint(mouse_pos):
                            self._help_mode()

    def _exercise_mode(self):
        time.sleep(0.5)
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

    def _upgrade_mode(self):
        background = self.settings.bg_image
        self.screen.blit(background, (0, 0))
        font1 = pygame.font.Font(self.settings.font_path, 50)
        font2 = pygame.font.Font(self.settings.font_path, 30)
        with open("other/data.txt", "r", encoding="utf-8") as f:
            content = f.read()
        title_text = font1.render('装备区', True, self.settings.text_color)
        text_rect = title_text.get_rect()
        text_rect.topleft = (40, 40)
        self.screen.blit(title_text, text_rect)
        text2 = font2.render("温馨提示：装备只可以用于一次对战，对战结束后将自动清空武器~~", True,
                             self.settings.font_color)
        self.screen.blit(text2, (
            self.settings.screen_width / 2 - text2.get_width() / 2, self.settings.screen_height - text2.get_height() * 2))
        bullet_text = font1.render(f"装载弹量限额：{self.settings.bullets_num}", True, self.settings.font_color)
        bullet_rect = bullet_text.get_rect()
        self.screen.blit(bullet_text, ((self.settings.screen_width - 400, 60)))
        text3 = font2.render("现在开始游戏！", True, (255, 0, 0))
        text3_rect = text3.get_rect()
        text3_rect.topleft = (self.settings.screen_width - 400, self.settings.screen_height - 60)
        self.screen.blit(text3, ((self.settings.screen_width - 400, self.settings.screen_height - 60)))
        bullet2_image = self.settings.bullet2_image
        bullet3_image = self.settings.bullet3_image
        bullet2_rect = bullet2_image.get_rect()
        bullet2_rect.topleft = (100, 100)
        bullet3_rect = bullet3_image.get_rect()
        bullet3_rect.topright = (self.settings.screen_width - 100, 100)
        self.screen.blit(bullet2_image, bullet2_rect)
        self.screen.blit(bullet3_image, bullet3_rect)

        text4 = font2.render(f"子弹2：{self.b2_num}", True, self.settings.font_color)
        self.screen.blit(text4, (bullet2_rect.left + 50, bullet2_rect.bottom + 50))
        text5 = font2.render(f"子弹3：{self.b3_num}", True, self.settings.font_color)
        self.screen.blit(text5, (bullet3_rect.left + 50, bullet3_rect.bottom + 50))
        pygame.display.flip()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self._show_exit_prompt()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.settings.bullets_num <= 0:
                        self.add_bullet = False
                    if bullet2_rect.collidepoint(mouse_pos) and self.add_bullet:
                        self.b2_num += 1
                        self.settings.bullets_num -= 1
                        # 使用背景色填充旧的文本区域
                        pygame.draw.rect(self.screen, self.settings.bg_color, (
                            bullet2_rect.left + 50, bullet2_rect.bottom + 50, text4.get_width(), text4.get_height()))
                        self.screen.blit(bullet2_image, bullet2_rect)
                        text4 = font2.render(f"子弹2：{self.b2_num}", True, self.settings.font_color)
                        self.screen.blit(text4, (bullet2_rect.left + 50, bullet2_rect.bottom + 50))

                    elif bullet3_rect.collidepoint(mouse_pos) and self.add_bullet:
                        self.b3_num += 1
                        self.settings.bullets_num -= 1
                        # 使用背景色填充旧的文本区域
                        pygame.draw.rect(self.screen, self.settings.bg_color, (
                            bullet3_rect.left + 50, bullet3_rect.bottom + 50, text5.get_width(), text5.get_height()))
                        self.screen.blit(bullet3_image, bullet3_rect)
                        text5 = font2.render(f"子弹3：{self.b3_num}", True, self.settings.font_color)
                        self.screen.blit(text5, (bullet3_rect.left + 50, bullet3_rect.bottom + 50))

                    elif text3_rect.collidepoint(mouse_pos):
                        self._exercise_mode()
                    pygame.display.flip()



        pygame.display.flip()

    def _help_mode(self):
        background = self.settings.bg_image
        self.screen.blit(background, (0, 0))
        font = pygame.font.Font(self.settings.font_path, 50)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self._re
                if event.type == pygame.QUIT:
                    running = False
            title_text = font.render(self.settings.help_text_title, True, self.settings.text_color)
            text_rect = title_text.get_rect()
            text_rect.midtop = (self.settings.screen_width / 2, 10)
            self.screen.blit(title_text, text_rect)
            a = 0
            for text in self.settings.help_text:
                a += 1
                text_text = font.render(text, True, self.settings.text_color)
                text_rect = text_text.get_rect()
                text_rect.midtop = (self.settings.screen_width / 2, 10 + a * self.settings.word_interval)
                self.screen.blit(text_text, text_rect)
            pygame.display.flip()

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.good_tank.moving_right = True
                    self.dic = 'right'
                elif event.key == pygame.K_a:
                    self.good_tank.moving_left = True
                    self.dic = 'left'
                elif event.key == pygame.K_w:
                    self.good_tank.moving_up = True
                    self.dic = 'up'
                elif event.key == pygame.K_s:
                    self.good_tank.moving_down = True
                    self.dic = 'down'
                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    self._choose_things()
                elif event.key == pygame.K_q:
                    self._show_exit_prompt()
            elif event.type == pygame.KEYUP:  # 添加按键释放事件处理
                if event.key == pygame.K_d:
                    self.good_tank.moving_right = False
                elif event.key == pygame.K_a:
                    self.good_tank.moving_left = False
                elif event.key == pygame.K_w:
                    self.good_tank.moving_up = False
                elif event.key == pygame.K_s:
                    self.good_tank.moving_down = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 鼠标左键按下
                    self.mouse_left_pressed_time = pygame.time.get_ticks()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # 鼠标左键释放
                    press_duration = pygame.time.get_ticks() - self.mouse_left_pressed_time
                    if press_duration < 200:  # 如果按下时间小于500毫秒，发射黄色子弹
                        self._fire_bullet('yellow')
                    else:
                        if self.chosen_bullet == 'bullet2':
                            self.b2_num -= 1
                            self._fire_bullet('red')

                        elif self.chosen_bullet == 'bullet3':
                            self.b3_num -= 1
                            self._fire_bullet('gold')

    def _choose_things(self):
        # 显示文字
        font = pygame.font.Font(self.settings.font_path, 36)
        text = font.render("选择强力子弹的类型，鼠标左键长按使用", True, self.settings.font_color)
        self.screen.blit(self.settings.bg_image, (0, 0))
        self.screen.blit(text, (20, 20))
        # 加载子弹图片
        bullet2_image = self.settings.bullet2_image
        bullet3_image = self.settings.bullet3_image

        # 获取子弹图片的矩形区域，并设置它们的位置
        bullet2_rect = bullet2_image.get_rect()
        bullet2_rect.topleft = (100, 100)  # 设置子弹2图片的位置
        bullet3_rect = bullet3_image.get_rect()
        bullet3_rect.topright = (self.settings.screen_width - 100, 100)  # 设置子弹3图片的位置

        # 在屏幕上绘制子弹图片
        self.screen.blit(bullet2_image, bullet2_rect)
        self.screen.blit(bullet3_image, bullet3_rect)
        pygame.display.flip()

        # 等待玩家点击
        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if bullet2_rect.collidepoint(mouse_pos):
                        self.chosen_bullet = 'bullet2'
                        waiting_for_click = False
                    elif bullet3_rect.collidepoint(mouse_pos):
                        self.chosen_bullet = 'bullet3'
                        waiting_for_click = False

    def _show_exit_prompt(self, text="退出并保存 (Y/N)"):
        """显示退出提示并等待用户响应"""
        font = pygame.font.Font(self.settings.font_path, 80)
        text = font.render(text, True, self.settings.font_color)
        self.screen.blit(text, (self.settings.screen_width / 2 - text.get_width() / 2, self.settings.screen_height / 2))
        pygame.display.flip()
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        with open('other/data.txt', 'w+') as f:
                            file_content = f.read()
                            if file_content == '':
                                file_content = '0'
                            f.write(str(int(file_content) + int(self.sb.score)))
                        self.sb.score = 0
                        self._refit_mode()
                    elif event.key == pygame.K_n:
                        waiting_for_input = False

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
        for bullet in self.bullets.copy():
            bullet.kill()
        for bad_tank in self.bad_tanks.copy():
            bad_tank.kill()
        pygame.display.flip()
        font = pygame.font.Font(self.settings.font_path, 80)
        text = font.render("您已死亡，即将退回主界面", True, self.settings.font_color)
        self.screen.blit(text, (self.settings.screen_width / 2 - text.get_width() / 2, self.settings.screen_height / 2))
        with open('other/data.txt', 'w+') as f:
            file_content = f.read()
            if file_content == '':
                file_content = '0'
            f.write(str(int(file_content) + int(self.sb.score)))
        self.sb.score = 0
        pygame.display.flip()
        time.sleep(2)
        self._refit_mode()

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
            for bullet, bad_tank_list in collisions.items():
                for tank in bad_tank_list:
                    if isinstance(tank, (BadTank1, BadTank2)):
                        if bullet.color == 'yellow':
                            tank.blood -= self.settings.yellow_shoot_damage
                            self.sb.score += self.settings.every_shoot_score_1

                        elif bullet.color == 'red':
                            tank.blood -= self.settings.red_shoot_damage
                            self.sb.score += self.settings.every_shoot_score_2

                        elif bullet.color == 'green':
                            tank.blood -= self.settings.yellow_shoot_damage
                            self.sb.score += self.settings.every_shoot_score_1

                        # 检查血量
                        if tank.blood <= 0:
                            self.settings.blast.play()
                            explosion = Explosion(self, tank.rect.center)
                            self.bad_tanks.add(explosion)
                            self.bad_tanks.remove(tank)

        if not self.bad_tanks:
            self.bullets.empty()
            self._create_fleet()

    def _fire_bullet(self, pattern='yellow'):
        if pattern == 'yellow':
            new_bullet = Bullet1(self)
            self.bullets.add(new_bullet)
            self.settings.shoot.play()
        elif pattern == 'red' and self.b2_num > 0:
            new_bullet = Bullet2(self)
            self.bullets.add(new_bullet)
            self.settings.shoot.play()
        elif pattern == 'gold' and self.b3_num > 0:
            new_bullet = Bullet3(self)
            self.bullets.add(new_bullet)
            self.settings.shoot.play()
        elif self.b2_num < 0 or self.b3_num < 0:
            font = pygame.font.Font(self.settings.font_path, 80)
            text = font.render('该型号子弹已空 (Y)', True, self.settings.font_color)
            self.screen.blit(text,
                             (self.settings.screen_width / 2 - text.get_width() / 2, self.settings.screen_height / 2))
            pygame.display.flip()
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_y:
                            waiting_for_input = False



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
