import pygame
from plane_sprites import *

class PlaneGame(object):
    '''飞机大战主游戏'''

    def __init__(self):
        print('游戏初始化')

        # 1.创建游戏的窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2.创建游戏的时钟
        self.clock = pygame.time.Clock()
        # 3.调用私有方法，精灵和精灵组的创建
        self.__create_sprites()
        # 4.设置定时器事件
        pygame.time.set_timer(CREATE_ENEMY,1000)
        pygame.time.set_timer(HERO_FIRE,500)

    # 创建精灵和精灵组的方法
    def __create_sprites(self):
        #创建背景精灵和精灵组
        bg1 = Background()
        bg2 = Background(True)
        self.back_group = pygame.sprite.Group(bg1,bg2)

        #创建敌机精灵组
        self.enemy_group = pygame.sprite.Group()

        #创建英雄和英雄精灵组
        #后续要对英雄进行碰撞检测和发射子弹，所有把英雄定义成一个属性
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        print('游戏开始')

        while True:
            #1.设置刷新频率
            self.clock.tick(FRAME_FREP)
            #2.事件监听
            self.__event_handler()
            #3.碰撞检测
            self.__check_collide()
            #4.更新，绘制精灵组
            self.__update_sprites()
            #5.更新屏幕显示
            pygame.display.update()

    def __event_handler(self):  #事件监听方法
        for event in pygame.event.get():
            # 检测用户是否点击关闭键
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            #监听敌机定时器事件
            elif event.type == CREATE_ENEMY:
                #创建敌机精灵
                enemy = Enemy()
                #将敌机精灵添加到精灵组
                self.enemy_group.add(enemy)
            #监听英雄开火事件
            elif event.type == HERO_FIRE:
                self.hero.fire()

        #使用键盘提供的方法获取按键 - 按键元祖
        key_pressed = pygame.key.get_pressed()
        #判断元祖中对应的按键索引值
        if key_pressed[pygame.K_RIGHT]: #向右移动
            self.hero.speed = 3
        elif key_pressed[pygame.K_LEFT]: #向左移动
            self.hero.speed = -3
        else:                            #其他方向键，速度变为0
            self.hero.speed = 0

    def __check_collide(self):  #碰撞检测方法
        #子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)

        #英雄与敌机发生碰撞
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        #判断返回的列表是否有内容
        if len(enemies) > 0:
            #杀死英雄
            self.hero.kill()
            #游戏结束
            PlaneGame.__game_over()

    def __update_sprites(self):  #更新绘制精灵方法
        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update()
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod
    def __game_over():  #游戏结束的方法（私有方法）
        print('游戏结束...')
        pygame.quit()
        exit()

if __name__ == '__main__':

    #创建游戏对象
    game = PlaneGame()

    #调用游戏开始方法
    game.start_game()