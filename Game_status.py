
class GameStatus:
    """统计游戏的状态信息"""
    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_start()
        self.high_score = 0



    def reset_start(self):
        """初始化设置"""

        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1