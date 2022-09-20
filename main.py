from random import choice, randint
from re import X
import pygame, sys
from laser import Laser
from player import Player
from alien import Alien, Extra
import obstacle

class Game:
    def __init__(self) -> None:
        # Player
        player_sprite = Player((screen_width / 2,screen_height - 10), screen_width, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        
        # Health
        self.lives = 3
        self.lives_surf = pygame.image.load('assets/player.png').convert_alpha()
        self.lives_x_start_pos = screen_width - (self.lives_surf.get_size()[0] * 2 + 20)
        
        # Score
        self.score = 0
        self.font = pygame.font.Font('font/Pixeled.ttf', 20)
        
        # Obstacles
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_positions = [
            num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multi_obstacles(*self.obstacle_x_positions, x_start=screen_width / 15, y_start=480)
        
        # Aliens
        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8)
        self.alien_direction = 1
        self.alien_lasers = pygame.sprite.Group()
        
        # Extra
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400,600)
        
    def alien_setup(self, rows, cols, x_dist=60, y_dist=48, x_offset=70, y_offset=100):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_dist + x_offset
                y = row_index  * y_dist + y_offset
                
                if row_index == 0: alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_index <= 2: alien_sprite = Alien('green', x, y)
                else: alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)
    
    def alien_position_checkup(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)
                
    def alien_move_down(self, dist):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += dist
    
    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, screen_height)
            self.alien_lasers.add(laser_sprite)
    
    def collision_checks(self):
        # Player lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # Obstacle
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                    
                # Alien
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                
                # Extra
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 500
                    laser.kill()
                    
        # Alien lasers
        if self.alien_lasers:
            for laser in self.alien_lasers.sprites():
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()
                
        # Aliens
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)
                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()
    
    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = x_start + offset_x + col_index * self.block_size
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size, (241,79,80), x, y)
                    self.blocks.add(block)
                    
    def create_multi_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)
    
    def display_lives(self):
        for life in range(self.lives - 1):
            x = self.lives_x_start_pos + (life * (self.lives_surf.get_size()[0] + 10))
            screen.blit(self.lives_surf, (x,8))
    
    def display_score(self):
        self.score_surf = self.font.render(str(self.score), False, 'white')
        self.score_rect = self.score_surf.get_rect(topleft = (10,-10))
        screen.blit(self.score_surf, self.score_rect)
    
    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time == 0:
            self.extra.add(Extra(choice(['right', 'left']), screen_width))
            self.extra_spawn_time = randint(400,600)
    
    def run(self):
        self.player.update()        
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        
        self.aliens.update(self.alien_direction)
        self.alien_position_checkup()
        self.alien_lasers.update()        
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        
        self.extra_alien_timer()
        self.extra.update()        
        self.extra.draw(screen)
        
        self.blocks.draw(screen)
        
        self.collision_checks()        
        self.display_lives()
        self.display_score()

class CRT:
    def __init__(self) -> None:
        self.tv = pygame.image.load('assets/tv.png').convert_alpha()
        # Responsive effect
        self.tv = pygame.transform.scale(self.tv, (screen_width, screen_height))
        
    def create_crt_lines(self):
        line_height = 3
        line_amount = int(screen_height / line_height)
        for line in range(line_amount):
            y_pos = line * line_height
            pygame.draw.line(self.tv, 'black', (0, y_pos), (screen_width, y_pos), 1)
        
    def draw(self):
        self.tv.set_alpha(randint(75,90))
        self.create_crt_lines()
        screen.blit(self.tv, (0,0))

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()
    crt = CRT()
    
    ALIENLASER = pygame. USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()
        
        screen.fill((30,30,30))
        game.run()
        crt.draw()
        
        pygame.display.flip()
        clock.tick(60)