import pygame
import sys
from enum import Enum

# Constants
WIDTH, HEIGHT = 300, 300
CELL_SIZE = WIDTH // 3
LINE_WIDTH = 15
FONT_SIZE = 40
FPS = 10
EMPTY_CELL = ' '

class Player(Enum):
    X = 1
    O = 2

# Colors
WHITE = (255, 255, 255)
GRID_COLOR = (0, 0, 0)
PLAYER_X_COLOR = (255, 0, 0)
PLAYER_O_COLOR = (0, 0, 255)
RESULT_SCREEN_COLOR = (160, 32, 160)
RESULT_TEXT_COLOR = (255, 255, 255)

# Initialize pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Initialize the game board
board = [[EMPTY_CELL for _ in range(3)] for _ in range(3)]
current_player = Player.X
winner = None
draw = False

# Use Pygame's default font
font = pygame.font.Font(None, FONT_SIZE)

def draw_grid():
    """Draws the game grid."""
    for i in range(1, 3):
        pygame.draw.line(screen, GRID_COLOR, (CELL_SIZE * i, 0), (CELL_SIZE * i, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, GRID_COLOR, (0, CELL_SIZE * i), (WIDTH, CELL_SIZE * i), LINE_WIDTH)

def draw_xo(row, col):
    """Draws X or O on the specified cell."""
    center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)

    if board[row][col] == Player.X:
        pygame.draw.line(screen, PLAYER_X_COLOR, (col * CELL_SIZE, row * CELL_SIZE),
                         ((col + 1) * CELL_SIZE, (row + 1) * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, PLAYER_X_COLOR, (col * CELL_SIZE, (row + 1) * CELL_SIZE),
                         ((col + 1) * CELL_SIZE, row * CELL_SIZE), LINE_WIDTH)
    elif board[row][col] == Player.O:
        pygame.draw.circle(screen, PLAYER_O_COLOR, center, CELL_SIZE // 2 - LINE_WIDTH // 2, LINE_WIDTH)

def check_winner():
    """Checks for a winner and returns the winning player."""
    for row in board:
        if len(set(row)) == 1 and row[0] != EMPTY_CELL:
            return Player(row[0])
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != EMPTY_CELL:
            return Player(board[0][col])
    if board[0][0] == board[1][1] == board[2][2] != EMPTY_CELL:
        return Player(board[0][0])
    if board[0][2] == board[1][1] == board[2][0] != EMPTY_CELL:
        return Player(board[0][2])
    return None

def is_draw():
    """Checks if the game is a draw."""
    return all(cell != EMPTY_CELL for row in board for cell in row)

def display_result_screen(result):
    """Displays the result screen with the given message."""
    text = font.render(result, True, RESULT_TEXT_COLOR)
    background_rect = pygame.Rect((WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2),
                                  (text.get_width(), text.get_height()))
    pygame.draw.rect(screen, RESULT_SCREEN_COLOR, background_rect)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

def reset_game():
    """Resets the game state."""
    global board, current_player, winner
    board = [[EMPTY_CELL for _ in range(3)] for _ in range(3)]
    current_player = Player.X
    winner = None

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and winner is None and not is_draw():
            col = event.pos[0] // CELL_SIZE
            row = event.pos[1] // CELL_SIZE
            if board[row][col] == EMPTY_CELL:
                board[row][col] = current_player
                winner = check_winner()
                if winner is not None:
                    print(f"Player {winner.name} wins!")
                elif is_draw():
                    print("It's a draw!")
                else:
                    current_player = Player.O if current_player == Player.X else Player.X
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (winner is not None or is_draw()):
                # Reset the game
                reset_game()
            elif event.key == pygame.K_ESCAPE:
                # Quit the game when 'Esc' is pressed
                running = False

    screen.fill(WHITE)
    draw_grid()

    # Draw X and O based on the board
    for i in range(3):
        for j in range(3):
            draw_xo(i, j)

    if winner is not None or is_draw():
        display_result_screen(f"Player {winner.name} wins!" if winner else "It's a draw!")
        press_r_text = font.render("Press 'r' to play again", True, RESULT_TEXT_COLOR)
        background_rect = pygame.Rect((WIDTH // 2 - press_r_text.get_width() // 2, HEIGHT // 2 + press_r_text.get_height()),
                                      (press_r_text.get_width(), press_r_text.get_height()))
        pygame.draw.rect(screen, RESULT_SCREEN_COLOR, background_rect)
        screen.blit(press_r_text, (WIDTH // 2 - press_r_text.get_width() // 2, HEIGHT // 2 + press_r_text.get_height()))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
