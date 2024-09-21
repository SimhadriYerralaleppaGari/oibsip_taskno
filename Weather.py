import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import io

# OpenWeatherMap API Key
API_KEY = 'a6e785fdf7bb528f38e520429dca5a3d'

# Function to get weather data
import requests

def get_weather(city, units='metric'):
    API_KEY = 'a6e785fdf7bb528f38e520429dca5a3d'  # Use your API key here
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units={units}&appid={API_KEY}"
    response = requests.get(url)
    data = response.json()

    # Check for invalid API key or any error
    if data['cod'] == 401:
        print("Invalid API key. Please check it.")
        return None
    return data


def display_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city")
        return
    
    units = "metric" if unit_var.get() == "Celsius" else "imperial"
    weather_data = get_weather(city, units)
    
    if weather_data:
        city_name = weather_data['name']
        temp = weather_data['main']['temp']
        weather_desc = weather_data['weather'][0]['description'].title()
        wind_speed = weather_data['wind']['speed']
        icon_code = weather_data['weather'][0]['icon']
        
        # Update the labels
        location_label.config(text=f"Location: {city_name}")
        temp_label.config(text=f"Temperature: {temp}°{unit_var.get()[0]}")
        weather_label.config(text=f"Condition: {weather_desc}")
        wind_label.config(text=f"Wind Speed: {wind_speed} m/s")
        
        # Try to load and display weather icon
        try:
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
            icon_response = requests.get(icon_url)
            icon_response.raise_for_status()  # Check for HTTP errors
            
            # Convert image data into an image object
            icon_img = Image.open(io.BytesIO(icon_response.content))
            icon_photo = ImageTk.PhotoImage(icon_img)
            
            # Update icon on the label
            icon_label.config(image=icon_photo)
            icon_label.image = icon_photo  # Keep reference to prevent garbage collection
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load weather icon: {e}")

# Initialize the GUI
root = tk.Tk()
root.title("Weather App")
root.geometry("400x300")

# City Entry
tk.Label(root, text="Enter City:").pack(pady=10)
city_entry = tk.Entry(root)
city_entry.pack(pady=5)

# Temperature Unit Option
unit_var = tk.StringVar(value="Celsius")
tk.Label(root, text="Select Temperature Unit:").pack(pady=5)
tk.Radiobutton(root, text="Celsius", variable=unit_var, value="Celsius").pack()
tk.Radiobutton(root, text="Fahrenheit", variable=unit_var, value="Fahrenheit").pack()

# Display Weather Button
tk.Button(root, text="Get Weather", command=display_weather).pack(pady=10)

# Weather Info Labels
location_label = tk.Label(root, text="Location: ", font=("bold", 14))
location_label.pack()

temp_label = tk.Label(root, text="Temperature: ", font=("bold", 14))
temp_label.pack()

weather_label = tk.Label(root, text="Condition: ", font=("bold", 14))
weather_label.pack()

wind_label = tk.Label(root, text="Wind Speed: ", font=("bold", 14))
wind_label.pack()

# Weather Icon Display
icon_label = tk.Label(root)
icon_label.pack(pady=10)

# Start the GUI loop
root.mainloop()
