import threading
import copy
import pyautogui
import time

from ultralytics import YOLO
from pynput.mouse import Controller, Button as MouseButton
from pynput.keyboard import Controller as KeyboardController

from const.const import decision_dict, decision_location_dict, decision_distance_dict, screenx_center, screeny_center
from bot_actions import Bot
from screenshots import Screenshots

mouse = Controller()
keyboard = KeyboardController()

bot_actions = Bot(mouse, keyboard, MouseButton, screenx_center, screeny_center)

def run_bot(decision_dict, decision_location_dict, decision_distance_dict, buy_button_locations, num_of_objects_under_400_distance, num_of_objects_under_600_distance, model):
    if num_of_objects_under_400_distance > 4:
        bot_actions.press_lightning()
    if num_of_objects_under_600_distance > 10:
        bot_actions.press_meteorites()

    # click buy buttons
    if decision_dict["buy"] or decision_dict["poor"]:
        for location in buy_button_locations:
            mouse.position = location
            mouse.click(MouseButton.left, 1)
            time.sleep(1)
        
        # scroll down to see if there are more buy buttons
        # take screenshot and run model again
        for _ in range(2):
            mouse.position = (200, 200)
            time.sleep(0.5)
            mouse.scroll(20, 0)
            time.sleep(1)

            boxes, classes, names, confidences = Screenshots.take_and_process_screenshot(model)
            buy_button_locations = []

            for box, cls, conf in zip(boxes, classes, confidences):
                x1, y1, x2, y2 = box

                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2

                name = names[int(cls)]

                if name == "buy":
                    buy_button_locations.append((center_x, center_y))

            for location in buy_button_locations:
                mouse.position = location
                mouse.click(MouseButton.left, 1)
                time.sleep(1)
        

    if decision_dict["next"]:
        bot_actions.click_next_button(decision_location_dict)
        return

    # click play button
    if decision_dict["play"]:
        bot_actions.click_play_button(decision_location_dict)
        return

    if decision_dict["continue"]:
        mouse.position = decision_location_dict["continue"]
        mouse.click(MouseButton.left, 1)
        return
    
    if decision_dict["no_thanks"]:
        mouse.position = decision_location_dict["no_thanks"]
        mouse.click(MouseButton.left, 1)
        return

    # go to fuel if it is close
    if decision_dict["fuel"] and decision_distance_dict["fuel"] < 600:
        mouse.position = decision_location_dict["fuel"]
        return

    if not decision_dict["tree"] and not decision_dict["building"]:
        return

    tree_distance = decision_distance_dict["tree"]
    building_distance = decision_distance_dict["building"] - 150

    # go to tree or building or center if not close to any
    if decision_dict["fuel"] and decision_distance_dict["fuel"] < 600:
        mouse.position = decision_location_dict["fuel"]
    elif tree_distance < building_distance:
        bot_actions.move_to_tree_or_building(decision_location_dict, "tree")
    else:
        bot_actions.move_to_tree_or_building(decision_location_dict, "building")

def take_screenshot(stop_event: threading.Event, model):
    pyautogui.FAILSAFE = False
    
    while not stop_event.is_set():
        decision_dict_deepcopy = copy.deepcopy(decision_dict)
        decision_location_dict_deepcopy = copy.deepcopy(decision_location_dict)
        decision_distance_dict_deepcopy = copy.deepcopy(decision_distance_dict)

        buy_button_locations = []
        num_of_objects_under_400_distance = 0
        num_of_objects_under_600_distance = 0

        boxes, classes, names, confidences = Screenshots.take_and_process_screenshot(model)

        #process result list
        for box, cls, conf in zip(boxes, classes, confidences):
            x1, y1, x2, y2 = box

            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2

            name = names[int(cls)]

            decision_dict_deepcopy[name] = True

            if name == "tree" or name == "building" or name == "fuel":
                distance = ((center_x - screenx_center) ** 2 + (center_y - screeny_center) **2) **.5

                if distance <= 400:
                    num_of_objects_under_400_distance += 1
                if distance <= 600:
                    num_of_objects_under_600_distance += 1

                decision_distance_dict_deepcopy[name] = min(decision_distance_dict_deepcopy[name], distance)

                if distance == decision_distance_dict_deepcopy[name]:
                    decision_location_dict_deepcopy[name] = (center_x, center_y)
            elif name == "buy":
                buy_button_locations.append((center_x, center_y))
            else:
                decision_location_dict_deepcopy[name] = (center_x, center_y)

        run_bot(decision_dict_deepcopy, decision_location_dict_deepcopy, decision_distance_dict_deepcopy, buy_button_locations, num_of_objects_under_400_distance, num_of_objects_under_600_distance, model)



def main():
    model = YOLO("./data/model/best.pt")
    stop_event = threading.Event()

    screenshot_thread = threading.Thread(target=take_screenshot, args=(stop_event, model))
    screenshot_thread.start()

if __name__ == "__main__":
    main()