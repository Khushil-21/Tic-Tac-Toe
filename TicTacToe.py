import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1100, 600
LEFT_SECTION_WIDTH = 500
GAME_AREA_WIDTH = 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = GAME_AREA_WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LEFT_SECTION_COLOR = (255, 255, 255)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (52, 152, 219)
BUTTON_HOVER_COLOR = (41, 128, 185)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Board
board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Function to draw the game board lines
def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (LEFT_SECTION_WIDTH, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (LEFT_SECTION_WIDTH, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (LEFT_SECTION_WIDTH + SQUARE_SIZE, 0), (LEFT_SECTION_WIDTH + SQUARE_SIZE, GAME_AREA_WIDTH), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (LEFT_SECTION_WIDTH + 2 * SQUARE_SIZE, 0), (LEFT_SECTION_WIDTH + 2 * SQUARE_SIZE, GAME_AREA_WIDTH), LINE_WIDTH)

# Function to draw X and O on the board
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                center = (int((col * SQUARE_SIZE) + SQUARE_SIZE // 2 + LEFT_SECTION_WIDTH), int(row * SQUARE_SIZE + SQUARE_SIZE // 2))
                pygame.draw.circle(screen, CIRCLE_COLOR, center, CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                start_pos1 = (col * SQUARE_SIZE + SPACE + LEFT_SECTION_WIDTH, row * SQUARE_SIZE + SPACE)
                end_pos1 = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE + LEFT_SECTION_WIDTH, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                start_pos2 = (col * SQUARE_SIZE + SPACE + LEFT_SECTION_WIDTH, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end_pos2 = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE + LEFT_SECTION_WIDTH, row * SQUARE_SIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_pos1, end_pos1, CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, start_pos2, end_pos2, CROSS_WIDTH)

# Function to mark a square on the board with a player's symbol
def mark_square(row, col, player):
    board[row][col] = player

# Function to check if a square is available (empty)
def available_square(row, col):
    return board[row][col] == ''

# Function to check if the board is full
def is_board_full():
    return all(all(cell != '' for cell in row) for row in board)

# Function to check if a player has won
def check_win(player):
    # Check horizontal, vertical, and diagonal win conditions
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True, [(i, 0), (i, 1), (i, 2)]
        if all(board[j][i] == player for j in range(3)):
            return True, [(0, i), (1, i), (2, i)]
    if all(board[i][i] == player for i in range(3)):
        return True, [(0, 0), (1, 1), (2, 2)]
    if all(board[i][2-i] == player for i in range(3)):
        return True, [(0, 2), (1, 1), (2, 0)]
    return False, []

# Improved minimax algorithm with alpha-beta pruning
def minimax(board, depth, alpha, beta, is_maximizing):
    if check_win('O')[0]:
        return 1
    if check_win('X')[0]:
        return -1
    if is_board_full():
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == '':
                    board[row][col] = 'O'
                    score = minimax(board, depth + 1, alpha, beta, False)
                    board[row][col] = ''
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == '':
                    board[row][col] = 'X'
                    score = minimax(board, depth + 1, alpha, beta, True)
                    board[row][col] = ''
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score

# Function to get the best move for the AI
def get_best_move():
    best_score = -math.inf
    best_move = None
    alpha = -math.inf
    beta = math.inf
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == '':
                board[row][col] = 'O'
                score = minimax(board, 0, alpha, beta, False)
                board[row][col] = ''
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    return best_move

# Function to reset the game
def reset_game():
    global board, game_over, player, winner
    board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    game_over = False
    player = 'X'
    winner = None

# Function to draw the game status (title, turn, rules)
def draw_status():
    # Game title
    title_text = font.render("Tic Tac Toe", True, TEXT_COLOR)
    screen.blit(title_text, (20, 20))

    # Current turn
    turn_text = font.render(f"Turn: {'Player' if player == 'X' else 'Computer'}", True, TEXT_COLOR)
    screen.blit(turn_text, (20, 60))

    # Rules
    rules = [
        "Rules:",
        "1. X is Player, O is Computer",
        "2. Players take turns marking empty squares",
        "3. First to get 3 in a row wins",
        "4. If all squares are filled with no winner, it's a draw"
    ]
    for i, rule in enumerate(rules):
        rule_text = small_font.render(rule, True, TEXT_COLOR)
        screen.blit(rule_text, (20, 120 + i * 30))

# Function to draw a button
def draw_button(text, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, (x, y, width, height))

    button_text = font.render(text, True, TEXT_COLOR)
    text_rect = button_text.get_rect(center=(x + width/2, y + height/2))
    screen.blit(button_text, text_rect)

# Function to draw the winner text
def draw_winner(winner):
    if winner == 'Draw':
        winner_text = font.render("It's a Draw!", True, TEXT_COLOR)
    else:
        winner_text = font.render(f"{'Player' if winner == 'X' else 'Computer'} Wins!", True, TEXT_COLOR)
    screen.blit(winner_text, (20, HEIGHT - 50))

# Function to draw the winning line
def draw_winning_line(win_line):
    start_pos = (win_line[0][1] * SQUARE_SIZE + SQUARE_SIZE // 2 + LEFT_SECTION_WIDTH,
                 win_line[0][0] * SQUARE_SIZE + SQUARE_SIZE // 2)
    end_pos = (win_line[2][1] * SQUARE_SIZE + SQUARE_SIZE // 2 + LEFT_SECTION_WIDTH,
               win_line[2][0] * SQUARE_SIZE + SQUARE_SIZE // 2)
    pygame.draw.line(screen, CROSS_COLOR, start_pos, end_pos, LINE_WIDTH)

# Main game loop
player = 'X'
game_over = False
winner = None
win_line = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] - LEFT_SECTION_WIDTH
            mouseY = event.pos[1]
            
            if 0 <= mouseX < GAME_AREA_WIDTH and 0 <= mouseY < GAME_AREA_WIDTH:
                clicked_row = int(mouseY // SQUARE_SIZE)
                clicked_col = int(mouseX // SQUARE_SIZE)
                
                if available_square(clicked_row, clicked_col):
                    mark_square(clicked_row, clicked_col, player)
                    game_won, win_line = check_win(player)
                    if game_won:
                        winner = player
                        game_over = True
                    elif is_board_full():
                        winner = 'Draw'
                        game_over = True
                    player = 'O' if player == 'X' else 'X'
                    
                    # AI move
                    if not game_over and player == 'O':
                        ai_move = get_best_move()
                        if ai_move:
                            ai_row, ai_col = ai_move
                            mark_square(ai_row, ai_col, 'O')
                            game_won, win_line = check_win('O')
                            if game_won:
                                winner = 'O'
                                game_over = True
                            elif is_board_full():
                                winner = 'Draw'
                                game_over = True
                            player = 'X'
    
    # Draw the game board
    screen.fill(LEFT_SECTION_COLOR, (0, 0, LEFT_SECTION_WIDTH, HEIGHT))
    screen.fill(BG_COLOR, (LEFT_SECTION_WIDTH, 0, GAME_AREA_WIDTH, HEIGHT))
    draw_lines()
    draw_figures()
    draw_status()
    draw_button("New Game", 20, HEIGHT - 100, 150, 50, reset_game)
    
    if game_over:
        draw_winner(winner)
        if win_line:
            draw_winning_line(win_line)
    
    pygame.display.update()

# Execution flow:
# 1. Initialize Pygame and set up the game window
# 2. Define constants, colors, and create the game board
# 3. Enter the main game loop:
#    a. Handle events (quit, mouse clicks)
#    b. If a valid move is made:
#       - Mark the square
#       - Check for a win or draw
#       - Switch players
#       - If it's the AI's turn, make a move using minimax with alpha-beta pruning
#    c. Update the display:
#       - Draw the left section (white) with game details and buttons
#       - Draw the right section (colored) with the game board
#       - If the game is over, display the winner and winning line
# 4. Repeat the loop until the game is quit
#
# Features:
# - Improved UI with separate left (white) and right (colored) sections
# - Player vs AI gameplay
# - Enhanced minimax algorithm with alpha-beta pruning for faster AI decisions
# - Interactive GUI with Pygame
# - Game status display (current turn, rules) in the left section
# - New Game button to reset the game
# - Win detection and display
# - Draw detection