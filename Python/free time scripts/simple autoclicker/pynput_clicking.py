from pynput.mouse import Button
import time
import variables


def click(mouse):
    mouse.press(Button.left)
    mouse.release(Button.left)


def start_clicking(mouse):
    click_count = 0
    start_time = time.time()
    while variables.active_clicking:
        click(mouse)
        time.sleep(0.018)  # 0.13 = +-73 cps
        click_count += 1

    end_time = time.time()
    final_time = end_time - start_time
    print("Clicked {0} times".format(click_count))
    print("Average {0} clicks per second".format(click_count/final_time))
