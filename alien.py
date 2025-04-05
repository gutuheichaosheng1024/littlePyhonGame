import pygame
from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self, ai_game):
        """初始化外星人及其初始位置"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #加载外星人图像及其属性
        self.image = pygame.image.load('img/enemy.bmp')
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect()

        #设置外星人属性
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def update(self):
        """向右移动外星人"""

        self.x += self.settings.alien_speed*self.settings.fleet_direction
        self.rect.x = self.x

    def check_edge(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)