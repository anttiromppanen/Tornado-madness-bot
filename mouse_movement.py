import pyautogui
import time
import os

from pynput.mouse import Controller as PynputMouseController
from evdev import UInput, ecodes

class MouseMovement:
    def __init__(self):
        self.PynputMouseController = PynputMouseController()
        self.positions = [(500, 500), (600, 500), (600, 600), (500, 600)]

    def test_pynput(self):
        print("Starting pynput mouse test...")
        for pos in self.positions:
            self.PynputMouseController.position = pos
            print(f"Moved to: {self.PynputMouseController.position}")
            time.sleep(0.5)
        print("Completed pynput test.")

    def test_pyautogui(self):
        print("Starting pyautogui mouse test...")
        for pos in self.positions:
            pyautogui.moveTo(pos[0], pos[1], duration=0.3)
            print(f"Moved to: {pyautogui.position()}")
            time.sleep(0.5)
        print("Completed pyautogui test.")

    def test_xdotool(self):
        print("Starting xdotool mouse test...")
        for pos in self.positions:
            os.system(f"xdotool mousemove {pos[0]} {pos[1]}")
            print(f"Moved to: {pos}")
            time.sleep(0.5)
        print("Completed xdotool test.")

    def test_evdev(self):
        try:
            with UInput() as ui:
                print("Starting evdev mouse test...")
                for dx, dy in self.positions:
                    ui.write(ecodes.EV_REL, ecodes.REL_X, dx)
                    ui.write(ecodes.EV_REL, ecodes.REL_Y, dy)
                    ui.syn()
                    print(f"Moved by: ({dx}, {dy})")
                    time.sleep(0.5)
                print("Completed evdev test.")
        except PermissionError:
            print("Permission denied. Try running this script as root.")