import math
import random
import sys
import threading
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
        self.color_dic = {
            "白色": (255, 255, 255),
            "黑色": (0, 0, 0),
            "红色": (255, 0, 0),
            "绿色": (0, 128, 0),
            "蓝色": (0, 0, 255),
            "青色": (0, 128, 128),
            "紫色": (238, 130, 238),
            "灰色": (128, 128, 128),
            "黄色": (255, 255, 0),
            "镉黄": (255, 153, 18),
            "金黄": (255, 215, 0),
            "肉黄": (255, 125, 64),
            "粉黄": (255, 227, 132),
            "香蕉黄": (227, 207, 87),
            "白烟灰": (245, 245, 245),
            "蛋壳灰": (252, 230, 202),
            "黄绿色": (127, 255, 0),
            "青绿色": (64, 224, 205),
            "天蓝灰": (202, 235, 216),
            "象牙灰": (251, 255, 242),
            "亚麻灰": (250, 240, 230),
            "杏仁灰": (255, 235, 205),
            "贝壳灰": (255, 245, 238),
            "棕褐色": (210, 180, 140),
            "爱丽丝蓝": (240, 248, 255),
            "古董白": (250, 235, 215),
            "浅绿色": (175, 238, 238),
            "海蓝色": (127, 255, 212),
            "蔚蓝色": (240, 255, 255),
            "米色": (245, 245, 220),
            "橘黄色": (255, 228, 196),
            "白杏仁": (255, 235, 205),
            "蓝紫色": (138, 43, 226),
            "棕色": (165, 42, 42),
            "硬木色": (222, 184, 135),
            "学员蓝": (95, 158, 160),
            "淡黄绿色": (127, 255, 0),
            "巧克力色": (210, 105, 30),
            "珊瑚色": (255, 127, 80),
            "矢车菊蓝": (100, 149, 237),
            "玉米丝色": (255, 248, 220),
            "深红": (220, 20, 60),
            "深蓝色": (0, 0, 139),
            "深青色": (0, 139, 139),
            "暗金色": (184, 134, 11),
            "深灰色": (169, 169, 169),
            "深绿色": (0, 100, 0),
            "深色卡其色": (189, 183, 107),
            "深品红色": (139, 0, 139),
            "深橄榄绿": (85, 107, 47),
            "深橙色": (255, 140, 0),
            "暗兰花": (153, 50, 204),
            "深红色": (139, 0, 0),
            "暗三文鱼": (233, 150, 122),
            "深海绿": (143, 188, 143),
            "深条纹蓝": (72, 61, 139),
            "深色条纹灰色": (47, 79, 79),
            "深绿松石": (0, 206, 209),
            "深紫色": (148, 0, 211),
            "深粉色": (255, 20, 147),
            "深蓝": (0, 191, 255),
            "暗灰色": (105, 105, 105),
            "道奇蓝": (30, 144, 255),
            "长石色": (209, 146, 117),
            "火砖色": (178, 34, 34),
            "花朵白色": (255, 250, 240),
            "森林绿": (34, 139, 34),
            "紫红色": (255, 0, 255),
            "淡灰色": (220, 220, 220),
            "幽灵白": (248, 248, 255),
            "黄金": (255, 2, 150),
            "鲜黄色": (218, 165, 32),
            "绿黄色": (173, 255, 47),
            "蜜露色": (240, 255, 240),
            "粉红色": (255, 192, 203),
            "印度红": (205, 92, 92),
            "靛蓝": (75, 0, 130),
            "象牙色": (255, 255, 240),
            "卡其色": (240, 230, 140),
            "薰衣草色": (230, 230, 250),
            "淡紫色腮红": (255, 240, 245),
            "草坪绿": (124, 252, 0),
            "柠檬色": (255, 250, 205),
            "淡蓝色": (173, 216, 230),
            "淡珊瑚色": (240, 128, 128),
            "淡青色": (224, 255, 255),
            "亮金黄色": (250, 250, 210),
            "浅灰色": (211, 211, 211),
            "浅粉色": (255, 182, 193),
            "浅鲑鱼肉色": (255, 160, 122),
            "浅海洋绿": (32, 178, 170),
            "淡天蓝色": (135, 206, 250),
            "亮条纹蓝": (132, 112, 255),
            "浅石板灰": (119, 136, 153),
            "亮钢蓝": (176, 196, 222),
            "浅黄色": (255, 255, 224),
            "石灰": (0, 255, 0),
            "柠檬绿": (50, 205, 50),
            "亚麻色": (250, 240, 230),
            "品红色": (255, 0, 255),
            "栗色": (128, 0, 0),
            "间绿色": (102, 205, 170),
            "中等蓝色": (0, 0, 205),
            "中兰花紫": (186, 85, 211),
            "中等紫色": (147, 112, 216),
            "中海洋绿": (60, 179, 113),
            "中板岩蓝": (123, 104, 238),
            "中等春绿色": (0, 250, 154),
            "中等绿松石色": (72, 209, 204),
            "中等琴红": (199, 21, 133),
            "午夜蓝": (25, 25, 112),
            "薄荷色": (245, 255, 250),
            "薄雾玫瑰色": (255, 228, 225),
            "莫卡辛色": (255, 228, 181),
            "纳瓦霍白": (255, 222, 173),
            "海军蓝": (0, 0, 128),
            "旧蕾丝色": (253, 245, 230),
            "橄榄色": (107, 142, 35),
            "橙色": (255, 165, 0),
            "橙红色": (255, 69, 0),
            "兰花色": (218, 112, 214),
            "淡菊黄色": (238, 232, 170),
            "淡绿色": (152, 251, 152),
            "淡紫罗兰红": (216, 112, 147),
            "番木色": (255, 239, 213),
            "桃色": (255, 218, 185),
            "秘鲁褐": (205, 133, 63),
            "梅花色": (221, 160, 221),
            "粉末蓝": (176, 224, 230),
            "玫瑰棕色": (188, 143, 143),
            "皇家蓝": (65, 105, 225),
            "马鞍棕色": (139, 69, 19),
            "浅橙色": (250, 128, 114),
            "沙棕色": (244, 164, 96),
            "海绿色": (46, 139, 87),
            "海贝色": (255, 245, 238),
            "褐土色": (160, 82, 45),
            "银色": (192, 192, 192),
            "天蓝": (135, 206, 235),
            "板条蓝": (106, 90, 205),
            "板条灰色": (112, 128, 144),
            "雪色": (255, 250, 250),
            "春绿色": (0, 255, 127),
            "钢蓝": (70, 130, 180),
            "蓟花色": (216, 191, 216),
            "番茄色": (255, 99, 71),
            "绿松石色": (64, 224, 208),
            "小提琴红": (208, 32, 144),
            "小麦色": (245, 222, 179),
            "白烟色": (245, 245, 245)
        }
        self.word_interval = 45
        self.font_path = 'other/字体.ttf'
        self.tank_speed = 4.0
        self.bad_tank_speed = self.tank_speed / 2
        self.bullet_speed = 6.0
        self.bullets_num = 50
        self.super_bullet_speed = 8.0
        self.bullet_width = 7
        self.bullet_height = 7
        self.default_direction = 'up'
        self.bad_tank_num = 6
        self.good_tank_left = 7
        self.bad_tank1_blood = 5
        self.bad_tank2_blood = 3
        self.every_shoot_score_1 = 10
        self.every_shoot_score_2 = 20
        self.yellow_shoot_damage = 1
        self.red_shoot_damage = 2
        self.yellow_shoot_money = 3
        self.red_shoot_money = 5
        self.blood_image = pygame.image.load('image/blood.png')
        self.bullet_image = pygame.image.load('image/bullet1.png')
        self.bullet2_image = pygame.image.load('image/bullet2#.png')
        self.bullet3_image = pygame.image.load('image/bullet3#.png')
        self.button_2_image = pygame.image.load('image/button2.png')
        self.button_3_image = pygame.image.load('image/button3.png')
        self.button_4_image = pygame.image.load('image/button4.png')
        self.bg_image = pygame.image.load('image/background.jpg')
        self.start_image = pygame.image.load('image/startgame.jpg')
        self.back_ground_music1 = 'music/bgm1.mp3'
        self.back_ground_music2 = 'music/bgm2.mp3'
        self.blast = pygame.mixer.Sound('music/爆炸.mp3')
        self.good_tank_shoot = pygame.mixer.Sound('music/好坦克射击.mp3')
        self.bad_tank_shoot = pygame.mixer.Sound('music/坏坦克射击.mp3')
        self.strike = pygame.mixer.Sound('music/撞击.mp3')
        self.help_text_title = '你好，玩家！'
        self.help_text = ['1.在任何时候按下Q键以退出游戏/回到主界面。',
                          '2.对战中，使用WASD键位移动，使用鼠标左键单击射击。',
                          '3.鼠标左键长按发射强力子弹。',
                          '3.在对战时按下CTRL键可以切换强力子弹。',
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
        for i in range(self.settings.good_tank_left):
            blood_position = self.blood_rect.topleft
            blood_position = (blood_position[0] + i * (self.blood_rect.width + 5), blood_position[1])
            self.screen.blit(self.blood_image, blood_position)


class ScoreBoard:
    def __init__(self, game):
        self.settings = game.settings
        self.screen = game.screen
        self.sreen_rect = self.screen.get_rect()
        self.score = 0
        self.font = pygame.font.SysFont(self.settings.font_path, 48)
        self.prep_score()

    def prep_score(self):
        self.score_str = str(self.score)
        self.score_image = self.font.render(self.score_str, True, self.settings.color_dic['白色'],
                                            self.settings.color_dic['黑色'])
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
    def __init__(self, game, bad_tank=None):
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings
        self.image = pygame.image.load('image/bullet1.png')
        self.rect = self.image.get_rect()

        # 根据发射者类型设置方向和位置
        if bad_tank is not None:
            self.shooter = bad_tank
            self.dic = bad_tank.dic
            if self.dic == 'up':
                self.rect.midbottom = bad_tank.rect.midtop
            elif self.dic == 'down':
                self.rect.midtop = bad_tank.rect.midbottom
            elif self.dic == 'right':
                self.rect.midleft = bad_tank.rect.midright
            elif self.dic == 'left':
                self.rect.midright = bad_tank.rect.midleft
        else:
            self.color = 'yellow'
            self.dic = game.dic  # 使用全局方向
            if self.dic == 'up':
                self.rect.midbottom = game.good_tank.rect.midtop
            elif self.dic == 'down':
                self.rect.midtop = game.good_tank.rect.midbottom
            elif self.dic == 'right':
                self.rect.midleft = game.good_tank.rect.midright
            elif self.dic == 'left':
                self.rect.midright = game.good_tank.rect.midleft

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

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
        self.game = game  # 保存 Game 实例
        self.bullets = pygame.sprite.Group()  # 新增子弹组

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        # 绘制血条
        blood_bar_width = (self.blood / self.settings.bad_tank1_blood) * self.rect.width
        pygame.draw.rect(self.screen, self.settings.color_dic['栗色'], (self.rect.x, self.rect.y, blood_bar_width, 5))

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

            new_bullet = Bullet1(self.game, bad_tank=self)
            self.game.bullets.add(new_bullet)
            self.settings.good_tank_shoot.play()
            self.last_move_time = current_time
            
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

            self.last_move_time = current_time

            self.rect.y = self.y
            self.rect.x = self.x
            self.last_move_time = current_time


class GoodTank:
    """管理好坦克的类"""

    def __init__(self, game, settigns):
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
        self.mouse_left_pressed_time = 0
        self.add_bullet = True
        self.blood_display = BloodDisplay(self)
        self._create_fleet()

    def run_game(self):
        self._start_game()

    def _start_game(self):
        thread1 = threading.Thread(target=self._music1)
        thread1.start()

        start_image = self.settings.start_image
        start_rect = start_image.get_rect()
        start_rect.center = (self.settings.screen_width // 2, self.settings.screen_height // 2)

        clock = pygame.time.Clock()
        running = True

        while running:
            # 绘制前景元素
            self.screen.blit(start_image, start_rect)

            # 绘制提示文字
            font = pygame.font.Font(self.settings.font_path, 36)
            font2 = pygame.font.Font(self.settings.font_path, 100)
            alpha = int(128 + 127 * math.sin(math.radians(pygame.time.get_ticks() / 5)))
            text = font.render("按任意键开始", True, (255, max(50, alpha), max(50, alpha)))
            text_rect = text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height - 60))
            alpha = int(128 + 127 * math.sin(math.radians(pygame.time.get_ticks() / 5)))
            text2 = font2.render("迷离世界", True, (255, max(50, alpha), max(50, alpha)))
            text_rect2 = text2.get_rect(center=(self.settings.screen_width // 2, 60))
            self.screen.blit(text, text_rect)
            self.screen.blit(text2, text_rect2)

            # 添加随机噪点特效
            for _ in range(30):  # 控制噪点数量
                x = random.randint(0, self.settings.screen_width)
                y = random.randint(0, self.settings.screen_height)
                pygame.draw.circle(self.screen, (255, 0, 0), (x, y), 1)

            pygame.display.flip()
            clock.tick(60)  # 限制60帧

            # 事件处理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    else:
                        running = False  # 退出循环
                        self._upgrade_mode(thread1)


    def _exercise_mode(self):
        time.sleep(0.5)
        global thread2
        thread2 = threading.Thread(target=self._music2)
        thread2.start()
        while True:
            self._check_collision()
            self._check_bullet_good_tank_collision()
            self._check_events()
            self.good_tank.update()
            self._update_bullets()
            self._update_bad_tanks()
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0 or bullet.rect.right <= 0 or bullet.rect.left >= self.settings.screen_width:
                    self.bullets.remove(bullet)
            self._update_screen()

    def _upgrade_mode(self, t1=None, inside=False):
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self._music1()  # 重新播放主菜单音乐
        running = True
        while running:
            # 每次循环重新计算beta
            beta = int(128 + 127 * math.sin(math.radians(pygame.time.get_ticks() / 10)))  # 调整除数
            text_color = (255, beta, beta)  # 直接使用beta

            # 绘制背景
            self.screen.blit(self.settings.bg_image, (0, 0))
            font0 = pygame.font.Font(self.settings.font_path, 70)
            font1 = pygame.font.Font(self.settings.font_path, 50)
            font2 = pygame.font.Font(self.settings.font_path, 30)
            with open("other/data.json", "r", encoding="utf-8") as f:
                content = f.read()
            title_text = font1.render('装备区', True, self.settings.color_dic['白色'])
            text_rect = title_text.get_rect()
            text_rect.topleft = (40, 40)
            self.screen.blit(title_text, text_rect)

            text0 = font0.render('帮助', True, self.settings.color_dic['火砖色'], self.settings.color_dic['浅石板灰'])
            text0_rect = title_text.get_rect()
            text0_rect.topright = (text0.get_width() + 40, self.settings.screen_height - text0.get_height())
            self.screen.blit(text0, text0_rect)

            text2 = font2.render("温馨提示：装备只可以用于一次对战，对战结束后将自动清空武器~~", True,
                                 self.settings.color_dic['白色'])
            self.screen.blit(text2, (
                self.settings.screen_width / 2 - text2.get_width() / 2,
                self.settings.screen_height - text2.get_height() * 2))
            bullet_text = font1.render(f"装载弹量限额：{self.settings.bullets_num}", True,
                                       self.settings.color_dic['白色'])
            bullet_rect = bullet_text.get_rect()
            self.screen.blit(bullet_text, (self.settings.screen_width - 400, 50))
            beta = int(128 + 127 * math.sin(math.radians(pygame.time.get_ticks() / 5)))
            text3 = font0.render("点此开始游戏！", True, text_color)  # 使用动态颜色
            text3_rect = text3.get_rect()
            text3_rect.topleft = (self.settings.screen_width - 430, self.settings.screen_height - 60)
            self.screen.blit(text3, (self.settings.screen_width - 450, self.settings.screen_height - 60))
            self.screen.blit(text3, (self.settings.screen_width - 450, self.settings.screen_height - 60))
            bullet2_image = self.settings.bullet2_image
            bullet3_image = self.settings.bullet3_image
            bullet2_rect = bullet2_image.get_rect()
            bullet2_rect.topleft = (100, 100)
            bullet3_rect = bullet3_image.get_rect()
            bullet3_rect.topright = (self.settings.screen_width - 100, 100)
            self.screen.blit(bullet2_image, bullet2_rect)
            self.screen.blit(bullet3_image, bullet3_rect)

            if not inside:
                text4 = font2.render(f"子弹2：{self.b2_num}", True, self.settings.color_dic['白色'])
                self.screen.blit(text4, (bullet2_rect.left + 50, bullet2_rect.bottom + 50))
                text5 = font2.render(f"子弹3：{self.b3_num}", True, self.settings.color_dic['白色'])
                self.screen.blit(text5, (bullet3_rect.left + 50, bullet3_rect.bottom + 50))
            else:
                self.b2_num = 0
                self.b3_num = 0
                text4 = font2.render(f"子弹2：{self.b2_num}", True, self.settings.color_dic['白色'])
                self.screen.blit(text4, (bullet2_rect.left + 50, bullet2_rect.bottom + 50))
                text5 = font2.render(f"子弹3：{self.b3_num}", True, self.settings.color_dic['白色'])
                self.screen.blit(text5, (bullet3_rect.left + 50, bullet3_rect.bottom + 50))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self._show_exit_prompt()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if text3_rect.collidepoint(mouse_pos):
                        pygame.mixer.music.stop()
                        if t1 is not None:
                            t1.join()
                        self._exercise_mode()
                    if text0_rect.collidepoint(mouse_pos):
                        self._help_mode()
                    if self.settings.bullets_num <= 0:
                        self.add_bullet = False
                    elif bullet2_rect.collidepoint(mouse_pos) and self.add_bullet:
                        self.b2_num += 1
                        self.settings.bullets_num -= 1
                        # 使用背景色填充旧的文本区域
                        pygame.draw.rect(self.screen, self.settings.color_dic['黑色'], (
                            bullet2_rect.left + 50, bullet2_rect.bottom + 50, text4.get_width(), text4.get_height()))
                        self.screen.blit(bullet2_image, bullet2_rect)
                        text4 = font2.render(f"子弹2：{self.b2_num}", True, self.settings.color_dic['白色'])
                        self.screen.blit(text4, (bullet2_rect.left + 50, bullet2_rect.bottom + 50))

                    elif bullet3_rect.collidepoint(mouse_pos) and self.add_bullet:
                        self.b3_num += 1
                        self.settings.bullets_num -= 1
                        # 使用背景色填充旧的文本区域
                        pygame.draw.rect(self.screen, self.settings.color_dic['黑色'], (
                            bullet3_rect.left + 50, bullet3_rect.bottom + 50, text5.get_width(), text5.get_height()))
                        self.screen.blit(bullet3_image, bullet3_rect)
                        text5 = font2.render(f"子弹3：{self.b3_num}", True, self.settings.color_dic['白色'])
                        self.screen.blit(text5, (bullet3_rect.left + 50, bullet3_rect.bottom + 50))






    def _help_mode(self):
        background = self.settings.bg_image
        self.screen.blit(background, (0, 0))
        font = pygame.font.Font(self.settings.font_path, 50)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self._upgrade_mode()()
                if event.type == pygame.QUIT:
                    running = False
            title_text = font.render(self.settings.help_text_title, True, self.settings.color_dic['白色'])
            text_rect = title_text.get_rect()
            text_rect.midtop = (self.settings.screen_width / 2, 10)
            self.screen.blit(title_text, text_rect)
            a = 0
            for text in self.settings.help_text:
                a += 1
                text_text = font.render(text, True, self.settings.color_dic['深红'])
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
                    self._show_exit_prompt(inside=True)
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

    def _music1(self):
        """播放主菜单音乐"""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.music.load(self.settings.back_ground_music1)
        pygame.mixer.music.play(-1)

    def _music2(self):
        """播放战斗音乐"""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.music.load(self.settings.back_ground_music2)
        pygame.mixer.music.play(-1)

    def _choose_things(self):
        # 显示文字
        font = pygame.font.Font(self.settings.font_path, 36)
        text = font.render("选择强力子弹的类型，鼠标左键长按使用", True, self.settings.color_dic['白色'])
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

    def _show_exit_prompt(self, text="退出并保存 (Y/N)", inside=False):
        """显示退出提示并等待用户响应"""
        font = pygame.font.Font(self.settings.font_path, 80)
        text = font.render(text, True, self.settings.color_dic['白色'])
        self.screen.blit(text, (self.settings.screen_width / 2 - text.get_width() / 2, self.settings.screen_height / 2))
        pygame.display.flip()
        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        if not inside:
                            with open('other/data.json', 'w+') as f:
                                file_content = f.read()
                                if file_content == '':
                                    file_content = '0'
                                f.write(str(int(file_content) + int(self.sb.score)))
                            pygame.quit()
                            sys.exit()
                        else:
                            self._one_game_over(myself=True)
                    elif event.key == pygame.K_n:
                        waiting_for_input = False

    def _check_collision(self):
        """检查好坦克与坏坦克的碰撞"""
        if pygame.sprite.spritecollideany(self.good_tank, self.bad_tanks):
            self._good_tank_hit()
            if self.settings.good_tank_left == 0:
                self._one_game_over()

    def _good_tank_hit(self):
        """响应好坦克被撞到"""
        self.settings.good_tank_left -= 1
        self.bad_tanks.empty()
        self.bullets.empty()
        self._create_fleet()
        self.good_tank.center_tank()
        self.blood_display.draw()
        time.sleep(0.5)

    def _one_game_over(self, myself=False):
        """ 单次游戏结束"""
        for bullet in self.bullets.copy():
            bullet.kill()
        for bad_tank in self.bad_tanks.copy():
            bad_tank.kill()
        self.settings.good_tank_left = -1
        pygame.mixer.music.stop()
        pygame.display.flip()
        font = pygame.font.Font(self.settings.font_path, 80)
        if not myself:
            text = font.render("您已死亡，即将退回主界面", True, self.settings.color_dic['白色'])
            self.screen.blit(text, (self.settings.screen_width / 2 - text.get_width() / 2, self.settings.screen_height / 2))
        else:
            pass
        with open('other/data.txt', 'w+') as f:
            file_content = f.read()
            if file_content == '':
                file_content = '0'
            f.write(str(int(file_content) + int(self.sb.score)))
        self.sb.score = 0
        pygame.display.flip()
        time.sleep(1)
        if not myself:
            self._upgrade_mode()
        else:
            self._upgrade_mode(inside=True)

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
        """检查子弹与坏坦克的碰撞（排除发射者自身）"""
        for bullet in self.bullets:
            # 跳过由坏坦克发射的子弹与自身碰撞
            if hasattr(bullet, 'shooter') and bullet.shooter in self.bad_tanks:
                continue  # 直接跳过该子弹的碰撞检测

            # 检测子弹与所有坏坦克的碰撞
            collisions = pygame.sprite.spritecollide(bullet, self.bad_tanks, False)
            if collisions:
                # 处理碰撞逻辑（仅针对非发射者）
                self.settings.strike.play()
                self.sb.prep_score()
                for tank in collisions:
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

                        # 检查血量是否归零
                        if tank.blood <= 0:
                            self.settings.blast.play()
                            explosion = Explosion(self, tank.rect.center)
                            self.bad_tanks.add(explosion)
                            self.bad_tanks.remove(tank)

                # 移除子弹（仅当子弹与敌人碰撞时）
                bullet.kill()

    def _check_bullet_good_tank_collision(self):
        """检测坏坦克子弹与好坦克的碰撞"""
        # 遍历所有子弹
        for bullet in self.bullets:
            # 检查是否是坏坦克发射的子弹
            if hasattr(bullet, 'shooter') and isinstance(bullet.shooter, (BadTank1, BadTank2)):
                # 检测子弹与好坦克的碰撞
                if pygame.sprite.collide_rect(bullet, self.good_tank):
                    self.settings.good_tank_left -= 1
                    self.bad_tanks.empty()
                    self.bullets.empty()
                    self._create_fleet()
                    self.good_tank.center_tank()
                    self.blood_display.draw()
                    time.sleep(0.5)
                    if self.settings.good_tank_left == 0:
                        self._one_game_over()

    def _fire_bullet(self, pattern='yellow'):
        if pattern == 'yellow':
            new_bullet = Bullet1(self)
            self.bullets.add(new_bullet)
            self.settings.good_tank_shoot.play()
        elif pattern == 'red' and self.b2_num > 0:
            new_bullet = Bullet2(self)
            self.bullets.add(new_bullet)
            self.settings.good_tank_shoot.play()
        elif pattern == 'gold' and self.b3_num > 0:
            new_bullet = Bullet3(self)
            self.bullets.add(new_bullet)
            self.settings.good_tank_shoot.play()
        elif self.b2_num < 0 or self.b3_num < 0:
            font = pygame.font.Font(self.settings.font_path, 80)
            text = font.render('该型号子弹已空 (Y)', True, self.settings.color_dic['白色'])
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
        self.screen.fill(self.settings.color_dic['黑色'])
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
