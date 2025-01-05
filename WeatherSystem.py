# This program simulates Weather System
import tkinter as tk
import requests
from PIL import Image, ImageTk
from datetime import datetime

# Main screen
root = tk.Tk()
root.title("Weather System")
root.geometry("600x500")
root.resizable(False, False)


# Key: 0fecc68658de6ebc1257a738a307885b
# API url: api.openweathermap.org/data/2.5/weather?q={city name}&appid={API key}
def format_response(weather):  # Weather responses
    try:
        city = weather['name']
        con = weather['sys']['country']
        lon, lat = weather['coord']['lon'], weather['coord']['lat']
        cond = weather['weather'][0]['description']
        temp = weather['main']['temp']
        min_temp = weather['main']['temp_min']
        max_temp = weather['main']['temp_max']
        fl = weather['main']['feels_like']
        pre = weather['main']['pressure']
        hum = weather['main']['humidity']
        sea = weather['main']['sea_level']
        grn = weather['main']['grnd_level']
        vis = weather['visibility']
        sr, ss = weather['sys']['sunrise'], weather['sys']['sunset']
        # Display all the strings
        final_str = ("City: %s\nCountry: %s\nCoordinate: [%2f, %2f]\nCondition: %s"
                     "\nTemperature: %s\tFeels Like: %s\nHighest: %s\tLowest: "
                     "%s\nPressure: %s\nHumidity: %s\nSea Level: %s\tGround Level: "
                     "%s\nVisibility: %s\nSunrise: %s\tSunset: %s"
                     % (city, con, lon, lat, cond.capitalize(),
                        temp, fl, max_temp, min_temp, pre, hum, sea, grn, vis, sr, ss))
    except KeyError:  # If the city is not found
        final_str = "City not found"
    return final_str


def open_image(icon):
    size = int(frame_two.winfo_height() * 0.2)
    image = ImageTk.PhotoImage(Image.open('Images/Weather_icons/'+icon+'.png').resize((size, size)))
    weather_icon.delete('all')
    weather_icon.create_image(0, 0, image=image, anchor="nw")
    weather_icon.image = image


def get_weather(city):
    weather_key = "0fecc68658de6ebc1257a738a307885b"
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"APPID": weather_key, 'q': city, 'units': 'imperial'}
    response = requests.get(url, params)
    # Return the weather information
    weather = response.json()  # response.json() returns weather information
    print(weather)  # Print the weather in the output to get further information
    result['text'] = format_response(weather)
    icon = weather['weather'][0]['icon']
    open_image(icon)


def update_time():  # Get the current time
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")  # Format the date and time
    time_label.config(text=current_time)  # Update the label text
    root.after(1000, update_time)  # Update every second


# Add background for the screen
img = Image.open("Images/weatherbackground.png")
img.resize((600, 500), Image.LANCZOS)
image = ImageTk.PhotoImage(img)
label = tk.Label(root, image=image)
label.place(x=0, y=0, width=600, height=500)

# Create the time label
time_label = tk.Label(root, font=('Calibri', 14), bg="black", fg="white")
time_label.place(relx=0.5, y=10, anchor='center')  # Position the label above the entry box
# Start the time update
update_time()

# Create the frame for entry box
frame_one = tk.Frame(root, bg="#42c2f4", bd=5)
frame_one.place(x=80, y=50, width=450, height=60)
# Create the entry box
entry_box = tk.Entry(frame_one, font=('Calibri', 25), width=16,
                     bg="white", fg="black")
entry_box.grid(row=0, column=0, sticky="w")
# Create the find button
button = tk.Button(frame_one, text="Get Weather", width=11, height=2,
                   font=("Calibri", 15, 'bold'), bg="white", fg="green",
                   highlightbackground="white",
                   command=lambda: get_weather(entry_box.get()))  # Get the value from the entry box
button.grid(row=0, column=1, padx=10)

# Get frame for the weather information
frame_two = tk.Frame(root, bg="#42c2f4", bd=5)
frame_two.place(x=80, y=120, width=450, height=300)

# Result Frame
result = tk.Label(frame_two, font=('Calibri', 16), bg="white", fg="black", justify='left', anchor="center")
result.place(relwidth=1, relheight=1)

# Weather icon
weather_icon = tk.Canvas(result, bg='white', bd=0, highlightthickness=0)
weather_icon.place(relx=0.8, rely=0.02, relwidth=1, relheight=0.5)

# Create the heading information
inform = tk.Label(root, text="Earth consists of over 200 countries and 200.000 cities!",
                  font=('Calibri', 15), fg="red", bg="light grey")
inform.place(x=120, y=430)

root.mainloop()
