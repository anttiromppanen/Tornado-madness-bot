import time
import numpy

from typing import Literal
from helpers import is_rgb_color_water

TreeOrBuilding = Literal["tree", "building"]

class Bot:
    def __init__(self, MouseController, KeyboardController, Screenshots, MouseButton, screenx_center, screeny_center):
        self.MouseController = MouseController
        self.KeyboardController = KeyboardController
        self.Screenshots = Screenshots
        self.MouseButton = MouseButton
        self.screenx_center = screenx_center
        self.screeny_center = screeny_center
    
    def press_lightning(self):
        self.KeyboardController.press("1")
        time.sleep(0.1)
        self.KeyboardController.release("1")

    def press_meteorites(self):
        time.sleep(0.5)
        self.KeyboardController.press("2")
        time.sleep(0.1)
        self.KeyboardController.release("2")

    def click_buy_button(self, buy_button_locations):
        for location in buy_button_locations:
            self.MouseController.position = location
            self.MouseController.click(self.MouseButton.left, 1)
            time.sleep(0.5)

    # handles all menu buttons except buy button
    def click_menu_button(self, button_type, button_locations_deepcopy):
        if button_type not in button_locations_deepcopy:
            raise ValueError(f"Error in click_menu_button: {button_type} not in {button_locations_deepcopy}")
        time.sleep(0.5)
        self.MouseController.position = button_locations_deepcopy[button_type]
        self.MouseController.click(self.MouseButton.left, 1)

    def handle_buy_menu(self, buy_button_locations, model):
        # click buy buttons in view
        self.click_buy_button(buy_button_locations)

        # scroll down to see if there are more buy buttons
        # take screenshot and run model again
        for _ in range(2):
            self.MouseController.position = (200, 200)
            time.sleep(0.5)
            self.MouseController.scroll(20, 0)
            time.sleep(0.5)

            boxes, classes, names, confidences = self.Screenshots.take_and_process_screenshot(model)
            buy_button_locations = []

            for box, cls, conf in zip(boxes, classes, confidences):
                x1, y1, x2, y2 = box

                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2

                name = names[int(cls)]

                if name == "buy":
                    buy_button_locations.append((center_x, center_y))

                self.click_buy_button(buy_button_locations)
    
    def run_bot(self, 
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
                max_object_cluster_sum,
                pixel_color_top_left_corner,
                model):
        if button_in_view:
            if button_locations_deepcopy["buy"] != None or button_locations_deepcopy["poor"] != None:
                self.handle_buy_menu(buy_button_locations, model)

            if button_locations_deepcopy["continue"] != None:
                self.click_menu_button("continue", button_locations_deepcopy)
            elif button_locations_deepcopy["next"] != None:
                self.click_menu_button("next", button_locations_deepcopy)
            elif button_locations_deepcopy["play"] != None:
                self.click_menu_button("play", button_locations_deepcopy)
        else: 
            if fuel_location != None and closest_fuel_distance <= 1000:
                self.MouseController.position = fuel_location
            elif max_object_cluster_sum < 7:
                # starts moving upwards if running into water
                if is_rgb_color_water(pixel_color_top_left_corner):
                    top_right_x = self.screenx_center + 200
                    top_right_y = self.screeny_center - 100
                    self.MouseController.position = (top_right_x, top_right_y)
                else:
                # top left corner
                    self.MouseController.position = (10, 10)
            elif obj_array_closest_distances_x_y[max_row_num][max_col_num] != numpy.inf:
                self.MouseController.position = obj_array_closest_distances_x_y[max_row_num][max_col_num]
            else:
                self.MouseController.position = (10, 10)

            if num_objects_around_600_distance >= 10:
                self.press_meteorites()
            if num_objects_around_400_distance >= 6:
                self.press_lightning()