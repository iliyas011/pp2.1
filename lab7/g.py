import pygame
pygame.init()
clock=pygame.time.Clock()
W=600
H=600
sc=pygame.display.set_mode((W,H))
pygame.display.set_caption("CIRCLE")

WHITE=(255,255,255)
FPS=60


x=W//2
y=H//2
speed=20



while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x-=speed
                if x < 0:
                    x=0
            elif event.key == pygame.K_RIGHT:
                x+=speed
                if x > W:
                    x=W
            elif event.key == pygame.K_UP:
                y-=speed
                if y<0:
                    y=0
            elif event.key == pygame.K_DOWN:
                y+=speed
                if y > H:
                    y = H
    sc.fill(WHITE)
    pygame.draw.circle(sc, (0,255,255), (x,y), 25)
    pygame.display.update()
    

    clock.tick(FPS)