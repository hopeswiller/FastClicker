# threading needed to control the clicks
# so we inherit the class
import sys
import logging
import threading
import time
from pynput.mouse import Button, Controller

log = logging.getLogger(__name__)

mouse = Controller()


class AutoClicker(threading.Thread):

    profile = []
    transactions = None
    repetitions = None
    button = None
    running = True
    app_running = True

    def __init__(self, profile, repetitions=5):
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
        app_counter = 0
        # while self.app_running and app_counter < self.repetitions:
        while self.app_running:

            counter = 0
            while self.running and counter < len(self.profile):
                for item in self.profile:
                    if self.running:  # click stop or not
                        log.debug(f"Click Activity : {item['Activity']}")
                        self.move_mouse(item["X"], item["Y"])

                        self.button = self.switch_btn(item["Button"])
                        mouse.click(self.button)

                        log.debug(
                            f'Delaying for {item["delay(s)"]} seconds for next activity\n'
                        )
                        time.sleep(item["delay(s)"])

                        counter += 1
            # log.debug(f"counter: {counter}")

            time.sleep(20) # time between every cycle
            # app_counter += 1
        # log.debug(f"app_counter: {app_counter}")
        log.debug(f"App Exit")
        self.exit()
