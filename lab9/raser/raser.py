import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()


RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 562
SPEED = 5
SCORE = 0
COIN_COUNT = 0
COINS_FOR_SPEEDUP = 5  

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("road122.png")
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Py2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player5.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
       
        self.coin_types = [
            ("money.png", 1, 0.7),  
            ("coins.png", 5, 0.3)      
        ]
        self.set_random_coin()
        self.speed = 3

    def set_random_coin(self):
      
        coin_choice = random.choices(self.coin_types, weights=[0.7, 0.3])[0]
        self.image = pygame.image.load(coin_choice[0]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), random.randint(100, SCREEN_HEIGHT-80))
        self.value = coin_choice[1]
       
    def move(self):
        self.rect.move_ip(0, 3)  
        if self.rect.top > SCREEN_HEIGHT:
            self.set_random_coin() 


P1 = Player()
E1 = Enemy()
COIN = Coin()


enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1)
coins = pygame.sprite.Group()
coins.add(COIN)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    DISPLAYSURF.blit(background, (0, 0))
    

    score_display = font_small.render(f"Score: {SCORE}", True, BLACK)
    coins_display = font_small.render(f"Coins: {COIN_COUNT}", True, BLACK)
    DISPLAYSURF.blit(score_display, (650, 10))
    DISPLAYSURF.blit(coins_display, (650, 40))


    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    COIN.move()
    DISPLAYSURF.blit(COIN.image, COIN.rect)
    

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(1)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (250, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

   
    if pygame.sprite.spritecollideany(P1, coins):
        COIN_COUNT += COIN.value 
        COIN.set_random_coin()  
    
 
    if COIN_COUNT % COINS_FOR_SPEEDUP == 0 and COIN_COUNT > 0:
        SPEED += 0.5
        COIN_COUNT += 1  

    pygame.display.update()
    FramePerSec.tick(FPS)
