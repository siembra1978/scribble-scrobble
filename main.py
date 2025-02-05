# Written by siembra1978
import os
import pandas
import tkinter as tk
from tkinter import filedialog
import csvmanipulator

csvFile = None

class ScribbleScrobble(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Scribble Scrobble")
        self.geometry("450x50")

        self.label = tk.Label(self, text="Choose 'Apple Music Play Activity.csv' to convert to Scrobbable csv files")
        self.label.pack()

        #self.list = tk.Listbox(self, height=10, width=50)
        #self.list.pack(pady=20)

        self.button = tk.Button(self, text="Select CSV File", command=self.on_button_click)
        self.button.pack()

    def on_button_click(self):
        csvFile = filedialog.askopenfilename()
        print(csvFile)
        csvmanipulator.filterCSV(csvFile)
	    
if __name__ == "__main__":
    app = ScribbleScrobble()
    app.mainloop()
