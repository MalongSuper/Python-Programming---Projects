# Number Conversion
from tkinter import *
from tkmacosx import CircleButton


# Convert numbers to decimal, binary, hexadecimal, octal, and alpha code
def decimal_number(number):
    return number


def binary_number(number):
    return bin(number)[2:]


def hexa_number(number):
    return hex(number)[2:].upper()


def octal_number(number):
    return oct(number)[2:]


def alpha_code(number):
    if number == 0:
        return "None"  # Return "None" for input 0
    if number == 1412:
        return "KID"  # Return "KID" for input 1412
    # Rules: 1-A, 2-B,..., 26-Z
    string_number = str(number)
    alphabet_list = {x: chr(64 + x) for x in range(1, 27)}
    value_list = []
    try:
        for i in range(0, len(string_number), 2):
            o = string_number[i:i + 2]
            if int(o) > 26:
                p = int(o) // 10
                q = int(o) % 10
                value_list.append(alphabet_list.get(int(p)))
                value_list.append(alphabet_list.get(int(q)))
            else:
                value_list.append(alphabet_list.get(int(o)))
    except (ValueError, IndexError):
        return "None"  # Return "None" for any conversion errors
    return ''.join(filter(None, value_list))  # Join valid characters, filtering out None


def convert():
    try:
        number = int(num_entry.get())
        decimal_result = decimal_number(number)
        binary_result = binary_number(number)
        hexa_result = hexa_number(number)
        octal_result = octal_number(number)
        alpha_result = alpha_code(number)
        # Change the entry to "normal" to add the result
        decimal_entry.config(state="normal", fg="yellow")
        binary_entry.config(state="normal", fg="yellow")
        hexa_entry.config(state="normal", fg="yellow")
        octal_entry.config(state="normal", fg="yellow")
        alpha_entry.config(state="normal", fg="yellow")
        # Display the result
        # delete(): Clear the existing text in the entry; insert(): Add new entry
        # This is necessary to avoid the new result appears but the old result still exists
        decimal_entry.delete(0, END)
        decimal_entry.insert(0, decimal_result)
        binary_entry.delete(0, END)
        binary_entry.insert(0, binary_result)
        hexa_entry.delete(0, END)
        hexa_entry.insert(0, hexa_result)
        octal_entry.delete(0, END)
        octal_entry.insert(0, octal_result)
        alpha_entry.delete(0, END)
        alpha_entry.insert(0, alpha_result)
        # Make the entries read-only
        decimal_entry.config(state="readonly")
        binary_entry.config(state="readonly")
        hexa_entry.config(state="readonly")
        octal_entry.config(state="readonly")
        alpha_entry.config(state="readonly")
    except ValueError:
        # Handle invalid input and display in red
        error_message = "Invalid input!!"
        decimal_entry.config(state="normal", fg="red")
        binary_entry.config(state="normal", fg="red")
        hexa_entry.config(state="normal", fg="red")
        octal_entry.config(state="normal", fg="red")
        alpha_entry.config(state="normal", fg="red")
        # Display error messages
        decimal_entry.delete(0, END)
        decimal_entry.insert(0, error_message)
        binary_entry.delete(0, END)
        binary_entry.insert(0, error_message)
        hexa_entry.delete(0, END)
        hexa_entry.insert(0, error_message)
        octal_entry.delete(0, END)
        octal_entry.insert(0, error_message)
        alpha_entry.delete(0, END)
        alpha_entry.insert(0, error_message)
        # Make the entries read-only
        decimal_entry.config(state="readonly")
        binary_entry.config(state="readonly")
        hexa_entry.config(state="readonly")
        octal_entry.config(state="readonly")
        alpha_entry.config(state="readonly")


# Create GUI
root = Tk()
root.title("Number Conversion")
root.geometry("600x600")
root['bg'] = "light yellow"
root.resizable(False, False)

# Create the frame to place the label and entry in the center
frame1 = Frame(root, bg="light yellow")
frame1.place(relx=0.5, rely=0.1, anchor="center")
frame2 = Frame(root, bg="light yellow")
frame2.place(relx=0.5, rely=0.5, anchor="center")

# Input number
title_label = Label(frame1, text="NUMBER CONVERSION", bg="light yellow", fg="black", font=("Helvetica", 20))
title_label.grid(row=1, column=5, padx=10, pady=10)

num_label = Label(frame2, text="Number", bg="light yellow", fg="black")
num_label.grid(row=3, column=2, padx=10, pady=10)
num_entry = Entry(frame2, bg="white", fg="purple", highlightbackground="black")
num_entry.grid(row=3, column=3, padx=10, pady=10)

decimal_label = Label(frame2, text="Decimal", bg="light yellow", fg="purple")
decimal_label.grid(row=4, column=2, padx=10, pady=10)
decimal_entry = Entry(frame2, bg="white", fg="yellow", highlightbackground="black", state=DISABLED)
decimal_entry.grid(row=4, column=3, padx=10, pady=10)

binary_label = Label(frame2, text="Binary", bg="light yellow", fg="purple")
binary_label.grid(row=5, column=2, padx=10, pady=10)
binary_entry = Entry(frame2, bg="white", fg="yellow", highlightbackground="black", state="readonly")
binary_entry.grid(row=5, column=3, padx=10, pady=10)

hexa_label = Label(frame2, text="Hexadecimal", bg="light yellow", fg="purple")
hexa_label.grid(row=6, column=2, padx=10, pady=10)
hexa_entry = Entry(frame2, bg="white", fg="yellow", highlightbackground="black", state="readonly")
hexa_entry.grid(row=6, column=3, padx=10, pady=10)

octal_label = Label(frame2, text="Octal", bg="light yellow", fg="purple")
octal_label.grid(row=7, column=2, padx=10, pady=10)
octal_entry = Entry(frame2, bg="white", fg="yellow", highlightbackground="black", state="readonly")
octal_entry.grid(row=7, column=3, padx=10, pady=10)

alpha_label = Label(frame2, text="Alpha Code", bg="light yellow", fg="purple")
alpha_label.grid(row=8, column=2, padx=10, pady=10)
alpha_entry = Entry(frame2, bg="white", fg="yellow", highlightbackground="black", state="readonly")
alpha_entry.grid(row=8, column=3, padx=10, pady=10)

convert_button = CircleButton(frame2, text="Convert", bg="pink", fg="red",
                              highlightbackground="light yellow", borderless=1, command=convert)
convert_button.grid(row=10, column=3, padx=10, pady=10)

# Run the code
root.mainloop()
