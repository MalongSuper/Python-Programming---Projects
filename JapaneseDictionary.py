import tkinter as tk
from tkinter import messagebox
import requests


# Function to query Jisho API
def search_word():
    word = entry.get()
    if not word:
        messagebox.showerror("Error", "Please enter a word to search")
        return

    try:
        response = requests.get(f"https://jisho.org/api/v1/search/words?keyword={word}")
        response.raise_for_status()
        data = response.json()
        if data['data']:
            meaning = data['data'][0]['senses'][0]['english_definitions']
            result = ', '.join(meaning)
            result_label.config(text=f"Meaning: {result}")
        else:
            result_label.config(text="No results found")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")


# Creating the main window
root = tk.Tk()
root.title("Japanese Dictionary")
root.resizable(False, False)

# Creating widgets
entry_label = tk.Label(root, text="Enter Japanese Word:")
entry_label.pack(pady=5)

entry = tk.Entry(root, width=40)
entry.pack(pady=5)

search_button = tk.Button(root, text="Search", command=search_word)
search_button.pack(pady=5)

result_label = tk.Label(root, text="", wraplength=300, justify="left")
result_label.pack(pady=10)

# Running the application
root.mainloop()
