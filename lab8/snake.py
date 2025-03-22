import pygame 
import random
pygame.init()
s_speed= 10
s_color = (0 , 255 , 0)
f_color= (255 ,255 ,255 )
bg_color = (0 , 0 , 0)

W = 600 
H = 400 
sc=pygame.display.set_mode((W,H))
fps = pygame.time.Clock()
s_p = [100, 50]
s_b = [[100 ,50],
       [90 , 50],
       [80, 50],
       [70, 50]]
f_p = [random.randrange(1, (W//10)) *10 , 
       random.randrange(1 , (H//10)) * 10]

f_s = True 
direction = 'RIGHT'
change_to = direction

point = 0 
font = pygame.font.Font(None, 36)
def show_point():
    text = font.render(f"Очки: {point}", True, (255, 0, 0))
    sc.blit(text, (10, 10))
while True:
    
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
    direction = change_to
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
        
    if direction == 'UP':
        s_p[1] -= 10
    elif direction == 'DOWN':
        s_p[1] += 10
    elif direction == 'LEFT':
        s_p[0] -= 10
    elif direction == 'RIGHT':
        s_p[0] += 10
        
    s_b.insert(0, list(s_p))
    if s_p == f_p:
        point += 1
        f_p = [random.randrange(1, (W // 10)) * 10, random.randrange(1, (H // 10)) * 10]
    else:
        s_b.pop()
    if s_p[0] < 0 or s_p[0] >= W or s_p[1] < 0 or s_p[1] >= H:
        running = False
    for block in s_b[1:]:
        if s_p == block:
            running = False
    sc.fill(bg_color)
    for pos in s_b:
        pygame.draw.rect(sc, s_color, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(sc, f_color, pygame.Rect(f_p[0], f_p[1], 10, 10))
    
    show_point()
    pygame.display.flip()
    fps.tick(s_speed)

pygame.quit()