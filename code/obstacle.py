import pygame

class Block(pygame.sprite.Sprite):
    def __init__(self, size, color, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x,y))

shape = (
    '  xxxxxxx',
    ' xxxxxxxxx',
    'xxxxxxxxxxx',
    'xxxxxxxxxxx',
    'xxx     xxx',
    'xx       xx'
)

#obstacle setup
def init(screen_width, block_size, obstacle_amount):
    global size, blocks, offsets
    size = block_size
    offsets = [num*(screen_width/obstacle_amount) for num in range(obstacle_amount)]
    blocks = pygame.sprite.Group()
    
def create_obstacle(x_start, y_start, x_offset):
    for row_ind, row in enumerate(shape):
        for col_ind, col in enumerate(row):
            if col == 'x':
                x = x_start + (col_ind * size) + x_offset
                y = y_start + (row_ind * size)
                block = Block(size, (241,79,80), x, y)
                blocks.add(block)
    
def multiple_obstacles(x_start, y_start):
    for x_offset in offsets:
        create_obstacle(x_start, y_start, x_offset)
    return blocks