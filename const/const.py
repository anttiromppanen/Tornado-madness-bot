# tracks objects seen in the last frame
decision_dict = {
    "buy": False,
    "play": False,
    "continue": False,
    "next": False,
    "tornado": False,
    "tree": False,
    "fuel": False,
    "building": False,
    "no_thanks": False,
    "poor": False,
}

# tracks location of objects seen in the last frame
decision_location_dict = {
    "buy": None,
    "play": None,
    "continue": None,
    "next": None,
    "tornado": None,
    "tree": None,
    "fuel": None,
    "building": None,
    "no_thanks": None,
    "poor": None,
}

# tracks object distances seen in the last frame
decision_distance_dict = {
    "tree": float("inf"),
    "fuel": float("inf"),
    "building": float("inf"),
}

screenx_center = 1920 / 2
screeny_center = 1080 / 2