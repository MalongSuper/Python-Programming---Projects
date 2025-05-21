# Connect Four by CustomTkinter
import customtkinter as ctk
import numpy as np
import random
import time
import math
from PIL import Image, ImageTk

# Indicate number of columns and rows for board
row_board = 6
column_board = 7
player_piece = 1
computer_piece = 2
# Add global variable for game status
game_over = False


def load_resized_icon(image_path, size=(30, 30)):
    image = Image.open(image_path)
    image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(image)


def connect_four(connectfour_frame, back_to_control_panel):  # Create a game with CPU
    # Implement Minimax Algorithm
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

    def draw_board(board):
        canvas.delete("all")  # Clear previous drawings
        circle_radius = 30
        for row in range(row_board):
            for col in range(column_board):
                color = "black" if board[row][col] == 0 else ("red" if board[row][col] == player_piece else "yellow")
                canvas.create_oval(
                    col * cell_size + (cell_size - 2 * circle_radius) // 2,  # Adjust X position to center
                    (row_board - row - 1) * cell_size + (cell_size - 2 * circle_radius) // 2,
                    # Adjust Y position to center
                    (col + 1) * cell_size - (cell_size - 2 * circle_radius) // 2,  # Adjust X position to center
                    (row_board - row) * cell_size - (cell_size - 2 * circle_radius) // 2,
                    # Adjust Y position to center
                    fill=color)

    def click(event):  # Upon the user's interaction
        global game_over
        if game_over:
            return
        col = event.x // cell_size
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, player_piece)
            draw_board(board)
            if winning_game(board, player_piece):
                label.configure(text="Player Wins!")
                game_over = True
                return
            elif draw_game(board):
                label.configure(text="Draw Game!")
                game_over = True
                return
            # Apply the Minimax algorithm for the CPU
            col, _ = minimax(board, 4, True)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, computer_piece)
            draw_board(board)
            if winning_game(board, computer_piece):
                label.configure(text="Computer Wins!")
                game_over = True
            elif draw_game(board):
                label.configure(text="Draw Game!")
                game_over = True

    # Define cell size and canvas for the board
    cell_size = 80
    canvas = ctk.CTkCanvas(connectfour_frame, width=column_board * cell_size,
                           height=row_board * cell_size, bg="#0147AB")
    canvas.pack(pady=25)
    # Center the canvas in the window
    canvas.place(relx=0.5, rely=0.5, anchor="center")
    # Add click event listener
    canvas.bind("<Button-1>", click)
    # Initialize game board
    board = create_board()
    draw_board(board)
    # Add status label
    label = ctk.CTkLabel(connectfour_frame, text="Click to make a move")
    label.pack()
    # Load the back button image
    back_icon = load_resized_icon('Images/iPhone-Home-Button.png', (30, 30))  # Path to back icon
    # Add the "Back to Control Panel" button with an image (no text, no borders) using pack
    back_button = ctk.CTkButton(
        connectfour_frame,
        image=back_icon,  # Set the image for the button
        # Function to go back to control panel, also reset the game state
        command=lambda: [reset_game(board, label), back_to_control_panel()],
        width=30,  # Set the width of the button
        height=30,  # Set the height of the button
        border_width=0,  # Remove the border width
        corner_radius=10,  # Optional: for rounded corners
        text="",  # Remove any text from the button
        fg_color="transparent",  # Make background transparent
        hover_color="blue"  # Ensure no hover color is applied
    )

    # Use pack to position the button at the bottom of the frame (chatbot_frame)
    back_button.pack(side="bottom", pady=10)  # Use side="bottom" to position it at the bottom of the chatbot frame

    # Function to reset the game when exiting
    def reset_game(board, label):
        global game_over
        game_over = False  # Reset game over status
        board[:] = 0  # Reset the game board to a new empty state
        label.configure(text="Click to make a move")  # Reset the status label
        draw_board(board)  # Redraw the board to its initial empty state


if __name__ == "__main__":
    # Set appearance and theme (optional)
    ctk.set_appearance_mode("dark")  # "light" or "dark"
    app = ctk.CTk()
    app.title("Connect Four")
    app.geometry("600x600")
    app.resizable(False, False)
    app.configure(bg="light blue")

    # Load the image using PIL
    icon_image = Image.open("Images/ConnectFour.png")
    # Convert to PhotoImage
    icon_photo = ImageTk.PhotoImage(icon_image)
    # Set the icon
    app.iconphoto(True, icon_photo)

    # --- Welcome Frame ---
    welcome_frame = ctk.CTkFrame(app)
    welcome_frame.pack(fill="both", expand=True)
    welcome_label = ctk.CTkLabel(welcome_frame, text="Connect Four",
                                 font=ctk.CTkFont(size=24, weight="bold"),
                                 text_color="white", fg_color="transparent",
                                 bg_color="transparent", corner_radius=0)
    welcome_label.pack(pady=50)

    # Add chatbot image under the continue button
    connect_img = Image.open("Images/ConnectFour.png")
    connect_img = connect_img.resize((100, 100), Image.LANCZOS)
    connect_ctk_image = ctk.CTkImage(connect_img, size=(200, 200))

    connect_img_label = ctk.CTkLabel(welcome_frame, image=connect_ctk_image, text="",
                                     fg_color="transparent", bg_color="transparent", corner_radius=0)
    connect_img_label.image = connect_ctk_image  # Keep a reference
    connect_img_label.pack(pady=40)


    def show_connect_interface():
        connect_popup = ctk.CTkToplevel()
        connect_popup.title("Connect Four Gameplay")
        connect_popup.geometry("600x600")
        connect_popup.resizable(False, False)

        def back_to_control_panel():
            connect_popup.destroy()
            welcome_frame.pack(fill="both", expand=True)

        connect_four(connect_popup, back_to_control_panel)
        welcome_frame.pack_forget()


    play_button = ctk.CTkButton(welcome_frame, text="Play", font=ctk.CTkFont(size=16),
                                corner_radius=10, width=200, height=40,
                                command=show_connect_interface)
    play_button.pack(pady=30)

    # Run the app
    app.mainloop()
