# Create a simple music player
import pygame
import tkinter as tk
from tkinter.filedialog import askdirectory
import os
from mutagen.mp3 import MP3

# Main screen
window = tk.Tk()
window.title("Music Player")
window.geometry("700x500")
window.resizable(False, False)

directory = askdirectory()
os.chdir(directory)
song_list = os.listdir()
font = ("Verdana", 12, "bold")
is_paused = False  # Add this variable for the pausing status of the music

playlist = tk.Listbox(window, font=font,
                      fg="light blue", bg="grey", selectmode=tk.SINGLE)
playlist.pack(fill="both", expand=True)

# Populate the playlist
x = 0
for song in song_list:
    playlist.insert(x, song)
    x += 1

pygame.init()
pygame.mixer.init()


def update_duration(duration):  # Function to keep track of the current duration of the song
    if pygame.mixer.music.get_busy():
        # Get the current position in milliseconds
        current_position = pygame.mixer.music.get_pos() // 1000  # Convert it to second
        minutes, seconds = divmod(current_position, 60)
        total_minutes, total_seconds = divmod(duration, 60)
        # Update the label
        var3.set(f"{minutes: 02}: {seconds: 02} "
                 f"/ {total_minutes: 02}: {total_seconds: 02}")
        window.after(1000, update_duration, duration)  # Update every second


def play():  # Function to play the music
    global is_paused
    selected_song = playlist.get(tk.ACTIVE)
    # Make sure the selected file is mp3
    if selected_song.endswith(".mp3"):
        if is_paused:
            pygame.mixer.music.unpause()
            var1.set(playlist.get(tk.ACTIVE) + " is playing")
            is_paused = False
        else:
            pygame.mixer.music.load(playlist.get(tk.ACTIVE))
            var1.set(playlist.get(tk.ACTIVE) + " is playing")
            # Get the duration of the song
            audio = MP3(selected_song)
            total_duration = int(audio.info.length)  # Duration in seconds
            pygame.mixer.music.play()
            update_duration(total_duration)  # Update current duration
            is_paused = False
    else:
        var2.set("Invalid file name")


def pause():   # Function to pause the music while it is playing
    global is_paused
    pygame.mixer.music.pause()
    var1.set("Paused")
    is_paused = True


def resume():  # Function to resume the music after pausing it
    global is_paused
    if is_paused:
        pygame.mixer.music.unpause()
        var1.set(playlist.get(tk.ACTIVE) + " is playing")
        is_paused = False


def stop():  # Function to stop the music
    pygame.mixer.music.stop()
    # Clear the messages when stopped
    var1.set("")
    var2.set("")
    var3.set("")


# Create buttons
play_button = tk.Button(window, width=5, height=3, font=font, text="PLAY",
                        command=play, bg="light blue", fg="gold")
play_button.pack(fill="x")

pause_button = tk.Button(window, width=5, height=3, font=font, text="PAUSE",
                         command=pause, bg="light blue", fg="gold")
pause_button.pack(fill="x")

resume_button = tk.Button(window, width=5, height=3, font=font, text="RESUME",
                          command=resume, bg="light blue", fg="gold")
resume_button.pack(fill="x")

stop_button = tk.Button(window, width=5, height=3, font=font, text="STOP",
                        command=stop, bg="light blue", fg="gold")
stop_button.pack(fill="x")

var1 = tk.StringVar()
var2 = tk.StringVar()
var3 = tk.StringVar()
song_title = tk.Label(window, font=font, textvariable=var1, fg="white")
song_title.pack()
message_label = tk.Label(window, font=font, textvariable=var2, fg="red")
message_label.pack()
duration_label = tk.Label(window, font=font, textvariable=var3, fg="white")
duration_label.pack()

# Run the program
window.mainloop()
