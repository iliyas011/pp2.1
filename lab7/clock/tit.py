import pygame
from datetime import datetime

pygame.init()
clock = pygame.time.Clock()


W, H = 800, 800
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("CLOCK")

WHITE = (255, 255, 255)
FPS = 60


bg = pygame.image.load("clock.png").convert_alpha()
minute = pygame.image.load("square_leftarm.png").convert_alpha() 
second = pygame.image.load("rightarm.png").convert_alpha()  


bg = pygame.transform.scale(bg, (650, 650))
minute = pygame.transform.scale(minute, (600, 600 ))  
second = pygame.transform.scale(second, (600, 600))  
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = minute
        self.image.set_colorkey(WHITE)                        
        self.rect = self.image.get_rect()
        self.rect.center = ( W / 2, H / 2)
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = second
        self.image.set_colorkey(WHITE)                        
        self.rect = self.image.get_rect()
        self.rect.center = ( W / 2, H / 2)


rect = bg.get_rect(center=(W // 2, H // 2))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    sc.fill(WHITE)
    sc.blit(bg, rect)

    time = datetime.now().time()

 
    sang = -(time.second * 7)
    rotated_second = pygame.transform.rotate(second, sang)
    sec_rect = rotated_second.get_rect(center=rect.center)
    sc.blit(rotated_second, sec_rect.topleft)


    mang = -(time.minute * 7 + time.second * 0.1)
    rotated_minute = pygame.transform.rotate(minute, mang)
    min_rect = rotated_minute.get_rect(center=rect.center)
    sc.blit(rotated_minute, min_rect.topleft)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
