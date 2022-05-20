import pygame
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load('graphics/player.png')
        self.rect = self.image.get_rect(midbottom = pos)
        self.x_constraint = constraint
        self.speed = speed
        self.laser_ready = True
        self.laser_time = 0
        self.recharge_time = 600
        self.lasers = pygame.sprite.Group()
        
        self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
        self.laser_sound.set_volume(0.2)
    
    def user_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        
        if keys[pygame.K_SPACE] and self.laser_ready:
            self.lasers.add(Laser(self.rect.center, -8, self.rect.bottom))
            self.laser_ready = False
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()
    
    def laser_recharge(self):
        if self.laser_ready == False:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.recharge_time:
                self.laser_ready = True

    def constraints(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.x_constraint:
            self.rect.right = self.x_constraint

    def update(self):
        self.user_input()
        self.constraints()
        self.laser_recharge()
        self.lasers.update()