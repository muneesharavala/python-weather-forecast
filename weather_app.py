import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import requests
import os
from datetime import datetime

# Replace with your OpenWeatherMap API key
API_KEY = "9b3cb4b2e1b9be19a5f1aa6e29a07538"

# Global for animation frames
bg_frames = []

def get_city_by_ip():
    try:
        response = requests.get("http://ip-api.com/json/").json()
        return response['city']
    except:
        return "London"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"

    try:
        data = requests.get(url).json()
        forecast_data = requests.get(forecast_url).json()

        if data.get("cod") != 200:
            result_label.config(text="City not found!")
            return

        weather = data['weather'][0]['main'].lower()
        description = data['weather'][0]['description'].title()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M:%S')
        sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M:%S')

        result = (
            f"Weather: {description}\n"
            f"Temp: {temp}°C\n"
            f"Humidity: {humidity}%\n"
            f"Wind: {wind} m/s\n"
            f"Sunrise: {sunrise}\n"
            f"Sunset: {sunset}"
        )
        result_label.config(text=result)

        update_animation(weather)
        update_background(weather)

        # Forecast
        forecast_text = ""
        for i in range(0, len(forecast_data['list']), 8):
            day = forecast_data['list'][i]
            date = datetime.fromtimestamp(day['dt']).strftime('%a %d')
            temp = day['main']['temp']
            desc = day['weather'][0]['description'].title()
            forecast_text += f"{date}: {temp}°C, {desc}\n"

        forecast_label.config(text=forecast_text.strip())

    except Exception as e:
        result_label.config(text=f"Error: {e}")

def update_animation(condition):
    gif_map = {
        "clear": "clear.gif",
        "clouds": "cloudy.gif",
        "rain": "rain.gif",
        "snow": "snow.gif",
        "thunderstorm": "storm.gif",
        "drizzle": "rain.gif",
        "mist": "cloudy.gif",
        "fog": "cloudy.gif",
        "haze": "cloudy.gif"
    }

    gif_file = gif_map.get(condition, "clear.gif")
    gif_path = os.path.join("assets", gif_file)
    print(f"Weather Icon Animation: {gif_path}")  # Debug

    try:
        img = Image.open(gif_path)
        frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(img)]

        def update(index):
            frame = frames[index]
            animation_label.config(image=frame)
            animation_label.image = frame
            root.after(100, update, (index + 1) % len(frames))

        update(0)

    except Exception as e:
        print(f"Error loading animation: {e}")

def update_background(condition):
    global bg_frames
    bg_map = {
        "clear": "clear.gif",
        "clouds": "cloudy.gif",
        "rain": "rain.gif",
        "snow": "snow.gif",
        "thunderstorm": "storm.gif",
        "drizzle": "rain.gif",
        "mist": "cloudy.gif",
        "fog": "cloudy.gif",
        "haze": "cloudy.gif"
    }

    gif_file = bg_map.get(condition, "clear.gif")
    gif_path = os.path.join("assets", gif_file)
    print(f"Background Animation: {gif_path}")  # Debug

    try:
        img = Image.open(gif_path)
        bg_frames = [ImageTk.PhotoImage(frame.copy().resize((400, 600))) for frame in ImageSequence.Iterator(img)]

        def animate_bg(index):
            frame = bg_frames[index]
            bg_label.config(image=frame)
            bg_label.image = frame
            root.after(100, animate_bg, (index + 1) % len(bg_frames))

        animate_bg(0)

    except Exception as e:
        print(f"Error loading background animation: {e}")

# GUI Setup
root = tk.Tk()
root.title("Advanced Weather App")
root.geometry("400x600")
root.resizable(False, False)

# Background Layer
bg_label = tk.Label(root)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Input
city_entry = tk.Entry(root, font=("Arial", 14), justify="center")
city_entry.place(relx=0.5, rely=0.05, anchor="n", width=250)

search_btn = tk.Button(root, text="Get Weather", font=("Arial", 12, "bold"), command=lambda: get_weather(city_entry.get()))
search_btn.place(relx=0.5, rely=0.13, anchor="n")

# Weather Icon Animation
animation_label = tk.Label(root, bg="lightblue")
animation_label.place(relx=0.5, rely=0.25, anchor="n")

# Weather Result
result_label = tk.Label(root, font=("Arial", 12), bg="lightblue", justify="left")
result_label.place(relx=0.5, rely=0.5, anchor="n")

# Forecast Section
tk.Label(root, text="5-Day Forecast:", font=("Arial", 12, "bold"), bg="lightblue").place(relx=0.5, rely=0.7, anchor="n")
forecast_label = tk.Label(root, font=("Arial", 10), bg="lightblue", justify="left")
forecast_label.place(relx=0.5, rely=0.75, anchor="n")

# Auto-fetch on load
detected_city = get_city_by_ip()
city_entry.insert(0, detected_city)
get_weather(detected_city)

root.mainloop()
# Ensure the assets directory exists
if not os.path.exists("assets"):
    os.makedirs("assets")
    