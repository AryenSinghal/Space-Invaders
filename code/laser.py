import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, y_constraint):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill('white')
        self.rect = self.image.get_rect(center = pos)
        self.speed = speed
        self.y_constraint = y_constraint
    
    def movement(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > self.y_constraint:
            self.kill()
    
    def update(self):
        self.movement()