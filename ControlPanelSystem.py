# This program creates a control panel system
import customtkinter as ctk
from PIL import Image, ImageTk


app = ctk.CTk()
app.title("Control Panel")
app.geometry("400x350")


# Applications
img = ctk.CTkImage(Image.open("Images/Chatbot.png"), size=(26, 26))
(ctk.CTkButton(app, text="Chatbot", image=img,
               width=90, compound="top").grid(row=10, column=1, padx=20, pady=20))


app.mainloop()
