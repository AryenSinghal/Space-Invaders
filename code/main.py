import pygame, sys
from laser import Laser
from player import Player
import obstacle
from alien import Alien, Extra
from random import choice, randint

class Game():
    def __init__(self):
        #player setup
        player_sprite = Player((WIDTH/2,HEIGHT), WIDTH, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)
        
        #obstacle setup
        obstacle.init(WIDTH, 6, 4)
        self.blocks = obstacle.multiple_obstacles(x_start=40, y_start=480)

        #alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_setup(rows=6, cols=8)
        self.direction = 1
        self.alien_lasers = pygame.sprite.Group()

        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(400,800)

        #health setup
        self.lives = 3
        self.life_surf = pygame.image.load('graphics/player.png').convert_alpha()
        self.life_x_start = WIDTH - (self.life_surf.get_size()[0] * 2 + 20)
        
        #score setup
        self.score = 0
        self.font = pygame.font.Font('font/Pixeled.ttf', 20)

        #audio
        music = pygame.mixer.Sound('audio/music.wav')
        music.set_volume(0.2)
        music.play(loops=-1)

        self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
        self.laser_sound.set_volume(0.2)
        self.explosion = pygame.mixer.Sound('audio/explosion.wav')
        self.explosion.set_volume(0.3)

    def alien_setup(self, rows, cols, x_dist=60, y_dist=48, x_offset=70, y_offset=100):
        for row_ind in range(rows):
            for col_ind in range(cols):
                x = (col_ind * x_dist) + x_offset
                y = (row_ind * y_dist) + y_offset
                if row_ind == 0: alien_sprite = Alien('yellow', x, y)
                elif 1 <= row_ind <= 2: alien_sprite = Alien('green', x, y)
                else: alien_sprite = Alien('red', x, y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        for alien in self.aliens.sprites():
            if alien.rect.right >= WIDTH:
                self.direction = -1
                for alien in self.aliens.sprites():
                    alien.rect.y += 2
            elif alien.rect.left <= 0:
                self.direction = 1
                for alien in self.aliens.sprites():
                    alien.rect.y += 2

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, 6, HEIGHT)
            self.alien_lasers.add(laser_sprite)
            self.laser_sound.play()

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right','left']), WIDTH))
            self.extra_spawn_time = randint(400,800)

    def collision_checks(self):
        #player laser
        for laser in self.player.sprite.lasers:
            if pygame.sprite.spritecollide(laser, self.blocks, True):
                laser.kill()
            aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
            for alien in aliens_hit:
                laser.kill()
                self.explosion.play()
                self.score += alien.value
            if pygame.sprite.spritecollide(laser, self.extra, True):
                laser.kill()
                self.explosion.play()
                self.score += 500
        
        #alien lasers
        for laser in self.alien_lasers:
            if pygame.sprite.spritecollide(laser, self.blocks, True):
                laser.kill()
            if pygame.sprite.spritecollide(laser, self.player, False):
                laser.kill()
                self.explosion.play()
                self.lives -= 1
                if self.lives <= 0:
                    pygame.quit()
                    sys.exit()
        
        #aliens
        for alien in self.aliens:
            pygame.sprite.spritecollide(alien, self.blocks, True)
            if pygame.sprite.spritecollide(alien, self.player, False):
                pygame.quit()
                sys.exit()
    
    def display_lives(self):
        for life in range(self.lives - 1):
            x = self.life_x_start + (life * (self.life_surf.get_size()[0] + 10))
            screen.blit(self.life_surf, (x,8))

    def display_score(self):
        self.score_surf = self.font.render(f'Score: {self.score}', False, 'white')
        self.score_rect = self.score_surf.get_rect(topleft=(10,-10))
        screen.blit(self.score_surf, self.score_rect)

    def victory_message(self):
        if not self.aliens.sprites():
            victory_surf = self.font.render('YOU WON', False, 'white')
            victory_rect = victory_surf.get_rect(center=(WIDTH/2, HEIGHT/2))
            screen.blit(victory_surf, victory_rect)

    def run(self):
        self.player.update()
        self.aliens.update(self.direction)
        self.alien_position_checker()
        self.alien_lasers.update()
        self.extra_alien_timer()
        self.extra.update()
        self.collision_checks()

        self.player.sprite.lasers.draw(screen)
        self.alien_lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.extra.draw(screen)

        self.display_lives()
        self.display_score()
        self.victory_message()

class CRT():
    def __init__(self):
        self.tv = pygame.image.load('graphics/tv.png').convert_alpha()
        self.tv = pygame.transform.scale(self.tv, (WIDTH, HEIGHT))
    
    def create_lines(self):
        line_height = 3
        line_amount = int(HEIGHT/line_height)
        for line in range(line_amount):
            y = line*line_height
            pygame.draw.line(self.tv, 'black', (0,y), (WIDTH,y))

    def draw(self):
        self.create_lines()
        self.tv.set_alpha(randint(75,90))
        screen.blit(self.tv, (0,0))


if __name__ == '__main__':
    pygame.init()
    WIDTH, HEIGHT = 600, 600
    pygame.display.set_caption('Space Invaders')
    pygame.display.set_icon(pygame.image.load('graphics/red.png'))
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    game = Game()
    crt = CRT()

    ALIENLASER = pygame.USEREVENT + 1
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