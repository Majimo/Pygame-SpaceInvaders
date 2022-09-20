import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed) -> None:
        super().__init__()
        self.image = pygame.image.load('assets/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x_constraint = constraint
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 600
        self.lasers = pygame.sprite.Group()
        
    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint
        
    def get_input(self):
        keys = pygame.key.get_pressed()
        
        # Move
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            
        # Shoot
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            
    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))
    
    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True
            
    def update(self) -> None:
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()