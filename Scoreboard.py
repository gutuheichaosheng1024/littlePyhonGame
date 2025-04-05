import pygame
from pygame.sprite import Group

from Ship import Ship

class Scoreboard:
    """显示得分信息的类"""
    
    def __init__(self, ai_game):
        """"初始化显示得分涉及属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.status
        
        #显示得分信息的字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        
        #准备初始得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ship()

    def prep_score(self):
        """将得分渲染成图像"""
        rounded_score = round(self.stats.score, -1)
        score_str = f"{rounded_score:,}"
        self.score_image = self.font.render(score_str, True, self.text_color,self.settings.bg_color)

        #右上角显示得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.rect.right-20
        self.score_rect.top = self.rect.top

    def show_score(self):
        """屏幕上显示分数"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score__rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """渲染最高分为图像"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = f"{high_score:,}"
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        self.high_score__rect = self.high_score_image.get_rect()
        self.high_score__rect.centerx = self.rect.centerx
        self.high_score__rect.top = self.rect.top

    def check_high_score(self):
        """检查是否诞生了最高分"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom+10

    def prep_ship(self):
        """显示剩下多少飞船 """
        self.ships  = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)