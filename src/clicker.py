import sys
# import load_data, autoclick, utils
# import utils
from pynput.keyboard import Listener, Key

# utils.init_figlet()
# log = utils.init_logging()

# profile = load_data.get_click_profile()
# log.debug(f"Click profile {profile}")

# click_thread = autoclick.AutoClicker(profile)
# log.debug(f"Click Thread Running...")
# click_thread.start()




# def on_press(key):
#     # start_stop_key will stop clicking if running flag is set to true
#     if key == Key.f4:
#         if click_thread.running:
#             log.info("Stop Clicking (F4)...")
#             click_thread.stop_click()
#         else:
#             log.info("Start Clicking (F4)...")
#             click_thread.start_click()

#     # here exit method is called and when
#     # key is pressed it terminates auto clicker
#     elif key == Key.esc:
#         click_thread.exit()
#         listener.stop()
#         sys.exit()

# with Listener(on_press=on_press) as listener:
#     listener.join()
