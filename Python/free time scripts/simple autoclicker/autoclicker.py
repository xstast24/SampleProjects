import variables
import threading
import time
from pynput_clicking import start_clicking
from pynput.mouse import Controller
from pynput.keyboard import Key, KeyCode, Listener


SWITCH_BUTTON = ';'  # activate/deactivate clicking
SHUTDOWN_BUTTON = Key.f6  # safely shutdown the whole autoclicker
# TODO not implemented yet
AUTO_STOP = False
OFFSET = 30


def on_press(key):
    if isinstance(key, KeyCode) and key == KeyCode.from_char(SWITCH_BUTTON):
        if variables.active_clicking:
            print("Autoclicker stopping")
            variables.active_clicking = False
            time.sleep(0.2)
            variables.clicking_thread.join()
            print("Autoclicker stopped\n")
        else:
            print("Autoclicker starting")
            variables.active_clicking = True
            variables.clicking_thread = threading.Thread(target=start_clicking, args=(variables.mouse,))
            variables.clicking_thread.start()
            print("Autoclicker started")
    if isinstance(key, Key) and key == SHUTDOWN_BUTTON:
        if variables.active_clicking:
            print("Autoclicker stopping")
            variables.active_clicking = False
            variables.clicking_thread.join()

        print("Autoclicker shutting down...")
        return False;


def start_keyboard_monitoring():
    # Collect events until released
    with Listener(on_press=on_press, on_release=None) as listener:
        listener.join()


variables.mouse = Controller()
variables.active_clicking = False
print("Autoclicker at your service!\n")

start_keyboard_monitoring()
exit(0)
