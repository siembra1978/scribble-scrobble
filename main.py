# Written by siembra1978
import os
import pandas
import tkinter as tk

class ScribbleScrobble(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scribble Scrobble")
        self.geometry("640x460")

        self.list = tk.Listbox(self, height=10, width=50)
        self.list.pack(pady=20)

        self.button = tk.Button(self, text="awkward", command=self.on_button_click)
        self.button.pack()

    def on_button_click(self):
        print("yipee")

if __name__ == "__main__":
    app = ScribbleScrobble()
    app.mainloop()