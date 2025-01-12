import pyautogui

screen_width, screen_height = pyautogui.size()

object_class_names = {
    "buy": True,
    "play": True,
    "continue": True,
    "next": True,
    "tornado": True,
    "tree": True,
    "fuel": True,
    "building": True,
    "no_thanks": True,
    "poor": True,
}

button_locations = {
    "buy": None,
    "play": None,
    "continue": None,
    "next": None,
    "no_thanks": None,
    "poor": None,
}

# tracks object distances seen in the last frame
decision_distance_dict = {
    "tree": float("inf"),
    "fuel": float("inf"),
    "building": float("inf"),
}

screenx_center = screen_width / 2
screeny_center = screen_height / 2

building_tree_scores = {
    "building": 2.5,
    "tree": 1,
}