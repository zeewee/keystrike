import datetime
from collections import defaultdict
import os
import time

from pynput import keyboard, mouse
import matplotlib.pyplot as plt

class keystriker():
    def __init__(self):
        self.desc = 'a simple tool to record key strike'
        self.KEYS = defaultdict(int)
        self.MOUSE_BUTTONS = defaultdict(int)
        self.DATA_FILE = 'key_log.txt'
        self.start_logging = True
        self.logger_period = 5 # in seconds
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
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.DATA_FILE, 'a') as f:
            f.write(f'{current_time},{sum(self.KEYS.values())},{sum(self.MOUSE_BUTTONS.values())}\n')
        self.KEYS.clear()
        self.MOUSE_BUTTONS.clear()

    def logging(self):
        with keyboard.Listener(on_press=self.on_press) as k_listener, \
                mouse.Listener(on_click=self.on_click) as m_listener:
            print('debug: start logging')
            while self.start_logging is True:
                try:
                    time.sleep(self.logger_period)
                    self.log_data()
                except KeyboardInterrupt:
                    print('keyboard interrupt, exit')
                    break
            print('logging stopped')

    def start(self):
        if self.start_logging is False:
            self.start_logging = True
            print('change start_logging, False -> True')
            self.logging()
        else:
            print('already start, nothing need to do')
            return

    def stop(self):
        self.start_logging = False
        print('set start_logging to False')

def generate_chart(time_unit):
    data = defaultdict(int)
    with open(DATA_FILE, 'r') as f:
        for line in f:
            date_time_str, keys, mouse_buttons = line.strip().split(',')
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
            if time_unit == 'hour':
                time_key = date_time_obj.strftime('%Y-%m-%d %H')
            elif time_unit == 'day':
                time_key = date_time_obj.strftime('%Y-%m-%d')
            else:
                time_key = date_time_obj.strftime('%Y-%m-%d %H:%M')
            data[time_key] += int(keys) + int(mouse_buttons)
    x, y = zip(*data.items())
    plt.plot(x, y)
    plt.xlabel(f'Time ({time_unit.capitalize()})')
    plt.ylabel('Number of Key/Mouse Clicks')
    plt.title(f'Key/Mouse Clicks per {time_unit.capitalize()}')
    plt.show()

#if __name__ == '__main__':
#    with keyboard.Listener(on_press=on_press) as k_listener, \
#         mouse.Listener(on_click=on_click) as m_listener:
#        while True:
#            try:
#                time.sleep(60)
#                log_data()
#            except KeyboardInterrupt:
#                break
#    generate_chart('minute')

