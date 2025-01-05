# Connect Four Game
import numpy as np
import pygame
import sys
import os
import random
import math

# Indicate colors
blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
purple = (128, 0, 128)
yellow = (255, 255, 0)
grey = (100, 100, 100)
green = (0, 255, 0)
dark_red = (139, 0, 0)
white = (255, 255, 255)
# Indicate number of columns and rows for board
row_board = 6
column_board = 7
# Screen setting
pygame.init()
screen_width = column_board * 100
screen_height = (row_board + 1) * 100
screen_game = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Connect Four")
# Font setting
font = pygame.font.SysFont("monospace", 40)
# Define static variable
player = 0
computer = 1
player_piece = 1
computer_piece = 2


# Initial screen with Class Button
class Button:
    def __init__(self, x, y, width, height, color, text="", action=None, text_color=black):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action
        self.text_color = text_color

    def draw(self, screen):  # Draw the screen
        pygame.draw.rect(screen, self.color, self.rect)
        if self.text:
            font_surface = font.render(self.text, 1, self.text_color)
            text_rect = font_surface.get_rect(center=self.rect.center)
            screen.blit(font_surface, text_rect)

    def clicked(self, position):  # Click the button
        return self.rect.collidepoint(position)


# Exit button
class ExitButton(Button):
    def __init__(self, x, y, width, height, color, text="", action=None, text_color=black):
        super().__init__(x, y, width, height, color, text, action, text_color)
        self.image = os.path.join("Images", "exit_button.png")
        self.image = pygame.image.load(self.image)  # Load the exit button image
        self.image = pygame.transform.scale(self.image, (50, 50))  # Resize the image

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        # Draw the exit button image in the top right corner
        screen.blit(self.image, (self.rect.right - self.image.get_width(), self.rect.bottom))

    def clicked(self, position):
        return self.rect.collidepoint(position)


def exit_game():
    pygame.quit()
    sys.exit()


def main_menu():  # Main menu function
    # Logo image
    logo_path = os.path.join("Images", "Connect_four_logo.png")
    logo_image = pygame.image.load(logo_path)
    resized_image = pygame.transform.scale(logo_image, (500, 150))
    # Create buttons
    start_button = Button(250, 250, 200, 50, blue, "Start", show_start_menu)
    intro_button = Button(200, 350, 300, 50, grey, "Introduction", show_introduction, white)
    quit_button = ExitButton(30, 580, 50, 50, grey, action=exit_game)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Trigger the action for buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.clicked(pygame.mouse.get_pos()):
                    quit_button.action()
                if start_button.clicked(pygame.mouse.get_pos()):
                    start_button.action()
                if intro_button.clicked(pygame.mouse.get_pos()):
                    intro_button.action()
        # Fill the screen with buttons
        screen_game.fill(grey)
        screen_game.blit(resized_image, (90, 45))
        start_button.draw(screen_game)
        intro_button.draw(screen_game)
        quit_button.draw(screen_game)
        pygame.display.update()


def show_start_menu():  # Function to show start menu
    pvp_button = Button(100, 200, 500, 50, red, "Player vs Player", play_pvp_game)
    pvc_button = Button(100, 400, 500, 50, red, "Player vs Computer", pvc_mode)
    back_button = Button(50, 50, 100, 20, grey, "Back", main_menu, white)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Trigger the action for buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pvp_button.clicked(pygame.mouse.get_pos()):
                    pvp_button.action()
                if pvc_button.clicked(pygame.mouse.get_pos()):
                    pvc_button.action()
                if back_button.clicked(pygame.mouse.get_pos()):
                    back_button.action()
        # Fill the screen with buttons
        screen_game.fill(grey)
        pvp_button.draw(screen_game)
        pvc_button.draw(screen_game)
        back_button.draw(screen_game)
        pygame.display.update()


def show_introduction():  # Function to show game introduction
    # Add the board image
    board_image_path = os.path.join("Images", "Connect_four_board.png")
    board_image = pygame.image.load(board_image_path)
    resized_image = pygame.transform.scale(board_image, (300, 250))
    intro_text = ["Introduction: ",
                  "Connect Four is a Two-Player Game in which the players",
                  "take turns dropping colored discs from the top into", "a vertically suspended grid.",
                  "The objective is to be the first to form a horizontal, ",
                  "vertical or diagonal line of four of one's own discs.", "Have Fun!!", ]
    # Change the font for the text
    word_font = pygame.font.SysFont("monospace", 18)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Trigger the action for buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                main_menu()

        screen_game.fill(grey)
        for i, line in enumerate(intro_text):
            line_surface = word_font.render(line, 1, white)
            screen_game.blit(line_surface, (50, 100 + i * 30))

        screen_game.blit(resized_image, (200, 350))
        pygame.display.update()


def play_pvp_game():  # If user chooses "Player vs Player", plays the connect four game
    game_connect_four()


def play_pvc_easy():  # Start playing "Player vs Computer in Easy"
    connect_four_easy_mode()


def play_pvc_medium():   # Start playing "Player vs Computer in Medium"
    connect_four_medium_mode()


def play_pvc_hard():   # Start playing "Player vs Computer in Hard"
    connect_four_hard_mode()


def play_pvc_extreme():   # Start playing "Player vs Computer in Extreme"
    # The CPU in this difficulty will be unbeatable
    connect_four_extreme_mode()


