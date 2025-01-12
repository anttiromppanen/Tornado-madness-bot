import time

from typing import Literal

TreeOrBuilding = Literal["tree", "building"]

class Bot:
    def __init__(self, MouseController, KeyboardController, MouseButton, screenx_center, screeny_center):
        self.MouseController = MouseController
        self.KeyboardController = KeyboardController
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

    def click_buy_button(self, location, buy_button_locations):
        for location in buy_button_locations:
            self.MouseController.position = location
            self.MouseController.click(self.MouseButton.left, 1)
            time.sleep(0.5)
    
    def click_play_button(self, decision_location_dict):
        time.sleep(1)
        self.MouseController.position = decision_location_dict["play"]
        self.MouseController.click(self.MouseButton.left, 1)

    def click_next_button(self, decision_location_dict):
        time.sleep(1)
        self.MouseController.position = decision_location_dict["next"]
        self.MouseController.click(self.MouseButton.left, 1)

    def click_continue_button(self, decision_location_dict):
        time.sleep(1)
        self.MouseController.position = decision_location_dict["continue"]
        self.MouseController.click(self.MouseButton.left, 1)

    def move_to_fuel(self, decision_location_dict):
        self.MouseController.position = decision_location_dict["fuel"]

    def move_to_tree_or_building(self, decision_location_dict, tree_or_building: TreeOrBuilding):
        if tree_or_building not in {"tree", "building"}:
            raise ValueError("tree_or_building must be 'tree' or 'building'")
        self.MouseController.position = decision_location_dict[tree_or_building] or (self.screenx_center, self.screeny_center)
