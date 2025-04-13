import pygame
import random
import psycopg2
import sys
from datetime import datetime
import data

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')


WHITE    = (255, 255, 255)
GREEN    = (0, 255, 0)
RED      = (255, 0, 0)
BLACK    = (0, 0, 0)
DARK_RED = (139, 0, 0)
BLUE     = (0, 0, 255)
PURPLE   = (128, 0, 128)

UP    = (0, -1)
DOWN  = (0, 1)
LEFT  = (-1, 0)
RIGHT = (1, 0)


def connect():
    return psycopg2.connect(
        host="localhost",
        database="Lab10",
        user="postgres",
        password=data.PASSWORD
    )

def init_db():
    con = connect()
    cur = con.cursor()
  
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS user_scores (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            score INTEGER,
            level INTEGER,
            saved_at TIMESTAMP
        )
    ''')
    con.commit()
    cur.close()
    con.close()

def get_or_create_user(username):
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT id FROM users WHERE username=%s", (username,))
    user = cur.fetchone()
    if user:
        user_id = user[0]
        cur.execute("SELECT MAX(level) FROM user_scores WHERE user_id=%s", (user_id,))
        res = cur.fetchone()[0]
        level = res if res is not None else 1
        print(f"Пользователь '{username}' найден. Текущий уровень: {level}")
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        con.commit()
        level = 1
        print(f"Новый пользователь '{username}' создан с уровнем: {level}")
    cur.close()
    con.close()
    return {'id': user_id, 'username': username, 'level': level}

def update_user_level(user_id, new_level, score=0):
    con = connect()
    cur = con.cursor()
    saved_at = datetime.now()
    cur.execute("INSERT INTO user_scores (user_id, score, level, saved_at) VALUES (%s, %s, %s, %s)",
                (user_id, score, new_level, saved_at))
    con.commit()
    cur.close()
    con.close()
    print(f"Новый уровень {new_level} сохранён для пользователя {user_id}.")

def save_score(user_id, score, level):
    con = connect()
    cur = con.cursor()
    saved_at = datetime.now()
    cur.execute("INSERT INTO user_scores (user_id, score, level, saved_at) VALUES (%s, %s, %s, %s)",
                (user_id, score, level, saved_at))
    con.commit()
    cur.close()
    con.close()
    print("Состояние игры сохранено в базу данных.")

def draw_text(surface, text, x, y, size=36, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def get_username():
    """
    Экран ввода имени пользователя через окно pygame.
    Пользователь вводит имя, которое отображается на экране, и подтверждает Enter.
    """
    input_active = True
    username = ""
    clock = pygame.time.Clock()

    while input_active:
        screen.fill(BLACK)
        draw_text(screen, "Введите ваше имя пользователя:", 100, 200, 36, WHITE)
        draw_text(screen, username, 100, 250, 36, WHITE)
        draw_text(screen, "Нажмите Enter для подтверждения", 100, 300, 24, WHITE)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if username.strip() != "":
                        input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
        clock.tick(30)
    return username.strip()


class Wall:
    def __init__(self, rect):
        self.rect = rect
        self.color = BLUE

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def collides_with(self, pos):
        snake_rect = pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
        return self.rect.colliderect(snake_rect)


class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.alive = True

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        if not self.alive:
            return

        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = [head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE]

        if new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT:
            self.alive = False
            return

        new_head = tuple(new_head)
        if new_head in self.positions:
            self.alive = False
            return

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        self.__init__()

    def draw(self, surface):
        for segment in self.positions:
            pygame.draw.rect(surface, self.color, pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, WHITE, pygame.Rect(segment[0], segment[1], GRID_SIZE, GRID_SIZE), 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause_game()
                elif event.key == pygame.K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT


class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position([], is_time_related=False, walls=[])
        self.is_time_need = False
        self.spawn_time = None
        self.weight = random.randint(1, 3)

    def randomize_position(self, snake_positions, is_time_related=False, walls=None):
        if walls is None:
            walls = []
        size = int(GRID_SIZE * 1.5) if is_time_related else GRID_SIZE
        while True:
            new_position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                            random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if new_position in snake_positions:
                continue
            food_rect = pygame.Rect(new_position[0] - (size - GRID_SIZE) // 2,
                                    new_position[1] - (size - GRID_SIZE) // 2,
                                    size, size)
            if any(wall.rect.colliderect(food_rect) for wall in walls):
                continue
            self.position = new_position
            if is_time_related:
                self.spawn_time = pygame.time.get_ticks()
                self.is_time_need = True
                self.weight = 5
            else:
                self.is_time_need = False
                self.weight = random.randint(1, 3)
            break

    def is_expired(self):
        return pygame.time.get_ticks() - self.spawn_time > 15000

    def collides_with(self, position):
        size = int(GRID_SIZE * 1.5) if self.is_time_need else GRID_SIZE
        x = self.position[0] - (size - GRID_SIZE) // 2
        y = self.position[1] - (size - GRID_SIZE) // 2
        food_rect = pygame.Rect(x, y, size, size)
        snake_rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
        return food_rect.colliderect(snake_rect)

    def draw(self, surface):
        size = int(GRID_SIZE * 1.5) if self.is_time_need else GRID_SIZE
        x = self.position[0] - (size - GRID_SIZE) // 2
        y = self.position[1] - (size - GRID_SIZE) // 2
        pygame.draw.rect(surface, self.color, pygame.Rect(x, y, size, size))
        pygame.draw.rect(surface, WHITE, pygame.Rect(x, y, size, size), 1)

def pause_game():
    global current_user, score, current_level
    save_score(current_user['id'], score, current_level)
    paused = True
    draw_text(screen, "ПАУЗА. Нажмите R для продолжения.", SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2, 36, WHITE)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    paused = False

def congrat_screen(new_level):
    screen.fill(PURPLE)
    draw_text(screen, f"Поздравляем! Вы перешли на уровень {new_level}!", 80, SCREEN_HEIGHT // 2 - 50, 40, WHITE)
    draw_text(screen, "Нажмите ПРОБЕЛ для продолжения или ESC для выхода", 80, SCREEN_HEIGHT // 2 + 10, 28, WHITE)
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def create_walls(level):
    walls = []
    if level == 1:
        return walls
    if level >= 2:
        walls.append(Wall(pygame.Rect(200, 150, 400, GRID_SIZE)))
        walls.append(Wall(pygame.Rect(200, 450, 400, GRID_SIZE)))
    if level >= 3:
        walls.append(Wall(pygame.Rect(100, 300, GRID_SIZE, 200)))
        walls.append(Wall(pygame.Rect(600, 100, GRID_SIZE, 200)))
    return walls

def game_over_screen(score):
    if current_level > current_user['level']:
        update_user_level(current_user['id'], current_level, score)
        current_user['level'] = current_level

    screen.fill(DARK_RED)
    draw_text(screen, "ВЫ УМЕРЛИ!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 50, WHITE)
    draw_text(screen, f"Ваш счет: {score}", SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 40, WHITE)
    draw_text(screen, "Пробел – рестарт, ESC – выход", SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 50, 30, WHITE)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    global score, current_level
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food()
    score = 0
    adding = 0
    current_level = current_user['level']
    walls = create_walls(current_level)
    level_threshold = 20 * (2 ** (current_level - 1))

    while snake.alive:
        screen.fill(BLACK)
        snake.handle_keys()
        snake.move()

        for wall in walls:
            if wall.collides_with(snake.get_head_position()):
                snake.alive = False

        if food.collides_with(snake.get_head_position()):
            snake.length += food.weight
            score += food.weight
            adding += food.weight
            if random.randint(1, 5) % 3 == 0:
                food.randomize_position(snake.positions, is_time_related=True, walls=walls)
            else:
                food.randomize_position(snake.positions, is_time_related=False, walls=walls)
            if adding >= level_threshold:
                current_level += 1
                update_user_level(current_user['id'], current_level, score)
                current_user['level'] = current_level
                congrat_screen(current_level)
                snake = Snake()
                adding = 0
                walls = create_walls(current_level)
                level_threshold = 20 * (2 ** (current_level - 1))

        if food.is_time_need:
            if food.is_expired():
                food.randomize_position(snake.positions, is_time_related=False, walls=walls)
            time_left = max(0, 15 - (pygame.time.get_ticks() - food.spawn_time) // 1000)
            draw_text(screen, f"Food Timer: {time_left}s", SCREEN_WIDTH - 200, 40)
            food.draw(screen)
        else:
            food.draw(screen)

        snake.draw(screen)
        for wall in walls:
            wall.draw(screen)

        draw_text(screen, f"Score: {score}", 10, 10)
        draw_text(screen, f"Level: {current_level}", 10, 40)
        pygame.display.update()
        clock.tick(8 + current_level)

    game_over_screen(score)

if __name__ == '__main__':
    init_db()
    username = get_username()
    current_user = get_or_create_user(username)

    while True:
        main()