import threading
import copy
import pyautogui
import numpy

from ultralytics import YOLO
from pynput.mouse import Controller, Button as MouseButton
from pynput.keyboard import Controller as KeyboardController

from const.const import screen_width, screen_height, screenx_center, screeny_center, building_tree_scores, button_locations
from bot_actions import Bot
from screenshots import Screenshots

from object_clusters import ObjectClusters

mouse = Controller()
keyboard = KeyboardController()

bot_actions = Bot(mouse, keyboard, Screenshots, MouseButton, screenx_center, screeny_center)

def take_screenshot_new(stop_event: threading.Event, model):
    pyautogui.FAILSAFE = False
    
    while not stop_event.is_set():
        boxes, classes, names, conf = Screenshots.take_and_process_screenshot(model)

        buy_button_locations = []

        # tracks closest fuel location & distance if any
        fuel_location = None
        closest_fuel_distance = numpy.inf

        # track objects in distance for lightning & meteor usage
        num_objects_around_400_distance = 0
        num_objects_around_600_distance = 0

        # divide screen into 6 equal sized blocks, and track objects on the blocks
        object_clusters = ObjectClusters(screen_width, screen_height)
        obj_array = numpy.zeros((2,3)) # tracks object sums in blocks
        obj_array_closest_distances = numpy.full((2,3), numpy.inf) # tracks distance to closest object by blocks
        obj_array_closest_distances_x_y = numpy.full((2,3), numpy.inf, dtype=object) # tracks (x,y) of closest object on blocks

        # O(1) tracking for block with highest score sum
        max_col_num, max_row_num, max_object_cluster_sum = -1, -1, -1

        button_in_view = False
        button_locations_deepcopy = copy.deepcopy(button_locations)

        for box, cls in zip(boxes, classes):
            name = names[int(cls)]
            
            x1, y1, x2, y2 = box

            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2


            if name in button_locations_deepcopy:
                button_in_view = True
                button_locations_deepcopy[name] = (center_x, center_y)

            if name == "buy":
                buy_button_locations.append((center_x, center_y))

            distance = ((center_x - screenx_center) ** 2 + (center_y - screeny_center) **2) **.5

            if name == "fuel":
                if distance < closest_fuel_distance:
                    closest_fuel_distance = distance
                    fuel_location = (center_x, center_y)

            if name != "tree" and name != "building": continue

            # track trees and buildings inside specific distance ranges
            if distance <= 400:
                num_objects_around_400_distance += 1
            elif distance <= 600:
                num_objects_around_600_distance += 1

            obj_column, obj_row = object_clusters.object_position_in_grid(center_x, center_y)
            obj_array[obj_row][obj_column] += building_tree_scores[name]

            if distance < obj_array_closest_distances[obj_row][obj_column]:
                obj_array_closest_distances[obj_row][obj_column] = distance
                obj_array_closest_distances_x_y[obj_row][obj_column] = (center_x, center_y)

            if obj_array[obj_row][obj_column] == max_object_cluster_sum and distance < obj_array_closest_distances[obj_row, obj_column]:
                max_object_cluster_sum = obj_array[obj_row][obj_column]
                max_col_num = obj_column
                max_row_num = obj_row

            if obj_array[obj_row][obj_column] > max_object_cluster_sum:
                max_object_cluster_sum = obj_array[obj_row][obj_column]
                max_col_num = obj_column
                max_row_num = obj_row

        bot_actions.run_bot(
            obj_array_closest_distances_x_y, 
            max_col_num, 
            max_row_num, 
            button_in_view, 
            button_locations_deepcopy, 
            buy_button_locations, 
            fuel_location,
            closest_fuel_distance,
            num_objects_around_400_distance,
            num_objects_around_600_distance,
            model)

def main():
    model = YOLO("./data/model/best.pt")
    stop_event = threading.Event()

    screenshot_thread = threading.Thread(target=take_screenshot_new, args=(stop_event, model))
    screenshot_thread.start()

if __name__ == "__main__":
    main()