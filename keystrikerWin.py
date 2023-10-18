import tkinter as tk
from keystriker import keystriker
import subprocess

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.ks = keystriker()
        self.default_size = '800x600'
        self.master.geometry(self.default_size)

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.quit_button_handler)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("Hi there, everyone!")

    def quit_button_handler(self):
        self.stop()
        self.master.destroy()

    def start(self):
        self.ks.start()

    def stop(self):
        if self.ks is None:
            print('Nothing need to do here for now')
        else:
            self.ks.stop()
            print('main window stop')

root = tk.Tk()
app = Application(master=root)
app.mainloop()