def pvc_mode():  # If user chooses "Player vs Computer", the user must choose CPU level
    # "Choose Difficulty" Text
    choose_difficulty = font.render("Choose Difficulty", 1, white)
    # Back Button
    easy_button = Button(200, 300, 300, 50, green, "EASY", play_pvc_easy)
    medium_button = Button(200, 400, 300, 50, yellow, "MEDIUM", play_pvc_medium)
    hard_button = Button(200, 500, 300, 50, red, "HARD", play_pvc_hard)
    extreme_button = Button(200, 600, 300, 50, dark_red, "EXTREME", play_pvc_extreme)
    back_button = Button(50, 50, 100, 20, grey, "Back", show_start_menu, white)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Trigger the action for buttons
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.clicked(pygame.mouse.get_pos()):
                    easy_button.action()
                if medium_button.clicked(pygame.mouse.get_pos()):
                    medium_button.action()
                if hard_button.clicked(pygame.mouse.get_pos()):
                    hard_button.action()
                if extreme_button.clicked(pygame.mouse.get_pos()):
                    extreme_button.action()
                if back_button.clicked(pygame.mouse.get_pos()):
                    back_button.action()
        # Fill the screen with buttons
        screen_game.fill(grey)
        screen_game.blit(choose_difficulty, (140, 150))
        easy_button.draw(screen_game)
        medium_button.draw(screen_game)
        hard_button.draw(screen_game)
        extreme_button.draw(screen_game)
        back_button.draw(screen_game)
        pygame.display.update()


