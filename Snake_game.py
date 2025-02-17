import pygame
import random
import time

# Initialize pygame
pygame.init()

# Set up the display
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Enhanced Graphics")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 50)
LIGHT_BLUE = (0, 0, 100)

# Game clock
clock = pygame.time.Clock()
FPS = 15

# Font for rendering text
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Function to display the score
def your_score(score):
    value = score_font.render("Your Score: " + str(score), True, WHITE)
    win.blit(value, [0, 0])

# Function to draw the snake with smooth animations
def draw_snake(snake_body):
    for i, segment in enumerate(snake_body):
        # Head is larger and colored differently for better visibility
        color = GREEN if i != 0 else YELLOW
        pygame.draw.rect(win, color, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE], border_radius=5)

# Function to draw the gradient background
def draw_gradient():
    for i in range(HEIGHT):
        color = (int(LIGHT_BLUE[0] * (i / HEIGHT) + DARK_BLUE[0] * (1 - i / HEIGHT)),
                 int(LIGHT_BLUE[1] * (i / HEIGHT) + DARK_BLUE[1] * (1 - i / HEIGHT)),
                 int(LIGHT_BLUE[2] * (i / HEIGHT) + DARK_BLUE[2] * (1 - i / HEIGHT)))
        pygame.draw.line(win, color, (0, i), (WIDTH, i))

# Function to display the message
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    win.blit(mesg, [WIDTH / 6, HEIGHT / 3])

# Function to handle the game loop
def gameLoop():
    game_over = False
    game_close = False

    # Snake starting position and size
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0
    snake_body = []
    length_of_snake = 1

    # Food position
    foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    # Game loop
    while not game_over:

        while game_close:
            win.fill(RED)  # Game over screen color
            message("You Lost! Press Q-Quit or C-Play Again", WHITE)
            your_score(length_of_snake - 1)
            pygame.display.update()

            # Handle key presses to restart or quit
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        draw_gradient()  # Draw the gradient background

        # Draw food and snake
        draw_snake(snake_body)
        pygame.draw.rect(win, YELLOW, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE], border_radius=5)

        # Snake growing mechanism
        snake_head_position = []
        snake_head_position.append(x1)
        snake_head_position.append(y1)
        snake_body.append(snake_head_position)
        if len(snake_body) > length_of_snake:
            del snake_body[0]

        for segment in snake_body[:-1]:
            if segment == snake_head_position:
                game_close = True

        # Display score
        your_score(length_of_snake - 1)

        # Update screen
        pygame.display.update()

        # Check if snake eats food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            foody = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            length_of_snake += 1

        clock.tick(FPS)

    pygame.quit()
    quit()

gameLoop()
