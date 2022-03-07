import json


def select_pick_time(current_time):
    if current_time.minute < 30:
        pick_time = current_time.replace(minute=0)
    else:
        pick_time = current_time.replace(minute=30)

    return pick_time
