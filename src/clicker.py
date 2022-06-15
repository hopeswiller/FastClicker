import sys,os, threading,time
# import load_data, autoclick, utils
# import utils
# from pynput.keyboard import Listener, Key

# print(os.environ['PROGRAMFILES'])
# for k,v in os.environ.items():
#     print(k, '-',v)
# print(os.path.expanduser('~'))
# print(os.sep.join([os.path.expanduser('~'), 'Application Data', 'MyApp']))
# v = os.path.join(os.environ, encodekey, decodekey, encodevalue, decodevalue) 'Program Files (x86)')

# print(v)
# import time

# class Test(threading.Thread):

#     stop = threading.Event() 
#     def run(self):
#         for i in range(1,11):
#             print(f'{i} of 20 thread is running')
#             time.sleep(0.3)

#             if self.stop.is_set():
#                 print("stopping thread..")
#                 break

#         print('finished..')

# test = Test()
# test.start()
# time.sleep(3)
# test.stop.set()
# test.join()
# time.sleep(2)
# # new 
# test1 = Test()
# # test1.stop.isSet = False
# print(test1.stop.is_set())
# test1.start()




# def sleep(seconds):
#     for i in range(seconds):
#         print(i)
#         if i == 3:
#             raise KeyboardInterrupt("asd")
#             print("Oh! You have sent a Keyboard Interrupt to me.\nBye, Bye")
#         try:
#             time.sleep(1)
#         except KeyboardInterrupt:
#             print("Oh! You have sent a Keyboard Interrupt to me.\nBye, Bye")
#             break


# sleep(60)
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
