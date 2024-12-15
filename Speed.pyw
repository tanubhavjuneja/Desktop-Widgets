import subprocess
import customtkinter as ctk
from PIL import Image 
import tkfilebrowser
import os
def close_window():
    speed_test.destroy()
def test(event):
    process = subprocess.Popen(["speedtest-cli", "--simple"], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    output = output.decode('utf-8')
    download_speed1 = float(output.split('\n')[2].split()[1])
    upload_speed1 = float(output.split('\n')[1].split()[1])
    ping_value = float(output.split('\n')[0].split()[1])
    download_label.configure(text=f"Download Speed\n\n{download_speed1:.2f} Mbps")
    upload_label.configure(text=f"Upload Speed\n\n{upload_speed1:.2f} Mbps")
    ping_label.configure(text=f"Ping\n\n{ping_value:.2f} ms")
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
read_file_location()
speed_test=ctk.CTk()
speed_test.title("Speed Test")
speed_test.geometry("400x290+1500+720")
speed_test.overrideredirect(True)
close_icon = ctk.CTkImage(Image.open(mfl + "assets/close.png"), size=(13, 13))
close_button = ctk.CTkButton(speed_test, image=close_icon, command=close_window, fg_color="gray14", text="", width=1)
close_button.place(relx=0.928, rely=0.01)
download_icon = ctk.CTkImage(Image.open(mfl + "assets/download.png"), size=(40, 40))
download_label = ctk.CTkLabel(speed_test,image=download_icon,compound=ctk.RIGHT, text="Download Speed\n\n___.__ Mbps", font=("Arial", 15, "bold"))
download_label.place(relx=0.1,rely=0.6)
upload_icon = ctk.CTkImage(Image.open(mfl + "assets/upload.png"), size=(40, 40))
upload_label = ctk.CTkLabel(speed_test, image=upload_icon,compound=ctk.RIGHT,text="Upload Speed\n\n___.__ Mbps", font=("Arial", 15, "bold"))
upload_label.place(relx=0.58,rely=0.6)
ping_icon = ctk.CTkImage(Image.open(mfl + "assets/ping.png"), size=(40, 40))
ping_label = ctk.CTkLabel(speed_test, image=ping_icon,compound=ctk.RIGHT,text="Ping\n\n___.__ ms", font=("Arial", 15, "bold"))
ping_label.place(relx=0.4,rely=0.25)
network_icon = ctk.CTkImage(Image.open(mfl + "assets/network.png"), size=(25, 25))
network_label = ctk.CTkLabel(speed_test, image=network_icon,compound=ctk.LEFT,text="  Network Speed",font=("Arial", 20, "bold"), fg_color="gray14", width=1)
network_label.bind("<Button-1>", test)
network_label.place(relx=0.03, rely=0.03)
test(None)
speed_test.mainloop()