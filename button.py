import pygame.font

class Button:
    """按钮的类"""

    def __init__(self, ai_game,msg,x,y):
        """初始化按钮属性"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        #设置按钮尺寸与属性
        self.width, self.height = 100, 50
        self.button_color = (135, 135, 135)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 48)

        #创建按钮矩形对象,并居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = x,y

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """将 msg渲染为图像"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制填充了颜色的矩形,再绘制文本"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)