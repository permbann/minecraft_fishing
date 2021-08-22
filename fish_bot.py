import pyautogui
import time
import win32api
from pynput.keyboard import Key, KeyCode, Events
import pydirectinput
import threading
from playsound import playsound


class BotJob(threading.Thread):

    def __init__(self, screen_width, screen_height):
        threading.Thread.__init__(self)

        # The shutdown_flag is a threading.Event object that
        # indicates whether the thread should be terminated.
        self.shutdown_flag = threading.Event()
        self.screen_width = screen_width
        self.screen_height = screen_height

    def run(self):
        print('Thread #%s started' % self.ident)
        if not self.check_screen_region():
            pydirectinput.click(button='right')
            time.sleep(2)
        while not self.shutdown_flag.is_set():
            result = self.check_screen_region()
            if not result:
                pydirectinput.click(button='right')
                time.sleep(0.5)
                pydirectinput.click(button='right')
                time.sleep(2)
            time.sleep(0.01)

        # ... Clean shutdown code here ...
        print('Thread #%s stopped' % self.ident)

    def check_screen_region(self):
        return pyautogui.locateOnScreen('tempsnip.png',
                                        region=(int(self.screen_width / 3), int(self.screen_width / 5),
                                                int(2 * self.screen_width / 3), int(4 * self.screen_width / 5)),
                                        grayscale=True, confidence=0.85)


if __name__ == '__main__':
    screen_width = win32api.GetSystemMetrics(0)
    screen_height = win32api.GetSystemMetrics(1)
    bot_job = BotJob(screen_width, screen_height)
    while True:
        with Events() as events:
            for event in events:
                if type(event) == Events.Release:
                    if event.key == KeyCode(char="v"):
                        if not bot_job.is_alive():
                            # starting
                            playsound('starting.wav')
                            bot_job.start()
                        else:
                            # pausing
                            playsound('pausing.wav')
                            bot_job.shutdown_flag.set()
                            bot_job.join()
                            bot_job = BotJob(screen_width, screen_height)

                    if event.key == Key.f4:
                        bot_job.shutdown_flag.set()
                        playsound('stopping.wav')
                        exit(0)
