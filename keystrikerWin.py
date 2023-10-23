import tkinter as tk
from keystriker import keystriker
from multiprocessing import Process, Pipe
from pynput import keyboard, mouse
from collections import defaultdict
import datetime
import time

class keystriker():
    def __init__(self):
        self.desc = 'a simple tool to record key strike'
        self.KEYS = defaultdict(int)
        self.MOUSE_BUTTONS = defaultdict(int)
        self.DATA_FILE = 'key_log.txt'
        self.logger_period = 5   # seconds
        print('keystriker init done')

    def on_press(self, key):
        try:
            self.KEYS[key.char] += 1
        except AttributeError:
            pass

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.MOUSE_BUTTONS[str(button)] += 1

    def log_data(self):
        current_time = datetime.datetime.now().isoformat()
        with open(self.DATA_FILE, 'a') as f:
            f.write(f'{current_time}, {sum(self.KEYS.values())},{sum(self.MOUSE_BUTTONS.values())}\n')
        self.KEYS.clear()
        self.MOUSE_BUTTONS.clear()

    def logging(self, conn):
        with keyboard.Listener(on_press=self.on_press) as k_listener, \
        mouse.Listener(on_click=self.on_click) as m_listener:
            print('debug: start logging')
            while True:
                try:
                    time.sleep(self.logger_period)
                    self.log_data()
                except KeyboardInterrupt:
                    print('keyboard interrupt, exit')
                    break
            print('logging stopped')

    def start(self):
        print('keystriker logging started')

    def stop(self):
        print('keystriker logging stopped')


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.default_size = '800x600'
        self.master.geometry(self.default_size)
        self.start()

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
        self.ks = keystriker()
        _, child_conn = Pipe()
        p = Process(target=self.ks.logging, args={child_conn,})
        p.daemon=True
        p.start()

    def stop(self):
        if self.ks is None:
            print('Nothing need to do here for now')
        else:
            self.ks.stop()
            print('main window stop')

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()

