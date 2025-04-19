from tkinter import *
import random

# Global variables
characters = ["x", "o"]
player = random.choice(characters)
buttons = [[None for _ in range(3)] for _ in range(3)]
label = None


def restart():
    global player
    player = random.choice(characters)
    label.config(text=player + " 's turn", fg="white")
    for row in range(3):
        for column in range(3):
            buttons[row][column].config(text="", fg="black", highlightbackground="black", highlightthickness=0)


def next_turn(row, column):
    global player

    if buttons[row][column]['text'] == "" and check_winner()[0] is False:
        buttons[row][column]['text'] = player
        buttons[row][column]['fg'] = "blue" if player == "x" else "red"
        result, winning_cells = check_winner()
        if result is False:
            player = characters[0] if player == characters[1] else characters[1]
            label.config(text=player + " 's turn", fg="white")
        elif result is True:
            label.config(text=player + " wins!", fg="blue" if player == "x" else "red")
            # Highlight winning buttons
            color = "blue" if player == "x" else "red"
            for r, c in winning_cells:
                buttons[r][c].config(highlightbackground=color, highlightthickness=4)
        elif result == "Draw":
            label.config(text="Draw!", fg="yellow")


def check_winner():
    # Check rows
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != '':
            return True, [(row, 0), (row, 1), (row, 2)]
    # Check columns
    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != '':
            return True, [(0, column), (1, column), (2, column)]
    # Diagonals
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != '':
        return True, [(0, 0), (1, 1), (2, 2)]
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != '':
        return True, [(0, 2), (1, 1), (2, 0)]
    # Draw
    if empty_spaces() is False:
        return "Draw", []
    return False, []


def empty_spaces():
    for row in range(3):
        for column in range(3):
            if buttons[row][column]['text'] == '':
                return True
    return False


def make_move(r, c):
    return lambda: next_turn(r, c)


def main():
    global label, buttons

    board = Tk()
    board.title("Tic-Tac-Toe")

    label = Label(text=player + " 's turn", font=("helvetica", 40))
    label.pack(side="top")

    new_game_button = Button(text="New Game",
                             font=("helvetica", 20), command=restart)
    new_game_button.pack(side="top")

    frame = Frame(board)
    frame.pack()

    for row in range(3):
        for column in range(3):
            buttons[row][column] = Button(frame, text="", font=('consolas', 40), width=5, height=2,
                                          command=make_move(row, column))
            buttons[row][column].grid(row=row, column=column)

    board.mainloop()


main()
