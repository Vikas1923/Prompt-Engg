import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 5
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 5
CROSS_WIDTH = 5
OFFSET = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe vs AI")
screen.fill(WHITE)

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Player Scores
player_score = 0
ai_score = 0

# Font for displaying text
font = pygame.font.SysFont('Arial', 20)

# Draw grid
for row in range(1, BOARD_ROWS):
    pygame.draw.line(screen, BLACK, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
for col in range(1, BOARD_COLS):
    pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_xo():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, RED, (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET),
                                 ((col + 1) * SQUARE_SIZE - OFFSET, (row + 1) * SQUARE_SIZE - OFFSET), CROSS_WIDTH)
                pygame.draw.line(screen, RED, ((col + 1) * SQUARE_SIZE - OFFSET, row * SQUARE_SIZE + OFFSET),
                                 (col * SQUARE_SIZE + OFFSET, (row + 1) * SQUARE_SIZE - OFFSET), CROSS_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)

def check_winner(player):
    win_conditions = [
        [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],  # Rows
        [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],  # Columns
        [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]  # Diagonals
    ]
    return any(all(board[r][c] == player for r, c in condition) for condition in win_conditions)

def is_draw():
    return all(all(cell is not None for cell in row) for row in board)

def available_moves():
    return [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] is None]

def minimax(is_maximizing):
    if check_winner('O'):
        return 1
    if check_winner('X'):
        return -1
    if is_draw():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for r, c in available_moves():
            board[r][c] = 'O'
            score = minimax(False)
            board[r][c] = None
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = math.inf
        for r, c in available_moves():
            board[r][c] = 'X'
            score = minimax(True)
            board[r][c] = None
            best_score = min(best_score, score)
        return best_score

def best_ai_move():
    best_score = -math.inf
    best_move = None
    for r, c in available_moves():
        board[r][c] = 'O'
        score = minimax(False)
        board[r][c] = None
        if score > best_score:
            best_score = score
            best_move = (r, c)
    return best_move

def draw_score():
    score_text = font.render(f"Player: {player_score} | AI: {ai_score}", True, BLACK)
    screen.blit(score_text, (10, 10))

def draw_turn_message(turn):
    if turn:
        turn_text = font.render("Player's Turn", True, BLACK)
    else:
        turn_text = font.render("AI's Turn", True, BLACK)
    screen.blit(turn_text, (WIDTH // 2 - turn_text.get_width() // 2, HEIGHT - 30))

# Game loop
player_turn = True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
            x, y = event.pos
            row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
            if board[row][col] is None:
                board[row][col] = 'X'
                player_turn = False

    # AI move
    if not player_turn and not check_winner('X') and not is_draw():
        pygame.time.delay(500)  # Delay to make AI move realistic
        ai_move = best_ai_move()
        if ai_move:
            board[ai_move[0]][ai_move[1]] = 'O'
        player_turn = True

    screen.fill(WHITE)
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

    draw_xo()
    draw_score()
    draw_turn_message(player_turn)
    pygame.display.update()

    # Check for game over
    if check_winner('X'):
        print("You Win!")
        player_score += 1
        pygame.time.delay(2000)
        board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        player_turn = True
    elif check_winner('O'):
        print("AI Wins!")
        ai_score += 1
        pygame.time.delay(2000)
        board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        player_turn = True
    elif is_draw():
        print("It's a Draw!")
        pygame.time.delay(2000)
        board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        player_turn = True

pygame.quit()
sys.exit()
