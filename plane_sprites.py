import random
import pygame

#窗口 大小的常量
SCREEN_RECT = pygame.Rect(0,0,480,700)
#刷新频率的常量
FRAME_FREP = 60
#敌机定时器的常量
CREATE_ENEMY = pygame.USEREVENT
#英雄发射子弹事件的常量
HERO_FIRE = pygame.USEREVENT + 1

class GameSprite(pygame.sprite.Sprite):
    '''飞机大战游戏精灵'''

    def __init__(self,image_name,speed=1):

        # 父类不是object，要主动调用父类的初始化方法
        super().__init__()

        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        #在屏幕上方垂直移动
        self.rect.y += self.speed


class Background(GameSprite):
    '''游戏背景精灵'''

    '''
       is_alt判断是否是另一张图像
       False 表示需要和屏幕重合的图像
       True 表示在屏幕正上方的另一张图像
    '''
    def __init__(self,is_alt=False):

        #调用父类的方法实现精灵的创建
        super().__init__('./images/background.png')

        #判断是否交替图像，如果是，需要设置初始位置
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        #调用父类的方法实现
        super().update()

        #判断是否移出屏幕，如果移出屏幕，将图像设置到屏幕的上方
        if self.rect.y >= SCREEN_RECT.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    '''敌机精灵'''

    def __init__(self):
        #调用父类方法，创建敌机精灵，同时指定敌机图片
        super().__init__('./images/enemy1.png')

        #指定敌机的初始随机速度
        self.speed = random.randint(1,3)

        #指定敌机的初始随机位置
        #设置y值
        self.rect.bottom = 0
        #设置x值的随机值
        max_x = SCREEN_RECT.width - self.rect.width
        self.rect.x = random.randint(0,max_x)

    def update(self):
        #调用父类方法，保持垂直方向的飞行
        super().update()

        #判断是否飞出屏幕，如果是，需要从精灵组删除敌机
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()


class Hero(GameSprite):
    '''英雄精灵'''

    def __init__(self):
        #调用父类的方法，初始速度设置为0，英雄一开始是不动的
        super().__init__('./images/me1.png',0)

        #设置英雄的初始位置
        #1.英雄出现在中心位置
        self.rect.centerx = SCREEN_RECT.centerx
        #2.英雄距离屏幕120
        self.rect.bottom = SCREEN_RECT.bottom - 120

        #创建子弹的精灵组
        self.bullets = pygame.sprite.Group()

    def update(self):
        #英雄向水平方向移动
        self.rect.x += self.speed

        #判断英雄是否移出屏幕
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

    def fire(self):
        #一次发射三颗子弹
        for i in (0,1,2):
            #创建子弹精灵
            bullet = Bullet()

            #子弹的初始位置
            bullet.rect.bottom = self.rect.y - i * 20
            bullet.rect.centerx = self.rect.centerx

            #将精灵添加到精灵组
            self.bullets.add(bullet)


class Bullet(GameSprite):
    '''子弹精灵'''

    def __init__(self):
        #调用父类的方法，设置图片，初始速度设置为-2
        super().__init__('./images/bullet1.png',-2)

    def update(self):
        #调用父类的方法
        super().update()
        #判断子弹是否飞出屏幕，如果是，删除子弹
        if self.rect.bottom < 0:
            self.kill()