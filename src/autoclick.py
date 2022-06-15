# threading needed to control the clicks
# so we inherit the class
import sys
import threading
import time
from pynput.mouse import Button, Controller

mouse = Controller()


class AutoClicker(threading.Thread):

    profile = []
    transactions = None
    repetitions = None
    button = None
    running = False
    app_running = True
    app_counter = 0
    time_between_repeats = 0
    status_msg = ""

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

    def exit(self):
        self.stop_click()
        self.app_running = False

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
            if self.app_counter < int(self.repetitions):
                if self.running:
                    print(f"Running Repeat {self.app_counter+1}...")
                    status_msg = (
                        f"Running Repeat {self.app_counter+1}..."
                        if self.running
                        else ""
                    )

                    counter = 0
                    while self.running and counter < len(self.profile):
                        for item in self.profile:
                            print(f"Click Activity : {item['Activity']}")
                            self.move_mouse(item["X"], item["Y"])

                            self.button = self.switch_btn(item["Button"])
                            mouse.click(self.button)

                            print(
                                f'Delaying for {item["delay(s)"]} seconds for next activity\n'
                            )
                            time.sleep(item["delay(s)"])

                            counter += 1

                    print(
                        f">> Delaying for {self.time_between_repeats} seconds for next repeat <<\n"
                    )
                    time.sleep(self.time_between_repeats)  # time between every repeat
                    self.app_counter += 1
