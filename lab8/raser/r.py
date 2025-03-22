import pygame, sys
from pygame.locals import *
import random, time
import os




pygame.init()


FPS = 60
FramePerSec = pygame.time.Clock()


BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 562
SPEED = 5
SCORE = 0
count = 0


font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("road122.png")


DISPLAYSURF = pygame.display.set_mode((800,562))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Py2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)

      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
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
        
      
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)

class coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('money.png').convert_alpha()
        self.imsc = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.imsc.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), random.randint(100, SCREEN_HEIGHT-80))
        self.speed = 3
        
   
     
    def empty_space(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), random.randint(100, SCREEN_HEIGHT-80))
        while pygame.sprite.collide_rect(P1, COIN):
            self.rect.center = (random.randint(40, SCREEN_WIDTH-40), random.randint(100, SCREEN_HEIGHT-80))
        return self.rect.center
    
    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > SCREEN_HEIGHT:  
            self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0) 


      
P1 = Player()
E1 = Enemy()
COIN = coin()



enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)





INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)


coins = pygame.sprite.Group()
coins.add(COIN)

while True:
      
 
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.5      
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


    DISPLAYSURF.blit(background, (0,0))
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (670,10))
    coinss = font_small.render("Coins: " + str(count), True, BLACK)
    DISPLAYSURF.blit(coinss, (700,10))
    DISPLAYSURF.blit(COIN.imsc, COIN.rect)
    

    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)
        


    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(1)
                   
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))
          
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()    


    if pygame.sprite.spritecollideany(P1, coins):
        count += 1
        COIN.rect.center = COIN.empty_space()
        
    COIN.move()  
    pygame.display.update()
    FramePerSec.tick(FPS)