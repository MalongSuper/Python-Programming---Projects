# Chatbot app with popup window
import customtkinter as ctk
from PIL import Image, ImageTk
import time
from ChatbotResponses import get_response
# The ChatbotResponses.py gets user's input then
# Returns a response


# Load and resize icons
def load_resized_icon(image_path, size=(30, 30)):
    image = Image.open(image_path)
    image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(image)


# Handle user input and display response
def on_response(entry_field, output_frame, user_icon, chatbot_icon):
    user_input = entry_field.get().lower()

    # User message
    user_frame = ctk.CTkFrame(output_frame, fg_color="gray", corner_radius=10)
    user_frame.pack(side="top", fill="x", pady=5)

    user_label = ctk.CTkLabel(user_frame, text=" " + user_input.capitalize(), image=user_icon,
                              compound="left", anchor="w", wraplength=500)
    user_label.pack(side="left", padx=10, fill="x", expand=True)
    # Simulate delay
    chat_response = get_response(user_input)
    time.sleep(2)
    # Chatbot message
    chatbot_frame = ctk.CTkFrame(output_frame, fg_color="blue", corner_radius=10)
    chatbot_frame.pack(side="top", fill="x", pady=5)
    chatbot_label = ctk.CTkLabel(chatbot_frame, text=" " + chat_response, image=chatbot_icon,
                                 compound="left", anchor="w", wraplength=500)
    chatbot_label.pack(side="left", padx=10, fill="x", expand=True)
    entry_field.delete(0, 'end')


# Load chatbot UI into a popup window
def load_chatbot_interface(parent_window, back_to_control_panel):
    # Load icons
    user_icon = load_resized_icon('Images/user_icon.png')
    chatbot_icon = load_resized_icon('Images/Chatbot.png')
    back_icon = load_resized_icon('Images/iPhone-Home-Button.png')
    # Input frame
    entry_frame = ctk.CTkFrame(parent_window, bg_color='black', border_width=0)
    entry_frame.pack(side="top", pady=5)

    entry_field = ctk.CTkEntry(entry_frame, placeholder_text="Message Chatbot",
                               width=400, border_width=1, corner_radius=10)
    entry_field.grid(row=0, column=0, padx=10)

    button_field = ctk.CTkButton(entry_frame, text="Send", bg_color="black",
                                 width=100, border_width=0, corner_radius=5,
                                 command=lambda: on_response(entry_field, output_frame, user_icon, chatbot_icon))
    button_field.grid(row=0, column=1, padx=10)

    # Output frame
    output_frame = ctk.CTkFrame(parent_window)
    output_frame.pack(side="top", pady=10, padx=20, fill="both", expand=True)

    # Back button
    back_button = ctk.CTkButton(
        parent_window,
        image=back_icon,
        command=lambda: [reset_chatbot(entry_field, output_frame), back_to_control_panel()],
        width=30, height=30, border_width=0, corner_radius=10,
        text="", fg_color="transparent", hover_color="blue")
    back_button.pack(side="bottom", pady=10)


# Reset the chatbot state
def reset_chatbot(entry_field, output_frame):
    entry_field.delete(0, 'end')
    for widget in output_frame.winfo_children():
        widget.destroy()


# Set background image on a frame or window
def set_background(widget, image_path):
    bg_image = Image.open(image_path)
    bg_ctk_image = ctk.CTkImage(bg_image, size=(600, 600))
    bg_label = ctk.CTkLabel(widget, image=bg_ctk_image, text="")
    bg_label.image = bg_ctk_image
    bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)


# Start the main app
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Chatbot App")
    app.geometry("600x600")
    app.resizable(False, False)

    # Load the image using PIL
    icon_image = Image.open("Images/Chatbot.png")
    # Convert to PhotoImage
    icon_photo = ImageTk.PhotoImage(icon_image)
    # Set the icon
    app.iconphoto(True, icon_photo)

    # --- Welcome Frame ---
    welcome_frame = ctk.CTkFrame(app)
    welcome_frame.pack(fill="both", expand=True)
    set_background(welcome_frame, "Images/Background.jpg")

    welcome_label = ctk.CTkLabel(welcome_frame, text="Welcome to Chatbot",
                                 font=ctk.CTkFont(size=24, weight="bold"),
                                 text_color="white", fg_color="transparent",
                                 bg_color="transparent", corner_radius=0)
    welcome_label.pack(pady=80)

    # Show the chatbot popup
    def show_chatbot_interface():
        chatbot_popup = ctk.CTkToplevel()
        chatbot_popup.title("Chatbot Interface")
        chatbot_popup.geometry("600x600")

        set_background(chatbot_popup, "Images/Background.jpg")

        def back_to_control_panel():
            chatbot_popup.destroy()
            welcome_frame.pack(fill="both", expand=True)

        load_chatbot_interface(chatbot_popup, back_to_control_panel)
        welcome_frame.pack_forget()

    continue_button = ctk.CTkButton(welcome_frame, text="Continue", font=ctk.CTkFont(size=16),
                                    corner_radius=10, width=200, height=40,
                                    command=show_chatbot_interface)
    continue_button.pack(pady=30)

    # Add chatbot image under the continue button
    chatbot_img = Image.open("Images/Chatbot.png")
    chatbot_img = chatbot_img.resize((100, 100), Image.LANCZOS)
    chatbot_ctk_image = ctk.CTkImage(chatbot_img, size=(100, 100))

    chatbot_img_label = ctk.CTkLabel(welcome_frame, image=chatbot_ctk_image, text="",
                                     fg_color="transparent",  bg_color="transparent", corner_radius=0)
    chatbot_img_label.image = chatbot_ctk_image  # Keep a reference
    chatbot_img_label.pack(pady=10)
    # Chatbot Lines
    chatbot_label = ctk.CTkLabel(welcome_frame, text="Hello, my name is Romax. How can I help you today?",
                                 font=ctk.CTkFont(size=20, weight="bold"),
                                 text_color="white", fg_color="transparent",
                                 bg_color="transparent", corner_radius=0)
    chatbot_label.pack(pady=40)
    # Run the app
    app.mainloop()
