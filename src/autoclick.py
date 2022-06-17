# threading needed to control the clicks
# so we inherit the class
import sys
import threading
import time
from pynput.mouse import Button, Controller

mouse = Controller()
delay_event = threading.Event()
exit_event = threading.Event()


class AutoClicker(threading.Thread):

    profile = []
    transactions = None
    repetitions = None
    button = None
    running = False
    app_running = True
    app_counter = 0
    time_between_repeats = 0
    status_msg = None

    def __init__(self, profile=[], repetitions=5):
        super(AutoClicker, self).__init__()
        self.button = Button.left
        self.profile = profile
        # self.transactions = transactions
        self.repetitions = repetitions

    def start_click(self):
        self.running = True

    def stop_click(self):
        self.running = False
        exit_event.set()

    def exit(self):
        self.stop_click()
        self.app_running = False
        print("Application Exiting...")

    def move_mouse(self, x, y):
        mouse.position = (x, y)

    def switch_btn(self, arg, Button=Button):
        switcher = {
            "L": Button.left,
            "R": Button.right,
        }
        return switcher.get(arg.upper(), Button.left)

    # When the thread starts, this method will be called
    def run(self):
        while self.app_running:
            print("Program Running...")
            if self.running:
                if self.app_counter < int(self.repetitions):
                    self.status_msg.config(text=f"> Running Repeat {self.app_counter+1}...")

                    counter = 0
                    while self.running and counter < len(self.profile):
                        for item in self.profile:
                            if exit_event.is_set():
                                break
                            print(f"Click Activity: {item['Activity']}")
                            self.move_mouse(item["X"], item["Y"])
                            
                            # if not self.running:
                            if exit_event.is_set():
                                break
                            self.button = self.switch_btn(item["Button"])
                            mouse.click(self.button)
                            print(f"Clicked at: {item['X']} and {item['Y']}")

                            if exit_event.is_set():
                                break
                            print(f'{item["delay(s)"]} secs delay for next activity\n')
                            delay_event.wait(item["delay(s)"])

                            counter += 1

                    print(f">> {self.time_between_repeats} secs delay for next repeat <<")
                    delay_event.wait(self.time_between_repeats)  # time between every repeat
                    self.app_counter += 1
                    print(f">> Next Repetition...<<")
