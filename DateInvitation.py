# Date Invitation
import tkinter as tk
import random

CAT_IMAGE_PATH = r"Images/Cat1.gif.jpg"
SHY_CAT_IMAGE_PATH = r"Images/Cat2.gif.jpg"


def on_yes_click():
    # Change the cat image to a shy pose
    cat_image_shy = tk.PhotoImage(file=SHY_CAT_IMAGE_PATH)
    cat_label.configure(image=cat_image_shy)
    cat_label.image = cat_image_shy
    # Change the text in the question label with a larger font
    question_label.config(text="See you at 6 p.m.", font=("Helvetica", 16), fg="black")
    # Destroy the Yes and No buttons after click Yes
    yes_button.destroy()
    no_button.destroy()


def on_no_click():
    # Move the 'No' button to a random position within the window
    new_x = random.randint(0, window.winfo_reqwidth() - no_button.winfo_reqwidth())
    new_y = random.randint(0, window.winfo_reqheight() - no_button.winfo_reqheight())
    no_button.place(x=new_x, y=new_y)


# Create the main window
window = tk.Tk()
window.title("Date Invitation")
window.configure(bg='light pink')
window.resizable(width=False, height=False)  # Make the window not resizable

# Add the question label above the cat image with a larger font
question_label = tk.Label(window, text="Do you want to go out with me?", font=("Helvetica", 16),
                          bg='light pink', fg='black')
question_label.grid(row=0, column=0, pady=10)

# Add the initial cat image
initial_cat_image = tk.PhotoImage(file=CAT_IMAGE_PATH)
cat_label = tk.Label(window, image=initial_cat_image, bg='light pink')
cat_label.grid(row=1, column=0, pady=10)

# Create and place the 'yes' button with a pink background under the cat image
yes_button = tk.Button(window, text="Yes", command=on_yes_click, highlightbackground='light pink')
yes_button.grid(row=2, column=0, pady=10)

# Create and place the 'no' button with a blue background under the cat image
no_button = tk.Button(window, text="No", command=on_no_click, highlightbackground='light pink')
no_button.grid(row=3, column=0, pady=10)

# Add a label in the background to display the message
background_label = tk.Label(window, text="", font=("Helvetica", 12), bg='light pink')
background_label.grid(row=4, column=0, pady=10)

# Run the main loop
window.mainloop()
