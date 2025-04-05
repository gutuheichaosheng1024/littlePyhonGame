import sys
from time import sleep

import pygame


from Settings import Settings
from Ship import Ship
from bullet import Bullet
from alien import Alien
from Game_status import GameStatus
from button import Button
from Scoreboard import Scoreboard

class AlienInvasion:
    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("music/sound.mp3")
        pygame.mixer.music.play(-1)

        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion')
        #创建实例记录游戏状态
        self.status = GameStatus(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.game_active = False
        x,y = self.screen.get_rect().center
        self.play_botton = Button(self,"Play",x,y)
        self.hard_botton = Button(self, "Hard", 50, 30)

    def run_game(self):
        """开始游戏主循环"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        # 侦听鼠标键盘事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos,False)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)


    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._check_play_button(pygame.mouse.get_pos(),True)

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False
        elif event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False

    def _fire_bullet(self):
        """创建子弹并加入编组"""
        if len(self.bullets) <= self.settings.bullet_limit:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """创建外星舰队"""
        #先创建一个外星人

        alien = Alien(self)
        alien_width,alien_height = alien.rect.size

        current_x,current_y = alien_width,alien_height
        while current_y < self.settings.screen_height-4*alien_height:
            while current_x <= self.settings.screen_width-2*alien_width:
                self._create_alien(current_x,current_y)
                current_x += alien_width*2
            current_x = alien_width
            current_y += alien_height*2

    def _create_alien(self,x_position,y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        """检查舰队里有没有外星人到边缘"""
        for alien in self.aliens.sprites():
            if alien.check_edge():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """向下移动并改变方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.game_active:
            self.play_botton.draw_button()
            self.hard_botton.draw_button()
        pygame.display.flip()

    def _update_aliens(self):
        """更新全部外星人的位置"""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            print("Hit!!!!!")
        self._check_aliens_bottom()

    def _update_bullets(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_aliens_collision()

    def _check_bullet_aliens_collision(self):
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #提高等级
            self.status.level +=1
            self.sb.prep_score()

        collections = pygame.sprite.groupcollide(self.bullets,self.aliens,True,True)

        if collections:
            for alien in collections.values():
                self.status.score += self.settings.alien_points*len(alien)
            self.sb.prep_score()
            self.sb.check_high_score()
        #检测两个组之间是否有碰撞,有的话就删除双方

    def _ship_hit(self):
        """相应船的碰撞"""

        print("yes")
        if self.status.ships_left > 0:
            self.status.ships_left -=1

            self.bullets.empty()
            self.aliens.empty()

            #创建新舰队,并将飞船放到屏幕底边中央
            self.ship.center_ship()
            self._create_fleet()
            self.sb.prep_ship()

            sleep(0.5)

        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos,isButton):
        """单击开始游戏"""
        button_active = (self.play_botton.rect.collidepoint(mouse_pos) or isButton) and not self.game_active
        if button_active:
            self.settings.initialize_dynamic_settings()
            pygame.mouse.set_visible(False)
            #重置游戏信息
            self.status.reset_start()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ship()
            self.game_active = True

            self.bullets.empty()
            self.aliens.empty()

            #创建新舰队,并将飞船放到屏幕底边中央
            self.ship.center_ship()
            self._create_fleet()

        hard_button = self.hard_botton.rect.collidepoint(mouse_pos) and not self.game_active
        if hard_button:
            self.settings.speedup_scale = 2.0

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()