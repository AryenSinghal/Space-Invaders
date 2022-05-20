import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        file_path = f'graphics/{color}.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))
        self.value = {'red': 100, 'green': 200, 'yellow': 300}[color]

    def update(self, direction):
        self.rect.x += direction

class Extra(pygame.sprite.Sprite):
    def __init__(self, side, screen_width):
        super().__init__()
        self.width = screen_width
        self.image = pygame.image.load('graphics/extra.png').convert_alpha()
        if side == 'right':
            self.rect = self.image.get_rect(topleft=(self.width,80))
            self.speed = -3
        else:
            self.rect = self.image.get_rect(topright=(0,80))
            self.speed = 3
    
    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > self.width:
            self.kill()