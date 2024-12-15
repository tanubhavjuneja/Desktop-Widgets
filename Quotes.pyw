import sys
import time
import customtkinter as ctk
import os
import tkfilebrowser
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QFrame, QPushButton
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer
import json
time.sleep(1)
previous_quote = {"quote": None, "author": None}
quote=None
author=None
def read_file_location():
    global mfl
    try:
        file = open('assets/file_location.txt', 'r')
        mfl = file.read().strip()
        file.close()
        if not os.path.isfile(os.path.join(mfl, 'assets/icon.ico')):
            get_file_location()
    except FileNotFoundError:
        get_file_location()
def get_file_location():
    global main
    main = ctk.CTk()
    main.geometry("200x50+860+420")
    main.attributes('-topmost', True)
    main.attributes("-alpha", 100.0)
    main.lift()
    file_button = ctk.CTkButton(main, text="Select File Location", command=select_file_location, width=1)
    file_button.pack(pady=10)
    main.mainloop()
def select_file_location():
    global main
    mfl = str(tkfilebrowser.askopendirname())
    mfl = mfl.replace('\\', '/')
    file = open('assets/file_location.txt', 'w')
    file.write(mfl)
    file.close()
    main.destroy()
    read_file_location()
class QuoteWidget:
    def __init__(self):
        global mfl
        self.app = QApplication(sys.argv)
        self.window = QLabel()
        self.app.setWindowIcon(QIcon(mfl + "assets/icon.ico"))
        self.window.setWindowFlags(Qt.FramelessWindowHint)
        self.window.setAttribute(Qt.WA_TranslucentBackground)
        self.window.setPixmap(QPixmap(mfl + "assets/paper.png").scaled(500, 500))
        self.window.resize(self.window.pixmap().size())
        self.window.move(1450, 1)
        self.frame = QFrame(self.window)
        self.frame.setGeometry(96, 64, 300, 380)
        self.frame.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.frame.setFixedWidth(300)
        self.quote_label = QLabel(self.frame)
        self.author_label = QLabel(self.frame)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_quote)
        self.timer.start(60000)
        store_button = QLabel(self.window)
        store_button.setPixmap(QPixmap(mfl+"assets/save.png").scaled(20, 20)) 
        store_button.setAlignment(Qt.AlignCenter)
        store_button.setStyleSheet("background-color: transparent;")
        store_button.move(store_button.width()+30, 70)
        store_button.mousePressEvent = self.store_quote
        previous_button = QLabel(self.window)
        previous_button.setPixmap(QPixmap(mfl+"assets/previous.png").scaled(20, 20)) 
        previous_button.setAlignment(Qt.AlignCenter)
        previous_button.setStyleSheet("background-color: transparent;")
        previous_button.move(previous_button.width()+5, 70)
        previous_button.mousePressEvent = self.show_previous_quote
        close_button = QLabel(self.window)
        close_button.setPixmap(QPixmap(mfl+"assets/close_1.png").scaled(40, 40)) 
        close_button.setAlignment(Qt.AlignCenter)
        close_button.setStyleSheet("background-color: transparent;")
        close_button.move(self.window.width() - close_button.width() - 40, 60)
        close_button.mousePressEvent = lambda event: sys.exit()
        self.window.show()
        self.update_quote()
        self.frame.mousePressEvent = self.update_quote
    def close_application():
        sys.exit()
    def update_quote(self, event=None):
        global previous_quote,quote,author
        while True:
            try:
                response = requests.get("https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en")
                response.raise_for_status()
                data = json.loads(response.text)
                previous_quote = {"quote": quote, "author": author}
                quote = "3 January - DSE\n15 January - DFBE\n24 January - DMS\n\n"+data["quoteText"]
                author = data["quoteAuthor"] or "Unknown"
                self.quote_label.setText(quote)
                self.quote_label.setFont(QFont("Arial", 16))
                self.quote_label.setWordWrap(True)
                self.quote_label.setAlignment(Qt.AlignCenter)
                self.quote_label.setFixedWidth(self.frame.width() - 20)
                self.quote_label.setStyleSheet("background-color: transparent; color: black;")
                self.author_label.setText("- " + author)
                self.author_label.setFont(QFont("Arial", 12))
                self.author_label.setAlignment(Qt.AlignRight)
                self.author_label.setStyleSheet("background-color: transparent; color: black;")
                self.quote_label.setGeometry(10, 20, self.frame.width() - 20, 300)
                self.author_label.setGeometry(10, 330, self.frame.width() - 20, 60)
                break
            except (requests.RequestException, json.JSONDecodeError):
                continue
    def show_previous_quote(self,event=None):
        global previous_quote
        if quote and previous_quote["quote"] and author is not None:
            self.quote_label.setText(previous_quote["quote"])
            self.author_label.setText("- " + previous_quote["author"])
    def store_quote(self, event):
        global quote, author
        if quote and author is not None:
            with open('stored_quotes.txt', 'a') as file:
                file.write(f'Quote: {quote}\nAuthor: {author}\n\n')
                file.close()
            print("Quote stored successfully!")
    def run(self):
        sys.exit(self.app.exec_())
if __name__ == "__main__":
    read_file_location()
    widget = QuoteWidget()
    widget.window.setWindowFlags(Qt.Window | Qt.Tool | Qt.FramelessWindowHint)
    widget.window.show()
    widget.run()