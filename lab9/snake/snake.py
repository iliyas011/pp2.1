import pygame
import random

pygame.init()


s_speed = 10  
s_color = (0, 255, 0)
bg_color = (0, 0, 0)
food_colors = {"normal": (255, 255, 255), "rare": (255, 0, 0)}

W = 600
H = 400
sc = pygame.display.set_mode((W, H))
fps = pygame.time.Clock()


s_p = [100, 50]  
s_b = [[100, 50], [90, 50], [80, 50], [70, 50]] 


food_types = [
    ("normal", 1, 15),  
    ("rare", 3, 10)
]

current_food = None
food_timer = 0

direction = 'RIGHT'
change_to = direction
point = 0

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)


def spawn_food():
    global current_food, food_timer
    food_type = random.choices(food_types, weights=[0.8, 0.2])[0]  
    f_p = [random.randrange(1, (W // 10)) * 10, random.randrange(1, (H // 10)) * 10]
    current_food = {"pos": f_p, "type": food_type[0], "points": food_type[1], "lifetime": food_type[2]}
    food_timer = pygame.time.get_ticks()

def show_point():
    text = font.render(f"Очки: {point}", True, (255, 0, 0))
    sc.blit(text, (10, 10))

def game_over():
    sc.fill((0, 0, 0)) 
    text = big_font.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Ваш счет: {point}", True, (255, 255, 255))
    sc.blit(text, (W // 2 - 150, H // 2 - 50))
    sc.blit(score_text, (W // 2 - 70, H // 2 + 10))
    pygame.display.flip()
    pygame.time.delay(2000)
    pygame.quit()
    exit()


spawn_food()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'
    direction = change_to

    if change_to == 'UP':
        s_p[1] -= 10
    elif change_to == 'DOWN':
        s_p[1] += 10
    elif change_to == 'LEFT':
        s_p[0] -= 10
    elif change_to == 'RIGHT':
        s_p[0] += 10

  
    if s_p[0] < 0 or s_p[0] >= W or s_p[1] < 0 or s_p[1] >= H:
        game_over()

 
    if s_p in s_b[1:]:
        game_over()

    s_b.insert(0, list(s_p))


    if s_p == current_food["pos"]:
        point += current_food["points"]  
        spawn_food() 
    else:
        s_b.pop() 

    
    if pygame.time.get_ticks() - food_timer > current_food["lifetime"] * 1000:
        spawn_food()

  
    sc.fill(bg_color)
    for pos in s_b:
        pygame.draw.rect(sc, s_color, pygame.Rect(pos[0], pos[1], 10, 10))


    pygame.draw.rect(sc, food_colors[current_food["type"]], pygame.Rect(current_food["pos"][0], current_food["pos"][1], 10, 10))

    
    show_point()

    pygame.display.flip()
    fps.tick(s_speed)

pygame.quit()
