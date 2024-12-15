import requests
import webbrowser
import pyautogui
import time
import sys
import customtkinter as ctk
from PIL import Image
import datetime
import os
import tkfilebrowser
from apscheduler.schedulers.background import BackgroundScheduler
def close_window():
    global scheduler,weather_window
    scheduler.shutdown(wait=False)
    time.sleep(0.1)
    weather_window.destroy()
    sys.exit()
def get_weather():
    global sent
    weather_api_key = '9bc99d2aca28c08cf29f9019b4637c02'
    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={weather_city},in&appid={weather_api_key}'
    response = requests.get(weather_url)
    weather_data = response.json()
    print(weather_data)
    icon_code=weather_data['weather'][0]['icon']
    icon_url = f"http://openweathermap.org/img/w/{icon_code}.png"
    response = requests.get(icon_url, stream=True)
    with open(mfl+"assets/weather_icon.png", "wb") as f:
        for chunk in response.iter_content(chunk_size=128):
            f.write(chunk)
    icon=ctk.CTkImage(Image.open(mfl+"assets/weather_icon.png"),size=(150,150))
    weather_icon.configure(image=icon)
    ist_offset = datetime.timedelta(hours=5, minutes=30)
    sunrise_datetime = datetime.datetime.utcfromtimestamp(weather_data['sys']['sunrise'])+ist_offset
    sunset_datetime = datetime.datetime.utcfromtimestamp(weather_data['sys']['sunset'])+ist_offset
    temperature = ((weather_data['main']['temp']- 273.15)//1)
    description = weather_data['weather'][0]['description']
    pressure=weather_data['main']['pressure']
    humidity=weather_data['main']['humidity']
    wind_speed=weather_data['wind']['speed']
    temperature_label.configure(text=f"{temperature} °C")
    description_label.configure(text=description)
    humidity_label.configure(text=f"{humidity} %")
    pressure_label.configure(text=f"{pressure} hPa")
    wind_speed_label.configure(text=f"{wind_speed} m/s")
    sunrise_label.configure(text=f"{sunrise_datetime.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    sunset_label.configure(text=f"{sunset_datetime.strftime('%Y-%m-%d %H:%M:%S UTC')}")
    if sent==False and 'cloud'in description.lower():
        pass
def get_romantic_quote():
    quote_url = 'https://api.quotable.io/random?tags=love'
    response = requests.get(quote_url)
    quote_data = response.json()
    return quote_data['content']
def send_quote():
    global sent
    romantic_quote = get_romantic_quote()
    url = "whatsapp://send?phone=7678312831"
    webbrowser.open(url)
    time.sleep(5)
    pyautogui.click(603, 1008)
    time.sleep(0.5)
    pyautogui.write(romantic_quote)
    time.sleep(0.5)
    pyautogui.click(1897, 1008)
    sent=True
def read_file_location():
    global mfl
    try:
        file=open('assets/file_location.txt', 'r')
        mfl = file.read().strip()
        file.close()
        if not os.path.isfile(os.path.join(mfl, 'assets/close.png')):
            get_file_location()
    except FileNotFoundError:
        get_file_location()
def get_file_location():
    global main
    main=ctk.CTk()
    main.geometry("200x50+860+420")
    main.attributes('-topmost', True)
    main.attributes("-alpha",100.0)
    main.lift()
    file_button = ctk.CTkButton(main, text="Select File Location",command=select_file_location,width=1)
    file_button.pack(pady=10)
    main.mainloop()
def select_file_location():
    global main
    mfl = str(tkfilebrowser.askopendirname())
    mfl = mfl.replace('\\', '/')
    file=open('assets/file_location.txt', 'w')
    file.write(mfl)
    file.close()
    main.destroy()
    read_file_location()
sent=False
read_file_location()
weather_city = 'Dehradun'
weather_window = ctk.CTk()
weather_window.title("Weather")
weather_window.geometry("400x290+1500+720")
weather_window.overrideredirect(True)
close_icon = ctk.CTkImage(Image.open(mfl + "assets/close.png"), size=(13, 13))
close_button = ctk.CTkButton(weather_window, image=close_icon, command=close_window, fg_color="gray14", text="", width=1)
close_button.place(relx=0.928, rely=0.01)
weather_label = ctk.CTkLabel(weather_window, text="Weather", font=("Arial", 20, "bold"))
weather_label.place(relx=0.05, rely=0.02)
weather_icon=ctk.CTkLabel(weather_window,image="",text="")
weather_icon.pack()
temperature_label=ctk.CTkLabel(weather_window, text="0 °C", font=("Arial", 20, "bold"))
description_label=ctk.CTkLabel(weather_window, text="Clear Sky", font=("Arial", 20, "bold"))
humidity_label=ctk.CTkLabel(weather_window, text="00 %", font=("Arial", 20, "bold"))
pressure_label=ctk.CTkLabel(weather_window, text="0 hPa", font=("Arial", 20, "bold"))
wind_speed_label=ctk.CTkLabel(weather_window, text="0 m/s", font=("Arial", 20, "bold"))
sunrise_label=ctk.CTkLabel(weather_window, text='%Y-%m-%d %H:%M:%S UTC', font=("Arial", 20, "bold"))
sunset_label=ctk.CTkLabel(weather_window, text='%Y-%m-%d %H:%M:%S UTC', font=("Arial", 20, "bold"))
temperature_label.pack()
description_label.pack()
humidity_label.pack()
pressure_label.pack()
wind_speed_label.pack()
sunrise_label.pack()
sunset_label.pack()
get_weather()
scheduler = BackgroundScheduler()
scheduler.add_job(get_weather,'interval', seconds=3600, max_instances=150)
scheduler.start()
weather_window.mainloop()