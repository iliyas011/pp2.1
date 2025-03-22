import pygame


pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Краска")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


current_color = BLACK
brush_size = 5


drawing = False
mode = "brush"  
start_pos = None


canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)


buttons = {
    "brush": pygame.image.load("b.png"),
    "rect": pygame.image.load("rect.png"),
    "circle": pygame.image.load("c1.png"),
    "eraser": pygame.image.load("eraser.png"),
    "black": pygame.image.load("black.png"),
    "red": pygame.image.load("red.png"),
    "blue": pygame.image.load("blue.png"),
    "green": pygame.image.load("green.png")
}


button_positions = {
    "brush": (10, 10),
    "rect": (70, 10),
    "circle": (130, 10),
    "eraser": (190, 10),
    "black": (250, 10),
    "red": (310, 10),
    "blue": (370, 10),
    "green": (430, 10)
}


running = True
while running:
    screen.fill(WHITE) 
    screen.blit(canvas, (0, 0))  

    for key, pos in button_positions.items():
        screen.blit(buttons[key], pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

   
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            for key, pos in button_positions.items():
                button_rect = pygame.Rect(pos, (50, 50)) 
                if button_rect.collidepoint(x, y):
                    if key in ["brush", "rect", "circle", "eraser"]:
                        mode = key
                    elif key in ["black", "red", "blue", "green"]:
                        current_color = {"black": BLACK, "red": RED, "blue": BLUE, "green": GREEN}[key]
                    break  

        
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            if mode in ["rect", "circle"]:
                end_pos = event.pos
                width = end_pos[0] - start_pos[0]
                height = end_pos[1] - start_pos[1]
                if mode == "rect":
                    pygame.draw.rect(canvas, current_color, (start_pos[0], start_pos[1], width, height), 2)
                elif mode == "circle":
                    pygame.draw.ellipse(canvas, current_color, (start_pos[0], start_pos[1], width, height), 2)

    
        if event.type == pygame.MOUSEMOTION and drawing:
            if mode == "brush":
                pygame.draw.circle(canvas, current_color, event.pos, brush_size)
            elif mode == "eraser":
                pygame.draw.circle(canvas, WHITE, event.pos, brush_size)

    pygame.display.update()

pygame.quit()
