import pygame
import random
import os

pygame.init()

#so basically this used to be a snake game, but when you said I needed to do more, 
#I just made it into an rpg by building upon it 
#so thats why all the variables are for the snake game.

width, height = 600, 400
win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Sami Game')

black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)

block_size = 20

try:
    font = pygame.font.Font("PressStart2P-Regular.ttf", 16)
except FileNotFoundError:
    print("Pixel font not found! Falling back to default font.")
    font = pygame.font.SysFont(None, 24)

clock = pygame.time.Clock()

girl_sprite = pygame.image.load('girl.png')
girl_sprite = pygame.transform.scale(girl_sprite, (block_size, block_size))

def draw_snake(snake_list):
    for block in snake_list:
        win.blit(girl_sprite, (block[0], block[1]))

def show_message(msg, color):
    text = font.render(msg, True, color)
    win.blit(text, [width / 6, height / 3])

def play_cutscenes(level):
    for i in range(1, 6):
        image_path = f"cutscenes/cutscene{level}_{i}.png"
        if not os.path.exists(image_path):
            print(f"Missing cutscene: {image_path}")
            continue
        img = pygame.image.load(image_path)
        img = pygame.transform.scale(img, (width, height))

        waiting = True
        while waiting:
            win.blit(img, (0, 0))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

    if level == 7:
        show_ending()
        pygame.time.delay(3000)
        pygame.quit()
        quit()

def show_ending():
    win.fill(black)
    end_text = font.render("The End: Sami", True, white)
    win.blit(end_text, (width / 2 - end_text.get_width() / 2, height / 2))
    pygame.display.update()

def title_screen():
    showing = True
    while showing:
        win.fill(black)
        title_text = font.render("Sami: Collect energy to advance.", True, white)
        start_text = font.render("Click or Press Any Key to Start", True, white)
        win.blit(title_text, (width / 2 - title_text.get_width() / 2, height / 3))
        win.blit(start_text, (width / 2 - start_text.get_width() / 2, height / 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                showing = False

def game_loop():
    level = 1
    speed = 10
    apples_needed = 1

    x, y = width // 2, height // 2
    dx, dy = 0, 0

    snake = []
    snake_length = 1
    apples_eaten = 0

    food_x = round(random.randrange(0, width - block_size) / 20) * 20
    food_y = round(random.randrange(0, height - block_size) / 20) * 20

    game_close = False
    running = True

    while running:
        while game_close:
            win.fill(black)
            show_message("You died. Press Q or C", red)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return False
                    elif event.key == pygame.K_c:
                        dx, dy = 0, 0
                        snake = []
                        snake_length = 1
                        x, y = width // 2, height // 2
                        food_x = round(random.randrange(0, width - block_size) / 20) * 20
                        food_y = round(random.randrange(0, height - block_size) / 20) * 20
                        apples_eaten = 0
                        game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -block_size
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = block_size
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dy = -block_size
                    dx = 0
                elif event.key == pygame.K_DOWN and dy == 0:
                    dy = block_size
                    dx = 0

        x += dx
        y += dy

        if x < 0 or x >= width or y < 0 or y >= height:
            game_close = True

        win.fill(black)
        pygame.draw.rect(win, white, [food_x, food_y, block_size, block_size])

        snake_head = [x, y]
        snake.append(snake_head)
        if len(snake) > snake_length:
            del snake[0]

        for segment in snake[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake)
        score_text = font.render(f"Level: {level}  Energy: {apples_eaten}/{apples_needed}", True, white)
        win.blit(score_text, (10, 10))
        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block_size) / 20) * 20
            food_y = round(random.randrange(0, height - block_size) / 20) * 20
            snake_length += 1
            apples_eaten += 1

            if apples_eaten >= apples_needed:
                play_cutscenes(level)
                level += 1
                speed += 2
                apples_eaten = 0
                snake_length = 1
                snake = []
                x, y = width // 2, height // 2
                dx, dy = 0, 0
                food_x = round(random.randrange(0, width - block_size) / 20) * 20
                food_y = round(random.randrange(0, height - block_size) / 20) * 20

        clock.tick(speed)

title_screen()
while True:
    play = game_loop()
    if not play:
        break

pygame.quit()
quit()