def game_connect_four():

    def create_board():  # Create a board
        board = np.zeros((row_board, column_board))
        return board

    def drop_piece(board, move_row, move_col, piece):  # Drop piece
        board[move_row][move_col] = piece

    def is_valid_location(board, move_col):  # Check if the move is valid
        return board[row_board - 1][move_col] == 0

    def get_next_open_row(board, move_col):
        for row in range(row_board):
            if board[row][move_col] == 0:
                return row

    def winning_game(board, piece):  # Winning move
        # Four pieces are needed for the win
        # Check Horizontal position
        for col in range(column_board - 3):  # Only four columns
            for row in range(row_board):
                # If the number of pieces is equal to the len of array
                if (board[row][col] == piece and board[row][col + 1] == piece
                        and board[row][col + 2] == piece and board[row][col + 3] == piece):
                    return True
        # Check Vertical position
        for col in range(column_board):
            for row in range(row_board - 3):  # Only three rows
                if (board[row][col] == piece and board[row + 1][col] == piece
                        and board[row + 2][col] == piece and board[row + 3][col] == piece):
                    return True
        # Check for positive diagonals
        for col in range(column_board - 3):
            for row in range(row_board - 3):
                if (board[row][col] == piece and board[row + 1][col + 1] == piece
                        and board[row + 2][col + 2] == piece and board[row + 3][col + 3] == piece):
                    return True
        # Check for negative diagonals
        for col in range(column_board - 3):
            for row in range(3, row_board):
                if (board[row][col] == piece and board[row - 1][col + 1] == piece
                        and board[row - 2][col + 2] == piece and board[row - 3][col + 3] == piece):
                    return True
        return False

    def draw_game(board):  # Draw Game
        # Check when there is no more valid move left
        return np.count_nonzero(board == 0) == 0

    def draw_board(screen, board, square_size, height, radius):  # Draw the board in the game screen
        for col in range(column_board):
            for row in range(row_board):
                # Draw the blue board
                pygame.draw.rect(screen, blue, (col * square_size, row * square_size + square_size,
                                                square_size, square_size))
                # Draw the black circle
                pygame.draw.circle(screen, black, (col * square_size + square_size / 2,
                                                   row * square_size + square_size + square_size // 2), radius)
        # Draw the pieces
        for col in range(column_board):
            for row in range(row_board):
                if board[row][col] == 1:
                    pygame.draw.circle(screen, red, (col * square_size + square_size // 2,
                                                     height - (row * square_size + square_size // 2)), radius)
                elif board[row][col] == 2:
                    pygame.draw.circle(screen, yellow, (col * square_size + square_size // 2,
                                                        height - (row * square_size + square_size // 2)), radius)
        pygame.display.update()

    def gameplay():
        game_board = create_board()
        game_over = False
        turn = 0
        # Initialize Game
        pygame.init()
        pygame.display.set_caption('Connect Four')
        # Indicate game screen
        square_size = 100
        # Width and Height of the board
        width = column_board * square_size
        height = (row_board + 1) * square_size
        size = (width, height)
        # Radius of the circles
        radius = square_size // 2 - 5
        # Display the screen
        screen = pygame.display.set_mode(size)
        # Call the draw board function to update the board
        draw_board(screen, game_board, square_size, height, radius)
        pygame.display.update()
        # Font of the words
        display_font = pygame.font.SysFont("monospace", 75)
        # Handle mouse click and controls
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit button
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:  # Mouse motion
                    pygame.draw.rect(screen, black, (0, 0, width, square_size))
                    pos_x = event.pos[0]
                    if turn == 0:  # Player 1 uses red piece
                        pygame.draw.circle(screen, red, (pos_x, square_size // 2), radius)
                    else:  # Player 2 uses yellow pieces
                        pygame.draw.circle(screen, yellow, (pos_x, square_size // 2), radius)
                pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse button goes down
                    pygame.draw.rect(screen, black, (0, 0, width, square_size))
                    # Player 1's move
                    if turn == 0:
                        pos_x = event.pos[0]
                        select_col = int(math.floor(pos_x / square_size))
                        # If the location is valid, proceed to put the piece
                        if is_valid_location(game_board, select_col):
                            select_row = get_next_open_row(game_board, select_col)
                            drop_piece(game_board, select_row, select_col, 1)
                            # Display if Player 1 Wins
                            if winning_game(game_board, 1):
                                label = display_font.render("Player 1 Wins!!", 1, red)
                                # Where the label is at
                                screen.blit(label, (20, 10))
                                game_over = True
                    # Player 2's move
                    else:
                        pos_x = event.pos[0]
                        select_col = int(math.floor(pos_x / square_size))
                        # If the location is valid, proceed to put the piece
                        if is_valid_location(game_board, select_col):
                            select_row = get_next_open_row(game_board, select_col)
                            drop_piece(game_board, select_row, select_col, 2)
                            # Display if Player 2 Wins
                            if winning_game(game_board, 2):
                                label = display_font.render("Player 2 Wins!!", 1, yellow)
                                # Where the label is at
                                screen.blit(label, (20, 10))
                                game_over = True

                    draw_board(screen, game_board, square_size, height, radius)
                    turn += 1
                    turn = turn % 2

            if draw_game(game_board):
                label = display_font.render("\t\t\t\t\tDraw!!", 1, purple)
                screen.blit(label, (20, 10))
                game_over = True

        # Display "Press R to play again or Q to quit" text
        play_again_font = pygame.font.SysFont("monospace", 30, bold=True)
        play_again_label = play_again_font.render("Press P-Play Again or R-Return", 1, grey)
        play_again_rect = play_again_label.get_rect(center=(width // 2, height - square_size // 2))
        screen.blit(play_again_label, play_again_rect)
        pygame.display.update()
        # Handle closing windows manually
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Restart the game or Quit the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        game_connect_four()
                    if event.key == pygame.K_r:
                        show_start_menu()
    # Start the game
    gameplay()


def connect_four_easy_mode():  # Create a game with easy CPU
    # In easy mode, the CPU only chooses the best move
    def create_board():  # Create a board
        board = np.zeros((row_board, column_board))
        return board

    def drop_piece(board, move_row, move_col, piece):  # Drop piece
        board[move_row][move_col] = piece

    def is_valid_location(board, move_col):  # Check if the move is valid
        return board[row_board - 1][move_col] == 0

    def get_next_open_row(board, move_col):
        for row in range(row_board):
            if board[row][move_col] == 0:
                return row

    def winning_game(board, piece):  # Winning move
        # Four pieces are needed for the win
        # Check Horizontal position
        for col in range(column_board - 3):  # Only four columns
            for row in range(row_board):
                # If the number of pieces is equal to the len of array
                if (board[row][col] == piece and board[row][col + 1] == piece
                        and board[row][col + 2] == piece and board[row][col + 3] == piece):
                    return True
        # Check Vertical position
        for col in range(column_board):
            for row in range(row_board - 3):  # Only three rows
                if (board[row][col] == piece and board[row + 1][col] == piece
                        and board[row + 2][col] == piece and board[row + 3][col] == piece):
                    return True
        # Check for positive diagonals
        for col in range(column_board - 3):
            for row in range(row_board - 3):
                if (board[row][col] == piece and board[row + 1][col + 1] == piece
                        and board[row + 2][col + 2] == piece and board[row + 3][col + 3] == piece):
                    return True
        # Check for negative diagonals
        for col in range(column_board - 3):
            for row in range(3, row_board):
                if (board[row][col] == piece and board[row - 1][col + 1] == piece
                        and board[row - 2][col + 2] == piece and board[row - 3][col + 3] == piece):
                    return True
        return False

    def score_position(board, piece):  # Define score position for CPU to pick move
        # Horizontal
        score = 0
        for row in range(row_board):
            row_array = [int(i) for i in list(board[row, :])]
            for col in range(column_board - 3):
                window = row_array[col:col+4]  # Window length
                if window.count(piece) == 4:
                    score += 100
                elif window.count(piece) == 3 and window.count(0) == 1:
                    score += 10

        # Vertical
        for col in range(column_board):
            col_array = [int(i) for i in list(board[:, col])]
            for row in range(row_board - 3):
                window = col_array[row:row+4]  # Window length
                if window.count(piece) == 4:
                    score += 100
                elif window.count(piece) == 3 and window.count(0) == 1:
                    score += 10

        # Positive Diagonal
        for row in range(row_board - 3):
            for col in range(column_board - 3):
                window = [board[row+i][col+i] for i in range(4)]  # Window length
                if window.count(piece) == 4:
                    score += 100
                elif window.count(piece) == 3 and window.count(0) == 1:
                    score += 10

        # Negative Diagonal
        for row in range(row_board - 3):
            for col in range(column_board - 3):
                window = [board[row + 3 - i][col + i] for i in range(4)]  # Window length
                if window.count(piece) == 4:
                    score += 100
                elif window.count(piece) == 3 and window.count(0) == 1:
                    score += 10

        return score

    def get_valid_locations(board):  # Make sure the CPU make a valid move
        valid_locations = []
        for col in range(column_board):
            if is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    def best_move(board, piece):  # Function for CPU to pick the best move
        valid_locations = get_valid_locations(board)
        best_score = 0
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, piece)
            score = score_position(temp_board, piece)
            if score > best_score:  # Set the new best score to the highest score
                best_score = score
                best_col = col  # Set new column
        return best_col

    def draw_game(board):  # Draw Game
        # Check when there is no more valid move left
        return np.count_nonzero(board == 0) == 0

    def draw_board(screen, board, square_size, height, radius):  # Draw the board in the game screen
        for col in range(column_board):
            for row in range(row_board):
                # Draw the blue board
                pygame.draw.rect(screen, blue, (col * square_size, row * square_size + square_size,
                                                square_size, square_size))
                # Draw the black circle
                pygame.draw.circle(screen, black, (col * square_size + square_size / 2,
                                                   row * square_size + square_size + square_size // 2), radius)
        # Draw the pieces
        for col in range(column_board):
            for row in range(row_board):
                if board[row][col] == player_piece:
                    pygame.draw.circle(screen, red, (col * square_size + square_size // 2,
                                                     height - (row * square_size + square_size // 2)), radius)
                elif board[row][col] == computer_piece:
                    pygame.draw.circle(screen, yellow, (col * square_size + square_size // 2,
                                                        height - (row * square_size + square_size // 2)), radius)
        pygame.display.update()

    def gameplay():
        game_board = create_board()
        game_over = False
        turn = 0
        # Initialize Game
        pygame.init()
        pygame.display.set_caption('Connect Four')
        # Indicate game screen
        square_size = 100
        # Width and Height of the board
        width = column_board * square_size
        height = (row_board + 1) * square_size
        size = (width, height)
        # Radius of the circles
        radius = square_size // 2 - 5
        # Display the screen
        screen = pygame.display.set_mode(size)
        # Call the draw board function to update the board
        draw_board(screen, game_board, square_size, height, radius)
        pygame.display.update()
        # Font of the words
        display_font = pygame.font.SysFont("monospace", 75)
        # Handle mouse click and controls
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit button
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:  # Mouse motion
                    pygame.draw.rect(screen, black, (0, 0, width, square_size))
                    pos_x = event.pos[0]
                    if turn == 0:  # Player 1 uses red piece
                        pygame.draw.circle(screen, red, (pos_x, square_size // 2), radius)
                    else:  # Player 2 uses yellow pieces
                        pygame.draw.circle(screen, yellow, (pos_x, square_size // 2), radius)
                pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse button goes down
                    pygame.draw.rect(screen, black, (0, 0, width, square_size))
                    # Player 1's move
                    if turn == 0:
                        pos_x = event.pos[0]
                        select_col = int(math.floor(pos_x / square_size))
                        # If the location is valid, proceed to put the piece
                        if is_valid_location(game_board, select_col):
                            select_row = get_next_open_row(game_board, select_col)
                            drop_piece(game_board, select_row, select_col, player_piece)
                            # Display if Player 1 Wins
                            if winning_game(game_board, player_piece):
                                label = display_font.render("\tPlayer Wins!!", 1, red)
                                # Where the label is at
                                screen.blit(label, (20, 10))
                                game_over = True
                            # Update the board before computer's turn
                            draw_board(screen, game_board, square_size, height, radius)
                            turn += 1
                            turn = turn % 2

                # CPU's move
                if turn == computer and not game_over:
                    select_col = best_move(game_board, computer_piece)
                    # If the location is valid, proceed to put the piece
                    if is_valid_location(game_board, select_col):
                        pygame.time.wait(500)
                        select_row = get_next_open_row(game_board, select_col)
                        drop_piece(game_board, select_row, select_col, computer_piece)
                        # Display if Player 2 Wins
                        if winning_game(game_board, computer_piece):
                            label = display_font.render("Computer Wins!!", 1, yellow)
                            # Where the label is at
                            screen.blit(label, (20, 10))
                            game_over = True
                    # Update for the user's next turn
                    draw_board(screen, game_board, square_size, height, radius)
                    turn += 1
                    turn = turn % 2

            if draw_game(game_board):
                label = display_font.render("\t\t\t\t\tDraw!!", 1, purple)
                screen.blit(label, (20, 10))
                game_over = True

        # Display "Press R to play again or Q to quit" text
        play_again_font = pygame.font.SysFont("monospace", 30, bold=True)
        play_again_label = play_again_font.render("Press P-Play Again or R-Return", 1, grey)
        play_again_rect = play_again_label.get_rect(center=(width // 2, height - square_size // 2))
        screen.blit(play_again_label, play_again_rect)
        pygame.display.update()
        # Handle closing windows manually
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Restart the game or Quit the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        connect_four_easy_mode()
                    if event.key == pygame.K_r:
                        show_start_menu()
    # Start the game
    gameplay()


def connect_four_medium_mode():  # Create a game with medium CPU
    # In medium mode, we implement Minimax Algorithm with low depth
    def create_board():  # Create a board
        board = np.zeros((row_board, column_board))
        return board

    def drop_piece(board, move_row, move_col, piece):  # Drop piece
        board[move_row][move_col] = piece

    def is_valid_location(board, move_col):  # Check if the move is valid
        return board[row_board - 1][move_col] == 0

    def get_next_open_row(board, move_col):
        for row in range(row_board):
            if board[row][move_col] == 0:
                return row

    def winning_game(board, piece):  # Winning move
        # Four pieces are needed for the win
        # Check Horizontal position
        for col in range(column_board - 3):  # Only four columns
            for row in range(row_board):
                # If the number of pieces is equal to the len of array
                if (board[row][col] == piece and board[row][col + 1] == piece
                        and board[row][col + 2] == piece and board[row][col + 3] == piece):
                    return True
        # Check Vertical position
        for col in range(column_board):
            for row in range(row_board - 3):  # Only three rows
                if (board[row][col] == piece and board[row + 1][col] == piece
                        and board[row + 2][col] == piece and board[row + 3][col] == piece):
                    return True
        # Check for positive diagonals
        for col in range(column_board - 3):
            for row in range(row_board - 3):
                if (board[row][col] == piece and board[row + 1][col + 1] == piece
                        and board[row + 2][col + 2] == piece and board[row + 3][col + 3] == piece):
                    return True
        # Check for negative diagonals
        for col in range(column_board - 3):
            for row in range(3, row_board):
                if (board[row][col] == piece and board[row - 1][col + 1] == piece
                        and board[row - 2][col + 2] == piece and board[row - 3][col + 3] == piece):
                    return True
        return False

    def evaluate_window(window, piece):  # Evaluate window clearer for CPU to make better move
        turn_piece = player_piece
        if piece == player_piece:
            turn_piece = computer_piece
        score = 0
        # Counting possible connect four
        # by counting number of pieces to number of empty slot required
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 10
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 5
	# Possible player's connect four
        if window.count(turn_piece) == 3 and window.count(0) == 1:
            score -= 80

        return score

    def terminal_node(board):  # There is no more possible move
        return (winning_game(board, player_piece) or
                winning_game(board, computer_piece) or len(get_valid_locations(board)) == 0)

    def minimax(board, depth, maximizing_player):  # Use minimax algorithm to increase the level of CPU
        valid_locations = get_valid_locations(board)
        is_terminal_node = terminal_node(board)
        if depth == 0 or is_terminal_node:
            if is_terminal_node:
                if winning_game(board, computer_piece):  # Computer wins
                    return None, 100000
                elif winning_game(board, player_piece):  # Player wins
                    return None, -10000
                else:  # Game over
                    return None, 0
            else:  # Depth == 0
                return None, score_position(board, computer_piece)
        if maximizing_player:
            value = - math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                board_copy = board.copy()
                drop_piece(board_copy, row, col, computer_piece)
                new_score = minimax(board_copy, depth - 1, False)[1]
                if new_score > value:
                    value = new_score
                    best_col = col
            return best_col, value
        else:  # Minimizing Player
            value = math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                board_copy = board.copy()
                drop_piece(board_copy, row, col, player_piece)
                new_score = minimax(board_copy, depth - 1, True)[1]
                if new_score < value:
                    value = new_score
                    best_col = col
            return best_col, value

    def score_position(board, piece):  # Define score position for CPU to pick move
        score = 0
        # Center column
        center_array = [int(i) for i in list(board[:, column_board // 2])]
        center_count = center_array.count(piece)
        score += center_count * 6
        # Horizontal
        for row in range(row_board):
            row_array = [int(i) for i in list(board[row, :])]
            for col in range(column_board - 3):
                window = row_array[col:col+4]  # Window length
                score += evaluate_window(window, piece)

        # Vertical
        for col in range(column_board):
            col_array = [int(i) for i in list(board[:, col])]
            for row in range(row_board - 3):
                window = col_array[row:row+4]  # Window length
                score += evaluate_window(window, piece)

        # Positive Diagonal
        for row in range(row_board - 3):
            for col in range(column_board - 3):
                window = [board[row+i][col+i] for i in range(4)]  # Window length
                score += evaluate_window(window, piece)

        # Negative Diagonal
        for row in range(row_board - 3):
            for col in range(column_board - 3):
                window = [board[row + 3 - i][col + i] for i in range(4)]  # Window length
                score += evaluate_window(window, piece)

        return score

    def get_valid_locations(board):  # Make sure the CPU make a valid move
        valid_locations = []
        for col in range(column_board):
            if is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    def draw_game(board):  # Draw Game
        # Check when there is no more valid move left
        return np.count_nonzero(board == 0) == 0

    def draw_board(screen, board, square_size, height, radius):  # Draw the board in the game screen
        for col in range(column_board):
            for row in range(row_board):
                # Draw the blue board
                pygame.draw.rect(screen, blue, (col * square_size, row * square_size + square_size,
                                                square_size, square_size))
                # Draw the black circle
                pygame.draw.circle(screen, black, (col * square_size + square_size / 2,
                                                   row * square_size + square_size + square_size // 2), radius)
        # Draw the pieces
        for col in range(column_board):
            for row in range(row_board):
                if board[row][col] == player_piece:
                    pygame.draw.circle(screen, red, (col * square_size + square_size // 2,
                                                     height - (row * square_size + square_size // 2)), radius)
                elif board[row][col] == computer_piece:
                    pygame.draw.circle(screen, yellow, (col * square_size + square_size // 2,
                                                        height - (row * square_size + square_size // 2)), radius)
        pygame.display.update()

    def gameplay():
        game_board = create_board()
        game_over = False
        turn = 0
        # Initialize Game
        pygame.init()
        pygame.display.set_caption('Connect Four')
        # Indicate game screen
        square_size = 100
        # Width and Height of the board
        width = column_board * square_size
        height = (row_board + 1) * square_size
        size = (width, height)
        # Radius of the circles
        radius = square_size // 2 - 5
        # Display the screen
        screen = pygame.display.set_mode(size)
        # Call the draw board function to update the board
        draw_board(screen, game_board, square_size, height, radius)
        pygame.display.update()
        # Font of the words
        display_font = pygame.font.SysFont("monospace", 75)
        # Handle mouse click and controls
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit button
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:  # Mouse motion
                    pygame.draw.rect(screen, black, (0, 0, width, square_size))
                    pos_x = event.pos[0]
                    if turn == 0:  # Player 1 uses red piece
                        pygame.draw.circle(screen, red, (pos_x, square_size // 2), radius)
                    else:  # Player 2 uses yellow pieces
                        pygame.draw.circle(screen, yellow, (pos_x, square_size // 2), radius)
                pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse button goes down
                    pygame.draw.rect(screen, black, (0, 0, width, square_size))
                    # Player 1's move
                    if turn == 0:
                        pos_x = event.pos[0]
                        select_col = int(math.floor(pos_x / square_size))
                        # If the location is valid, proceed to put the piece
                        if is_valid_location(game_board, select_col):
                            select_row = get_next_open_row(game_board, select_col)
                            drop_piece(game_board, select_row, select_col, player_piece)
                            # Display if Player 1 Wins
                            if winning_game(game_board, player_piece):
                                label = display_font.render("\tPlayer Wins!!", 1, red)
                                # Where the label is at
                                screen.blit(label, (20, 10))
                                game_over = True
                            # Update the board before computer's turn
                            draw_board(screen, game_board, square_size, height, radius)
                            turn += 1
                            turn = turn % 2

                # CPU's move
                if turn == computer and not game_over:
                    select_col, minimax_score = minimax(game_board, 2, True)
                    # If the location is valid, proceed to put the piece
                    if is_valid_location(game_board, select_col):
                        pygame.time.wait(500)
                        select_row = get_next_open_row(game_board, select_col)
                        drop_piece(game_board, select_row, select_col, computer_piece)
                        # Display if Player 2 Wins
                        if winning_game(game_board, computer_piece):
                            label = display_font.render("Computer Wins!!", 1, yellow)
                            # Where the label is at
                            screen.blit(label, (20, 10))
                            game_over = True
                    # Update for the user's next turn
                    draw_board(screen, game_board, square_size, height, radius)
                    turn += 1
                    turn = turn % 2

            if draw_game(game_board):
                label = display_font.render("\t\t\t\t\tDraw!!", 1, purple)
                screen.blit(label, (20, 10))
                game_over = True

        # Display "Press R to play again or Q to quit" text
        play_again_font = pygame.font.SysFont("monospace", 30, bold=True)
        play_again_label = play_again_font.render("Press P-Play Again or R-Return", 1, grey)
        play_again_rect = play_again_label.get_rect(center=(width // 2, height - square_size // 2))
        screen.blit(play_again_label, play_again_rect)
        pygame.display.update()
        # Handle closing windows manually
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Restart the game or Quit the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        connect_four_medium_mode()
                    if event.key == pygame.K_r:
                        show_start_menu()
    # Start the game
    gameplay()


def connect_four_hard_mode():  # Create a game with hard CPU
    # In hard mode, we implement Minimax Algorithm with high depth
    def create_board():  # Create a board
        board = np.zeros((row_board, column_board))
        return board

    def drop_piece(board, move_row, move_col, piece):  # Drop piece
        board[move_row][move_col] = piece

    def is_valid_location(board, move_col):  # Check if the move is valid
        return board[row_board - 1][move_col] == 0

    def get_next_open_row(board, move_col):
        for row in range(row_board):
            if board[row][move_col] == 0:
                return row

    def winning_game(board, piece):  # Winning move
        # Four pieces are needed for the win
        # Check Horizontal position
        for col in range(column_board - 3):  # Only four columns
            for row in range(row_board):
                # If the number of pieces is equal to the len of array
                if (board[row][col] == piece and board[row][col + 1] == piece
                        and board[row][col + 2] == piece and board[row][col + 3] == piece):
                    return True
        # Check Vertical position
        for col in range(column_board):
            for row in range(row_board - 3):  # Only three rows
                if (board[row][col] == piece and board[row + 1][col] == piece
                        and board[row + 2][col] == piece and board[row + 3][col] == piece):
                    return True
        # Check for positive diagonals
        for col in range(column_board - 3):
            for row in range(row_board - 3):
                if (board[row][col] == piece and board[row + 1][col + 1] == piece
                        and board[row + 2][col + 2] == piece and board[row + 3][col + 3] == piece):
                    return True
        # Check for negative diagonals
        for col in range(column_board - 3):
            for row in range(3, row_board):
                if (board[row][col] == piece and board[row - 1][col + 1] == piece
                        and board[row - 2][col + 2] == piece and board[row - 3][col + 3] == piece):
                    return True
        return False

    def evaluate_window(window, piece):  # Evaluate window clearer for CPU to make better move
        turn_piece = player_piece
        if piece == player_piece:
            turn_piece = computer_piece
        score = 0
        # Counting possible connect four
        # by counting number of pieces to number of empty slot required
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 10
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 5

        if window.count(turn_piece) == 3 and window.count(0) == 1:
            score -= 80

        return score

    def terminal_node(board):  # There is no more possible move
        return (winning_game(board, player_piece) or
                winning_game(board, computer_piece) or len(get_valid_locations(board)) == 0)

    def minimax(board, depth, alpha, beta, maximizing_player):  # Use minimax algorithm to increase the level of CPU
        valid_locations = get_valid_locations(board)
        is_terminal_node = terminal_node(board)
        if depth == 0 or is_terminal_node:
            if is_terminal_node:
                if winning_game(board, computer_piece):  # Computer wins
                    return None, 100000
                elif winning_game(board, player_piece):  # Player wins
                    return None, -10000
                else:  # Game over
                    return None, 0
            else:  # Depth == 0
                return None, score_position(board, computer_piece)
        if maximizing_player:
            value = - math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                board_copy = board.copy()
                drop_piece(board_copy, row, col, computer_piece)
                new_score = minimax(board_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_col, value
        else:  # Minimizing Player
            value = math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                board_copy = board.copy()
                drop_piece(board_copy, row, col, player_piece)
                new_score = minimax(board_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_col, value

    def score_position(board, piece):  # Define score position for CPU to pick move
        score = 0
        # Center column
        center_array = [int(i) for i in list(board[:, column_board // 2])]
        center_count = center_array.count(piece)
        score += center_count * 6
        # Horizontal
        for row in range(row_board):
            row_array = [int(i) for i in list(board[row, :])]
            for col in range(column_board - 3):
                window = row_array[col:col + 4]  # Window length
                score += evaluate_window(window, piece)

        # Vertical
        for col in range(column_board):
            col_array = [int(i) for i in list(board[:, col])]
            for row in range(row_board - 3):
                window = col_array[row:row + 4]  # Window length
                score += evaluate_window(window, piece)

        # Positive Diagonal
        for row in range(row_board - 3):
            for col in range(column_board - 3):
                window = [board[row + i][col + i] for i in range(4)]  # Window length
                score += evaluate_window(window, piece)

        # Negative Diagonal
        for row in range(row_board - 3):
            for col in range(column_board - 3):
                window = [board[row + 3 - i][col + i] for i in range(4)]  # Window length
                score += evaluate_window(window, piece)

        return score

    def get_valid_locations(board):  # Make sure the CPU make a valid move
        valid_locations = []
        for col in range(column_board):
            if is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    def draw_game(board):  # Draw Game
        # Check when there is no more valid move left
        return np.count_nonzero(board == 0) == 0

    def draw_board(screen, board, square_size, height, radius):  # Draw the board in the game screen
        for col in range(column_board):
            for row in range(row_board):
                # Draw the blue board
                pygame.draw.rect(screen, blue, (col * square_size, row * square_size + square_size,
                                                square_size, square_size))
                # Draw the black circle
                pygame.draw.circle(screen, black, (col * square_size + square_size / 2,
                                                   row * square_size + square_size + square_size // 2), radius)
        # Draw the pieces
        for col in range(column_board):
            for row in range(row_board):
                if board[row][col] == player_piece:
                    pygame.draw.circle(screen, red, (col * square_size + square_size // 2,
                                                     height - (row * square_size + square_size // 2)), radius)
                elif board[row][col] == computer_piece:
                    pygame.draw.circle(screen, yellow, (col * square_size + square_size // 2,
                                                        height - (row * square_size + square_size // 2)), radius)
        pygame.display.update()

    def gameplay():
        game_board = create_board()
        game_over = False
        turn = 0
        # Initialize Game
        pygame.init()
        pygame.display.set_caption('Connect Four')
        # Indicate game screen
        square_size = 100
        # Width and Height of the board
        width = column_board * square_size
        height = (row_board + 1) * square_size
        size = (width, height)
        # Radius of the circles
        radius = square_size // 2 - 5
        # Display the screen
        screen = pygame.display.set_mode(size)
        # Call the draw board function to update the board
        draw_board(screen, game_board, square_size, height, radius)
        pygame.display.update()
        # Font of the words
        display_font = pygame.font.SysFont("monospace", 75)
        # Handle mouse click and controls
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit button
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:  # Mouse motion
                    pygame.draw.rect(screen, black, (0, 0, width, square_size))
                    pos_x = event.pos[0]
                    if turn == 0:  # Player 1 uses red piece
                        pygame.draw.circle(screen, red, (pos_x, square_size // 2), radius)
                    else:  # Player 2 uses yellow pieces
                        pygame.draw.circle(screen, yellow, (pos_x, square_size // 2), radius)
                pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse button goes down
                    pygame.draw.rect(screen, black, (0, 0, width, square_size))
                    # Player 1's move
                    if turn == 0:
                        pos_x = event.pos[0]
                        select_col = int(math.floor(pos_x / square_size))
                        # If the location is valid, proceed to put the piece
                        if is_valid_location(game_board, select_col):
                            select_row = get_next_open_row(game_board, select_col)
                            drop_piece(game_board, select_row, select_col, player_piece)
                            # Display if Player 1 Wins
                            if winning_game(game_board, player_piece):
                                label = display_font.render("\tPlayer Wins!!", 1, red)
                                # Where the label is at
                                screen.blit(label, (20, 10))
                                game_over = True
                            # Update the board before computer's turn
                            draw_board(screen, game_board, square_size, height, radius)
                            turn += 1
                            turn = turn % 2

                # CPU's move
                if turn == computer and not game_over:
                    select_col, minimax_score = minimax(game_board, 4, -math.inf, math.inf, True)
                    # If the location is valid, proceed to put the piece
                    if is_valid_location(game_board, select_col):
                        pygame.time.wait(500)
                        select_row = get_next_open_row(game_board, select_col)
                        drop_piece(game_board, select_row, select_col, computer_piece)
                        # Display if Player 2 Wins
                        if winning_game(game_board, computer_piece):
                            label = display_font.render("Computer Wins!!", 1, yellow)
                            # Where the label is at
                            screen.blit(label, (20, 10))
                            game_over = True
                    # Update for the user's next turn
                    draw_board(screen, game_board, square_size, height, radius)
                    turn += 1
                    turn = turn % 2

            if draw_game(game_board):
                label = display_font.render("\t\t\t\t\tDraw!!", 1, purple)
                screen.blit(label, (20, 10))
                game_over = True

        # Display "Press R to play again or Q to quit" text
        play_again_font = pygame.font.SysFont("monospace", 30, bold=True)
        play_again_label = play_again_font.render("Press P-Play Again or R-Return", 1, grey)
        play_again_rect = play_again_label.get_rect(center=(width // 2, height - square_size // 2))
        screen.blit(play_again_label, play_again_rect)
        pygame.display.update()
        # Handle closing windows manually
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Restart the game or Quit the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        connect_four_hard_mode()
                    if event.key == pygame.K_r:
                        show_start_menu()

    # Start the game
    gameplay()


def connect_four_extreme_mode():  # Create a game with extreme CPU
    # In hard mode, we implement Minimax Algorithm with high depth
    def create_board():  # Create a board
        board = np.zeros((row_board, column_board))
        return board

    def drop_piece(board, move_row, move_col, piece):  # Drop piece
        board[move_row][move_col] = piece

    def is_valid_location(board, move_col):  # Check if the move is valid
        return board[row_board - 1][move_col] == 0

    def get_next_open_row(board, move_col):
        for row in range(row_board):
            if board[row][move_col] == 0:
                return row

    def winning_game(board, piece):  # Winning move
        # Four pieces are needed for the win
        # Check Horizontal position
        for col in range(column_board - 3):  # Only four columns
            for row in range(row_board):
                # If the number of pieces is equal to the len of array
                if (board[row][col] == piece and board[row][col + 1] == piece
                        and board[row][col + 2] == piece and board[row][col + 3] == piece):
                    return True
        # Check Vertical position
        for col in range(column_board):
            for row in range(row_board - 3):  # Only three rows
                if (board[row][col] == piece and board[row + 1][col] == piece
                        and board[row + 2][col] == piece and board[row + 3][col] == piece):
                    return True
        # Check for positive diagonals
        for col in range(column_board - 3):
            for row in range(row_board - 3):
                if (board[row][col] == piece and board[row + 1][col + 1] == piece
                        and board[row + 2][col + 2] == piece and board[row + 3][col + 3] == piece):
                    return True
        # Check for negative diagonals
        for col in range(column_board - 3):
            for row in range(3, row_board):
                if (board[row][col] == piece and board[row - 1][col + 1] == piece
                        and board[row - 2][col + 2] == piece and board[row - 3][col + 3] == piece):
                    return True
        return False

    def evaluate_window(window, piece):  # Evaluate window clearer for CPU to make better move
        turn_piece = player_piece
        if piece == player_piece:
            turn_piece = computer_piece
        score = 0
        # Counting possible connect four
        # by counting number of pieces to number of empty slot required
        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 10
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 5

        if window.count(turn_piece) == 3 and window.count(0) == 1:
            score -= 80

        return score

    def terminal_node(board):  # There is no more possible move
        return (winning_game(board, player_piece) or
                winning_game(board, computer_piece) or len(get_valid_locations(board)) == 0)

    def minimax(board, depth, alpha, beta, maximizing_player):  # Use minimax algorithm to increase the level of CPU
        valid_locations = get_valid_locations(board)
        is_terminal_node = terminal_node(board)
        if depth == 0 or is_terminal_node:
            if is_terminal_node:
                if winning_game(board, computer_piece):  # Computer wins
                    return None, 100000
                elif winning_game(board, player_piece):  # Player wins
                    return None, -10000
                else:  # Game over
                    return None, 0
            else:  # Depth == 0
                return None, score_position(board, computer_piece)
        if maximizing_player:
            value = - math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                board_copy = board.copy()
                drop_piece(board_copy, row, col, computer_piece)
                new_score = minimax(board_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    best_col = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_col, value
        else:  # Minimizing Player
            value = math.inf
            best_col = random.choice(valid_locations)
            for col in valid_locations:
                row = get_next_open_row(board, col)
                board_copy = board.copy()
                drop_piece(board_copy, row, col, player_piece)
                new_score = minimax(board_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    best_col = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return best_col, value

    def score_position(board, piece):  # Define score position for CPU to pick move
        score = 0
        # Center column
        center_array = [int(i) for i in list(board[:, column_board // 2])]
        center_count = center_array.count(piece)
        score += center_count * 6
        # Horizontal
        for row in range(row_board):
            row_array = [int(i) for i in list(board[row, :])]
            for col in range(column_board - 3):
                window = row_array[col:col + 4]  # Window length
                score += evaluate_window(window, piece)

        # Vertical
        for col in range(column_board):
            col_array = [int(i) for i in list(board[:, col])]
            for row in range(row_board - 3):
                window = col_array[row:row + 4]  # Window length
                score += evaluate_window(window, piece)

        # Positive Diagonal
        for row in range(row_board - 3):
            for col in range(column_board - 3):
                window = [board[row + i][col + i] for i in range(4)]  # Window length
                score += evaluate_window(window, piece)

        # Negative Diagonal
        for row in range(row_board - 3):
            for col in range(column_board - 3):
                window = [board[row + 3 - i][col + i] for i in range(4)]  # Window length
                score += evaluate_window(window, piece)

        return score

    def get_valid_locations(board):  # Make sure the CPU make a valid move
        valid_locations = []
        for col in range(column_board):
            if is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations

    def draw_game(board):  # Draw Game
        # Check when there is no more valid move left
        return np.count_nonzero(board == 0) == 0

    def draw_board(screen, board, square_size, height, radius):  # Draw the board in the game screen
        for col in range(column_board):
            for row in range(row_board):
                # Draw the blue board
                pygame.draw.rect(screen, blue, (col * square_size, row * square_size + square_size,
                                                square_size, square_size))
                # Draw the black circle
                pygame.draw.circle(screen, black, (col * square_size + square_size / 2,
                                                   row * square_size + square_size + square_size // 2), radius)
        # Draw the pieces
        for col in range(column_board):
            for row in range(row_board):
                if board[row][col] == player_piece:
                    pygame.draw.circle(screen, red, (col * square_size + square_size // 2,
                                                     height - (row * square_size + square_size // 2)), radius)
                elif board[row][col] == computer_piece:
                    pygame.draw.circle(screen, red, (col * square_size + square_size // 2,
                                                     height - (row * square_size + square_size // 2)), radius)
        pygame.display.update()

    def gameplay():
        game_board = create_board()
        game_over = False
        turn = 0
        # Initialize Game
        pygame.init()
        pygame.display.set_caption('Connect Four')
        # Indicate game screen
        square_size = 100
        # Width and Height of the board
        width = column_board * square_size
        height = (row_board + 1) * square_size
        size = (width, height)
        # Radius of the circles
        radius = square_size // 2 - 5
        # Display the screen
        screen = pygame.display.set_mode(size)
        # Call the draw board function to update the board
        draw_board(screen, game_board, square_size, height, radius)
        pygame.display.update()
        # Font of the words
        display_font = pygame.font.SysFont("monospace", 75)
        # Handle mouse click and controls
        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit button
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:  # Mouse motion
                    pygame.draw.rect(screen, black, (0, 0, width, square_size))
                    pos_x = event.pos[0]
                    if turn == 0:  # Player 1 uses red piece
                        pygame.draw.circle(screen, red, (pos_x, square_size // 2), radius)
                    else:  # Player 2 uses red piece, same with Player 1
                        pygame.draw.circle(screen, red, (pos_x, square_size // 2), radius)
                pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:  # Mouse button goes down
                    pygame.draw.rect(screen, black, (0, 0, width, square_size))
                    # Player 1's move
                    if turn == 0:
                        pos_x = event.pos[0]
                        select_col = int(math.floor(pos_x / square_size))
                        # If the location is valid, proceed to put the piece
                        if is_valid_location(game_board, select_col):
                            select_row = get_next_open_row(game_board, select_col)
                            drop_piece(game_board, select_row, select_col, player_piece)
                            # Display if Player 1 Wins
                            if winning_game(game_board, player_piece):
                                label = display_font.render("\tPlayer Wins!!", 1, red)
                                # Where the label is at
                                screen.blit(label, (20, 10))
                                game_over = True
                            # Update the board before computer's turn
                            draw_board(screen, game_board, square_size, height, radius)
                            turn += 1
                            turn = turn % 2

                # CPU's move
                if turn == computer and not game_over:
                    select_col, minimax_score = minimax(game_board, 5, -math.inf, math.inf, True)
                    # If the location is valid, proceed to put the piece
                    if is_valid_location(game_board, select_col):
                        pygame.time.wait(500)
                        select_row = get_next_open_row(game_board, select_col)
                        drop_piece(game_board, select_row, select_col, computer_piece)
                        # Display if Player 2 Wins
                        if winning_game(game_board, computer_piece):
                            label = display_font.render("Computer Wins!!", 1, yellow)
                            # Where the label is at
                            screen.blit(label, (20, 10))
                            game_over = True
                    # Update for the user's next turn
                    draw_board(screen, game_board, square_size, height, radius)
                    turn += 1
                    turn = turn % 2

            if draw_game(game_board):
                label = display_font.render("\t\t\t\t\tDraw!!", 1, purple)
                screen.blit(label, (20, 10))
                game_over = True

        # Display "Press R to play again or Q to quit" text
        play_again_font = pygame.font.SysFont("monospace", 30, bold=True)
        play_again_label = play_again_font.render("Press P-Play Again or R-Return", 1, grey)
        play_again_rect = play_again_label.get_rect(center=(width // 2, height - square_size // 2))
        screen.blit(play_again_label, play_again_rect)
        pygame.display.update()
        # Handle closing windows manually
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Restart the game or Quit the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        connect_four_extreme_mode()
                    if event.key == pygame.K_r:
                        show_start_menu()

    # Start the game
    gameplay()


# Main function:
def main():
    main_menu()


# Start the program
main()
