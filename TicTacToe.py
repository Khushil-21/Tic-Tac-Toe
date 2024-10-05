import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
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
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (52, 152, 219)
BUTTON_HOVER_COLOR = (41, 128, 185)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Board
board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (WIDTH - GAME_AREA_WIDTH, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH - GAME_AREA_WIDTH, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (WIDTH - GAME_AREA_WIDTH + SQUARE_SIZE, 0), (WIDTH - GAME_AREA_WIDTH + SQUARE_SIZE, GAME_AREA_WIDTH), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (WIDTH - GAME_AREA_WIDTH + 2 * SQUARE_SIZE, 0), (WIDTH - GAME_AREA_WIDTH + 2 * SQUARE_SIZE, GAME_AREA_WIDTH), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int((col * SQUARE_SIZE) + SQUARE_SIZE // 2 + (WIDTH - GAME_AREA_WIDTH)), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE + (WIDTH - GAME_AREA_WIDTH), row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE + (WIDTH - GAME_AREA_WIDTH), row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE + (WIDTH - GAME_AREA_WIDTH), row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE + (WIDTH - GAME_AREA_WIDTH), row * SQUARE_SIZE + SPACE), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == ''

def is_board_full():
    return all(all(cell != '' for cell in row) for row in board)

def check_win(player):
    # Check horizontal
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True, [(row, 0), (row, 1), (row, 2)]
    # Check vertical
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True, [(0, col), (1, col), (2, col)]
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True, [(0, 0), (1, 1), (2, 2)]
    if board[0][2] == board[1][1] == board[2][0] == player:
        return True, [(0, 2), (1, 1), (2, 0)]
    return False, []

def minimax(board, depth, is_maximizing):
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
                    score = minimax(board, depth + 1, False)
                    board[row][col] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == '':
                    board[row][col] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[row][col] = ''
                    best_score = min(score, best_score)
        return best_score

def get_best_move():
    best_score = -math.inf
    best_move = None
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == '':
                board[row][col] = 'O'
                score = minimax(board, 0, False)
                board[row][col] = ''
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    return best_move

def reset_game():
    global board, game_over, player, winner
    screen.fill(BG_COLOR)
    draw_lines()
    board = [['' for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    game_over = False
    player = 'X'
    winner = None

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

def draw_winner(winner):
    if winner == 'Draw':
        winner_text = font.render("It's a Draw!", True, TEXT_COLOR)
    else:
        winner_text = font.render(f"{'Player' if winner == 'X' else 'Computer'} Wins!", True, TEXT_COLOR)
    screen.blit(winner_text, (20, HEIGHT - 50))

def draw_winning_line(win_line):
    start_pos = (win_line[0][1] * SQUARE_SIZE + SQUARE_SIZE // 2 + (WIDTH - GAME_AREA_WIDTH),
                 win_line[0][0] * SQUARE_SIZE + SQUARE_SIZE // 2)
    end_pos = (win_line[2][1] * SQUARE_SIZE + SQUARE_SIZE // 2 + (WIDTH - GAME_AREA_WIDTH),
               win_line[2][0] * SQUARE_SIZE + SQUARE_SIZE // 2)
    pygame.draw.line(screen, CROSS_COLOR, start_pos, end_pos, LINE_WIDTH)

# Main game loop
player = 'X'
game_over = False
winner = None
win_line = []

draw_lines()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] - (WIDTH - GAME_AREA_WIDTH)
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
                    
                    draw_figures()
                    
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
                        
                        draw_figures()
    
    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    draw_status()
    draw_button("New Game", 20, HEIGHT - 100, 150, 50, reset_game)
    
    if game_over:
        draw_winner(winner)
        if win_line:
            draw_winning_line(win_line)
    
    pygame.display.update()
