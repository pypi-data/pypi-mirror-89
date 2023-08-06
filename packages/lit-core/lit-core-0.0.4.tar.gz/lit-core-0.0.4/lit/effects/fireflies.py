import random
import logging

logger = logging.getLogger(__name__)
name = "Fireflies"

start_message = name + " started!"

description = "You would not believe your eyes"


def setup_start_duration_colors(lights, args):
    return [(-1, 1, (0, 0, 0))] * lights.size


schema = {
    "color": {
        "value": {"type": "color", "default": (255, 240, 0)},
        "user_input": True,
        "required": False,
    },
    "density": {
        "value": {"type": "number", "min": 1, "max": 100, "default": 50},
        "user_input": True,
        "required": False,
    },
    "start_duration_colors": {
        "value": {
            "type": "(int, int, (int, int, int)) list",
            "default_gen": setup_start_duration_colors,
        },
        "user_input": False,
    },
}

# Average time a led is on
AVG_ON_TIME = 100
MIN_ON_TIME = 10


def update(lights, step, state):
    color_gen = state["color"]
    start_duration_colors = state["start_duration_colors"]
    """ MATH:
    DENSITY = OnTime/(Ontime+OffTime)
    OnTime(1-DENSITY) = Density*OffTime
    Offtime = ((1-Density)*OnTime)/Density 
    """
    density = state["density"] / 100
    avg_off_time = ((1 - density) * AVG_ON_TIME) / density
    for i in range(lights.size):
        sdc = start_duration_colors[i]
        if sdc[0] + sdc[1] <= step:
            state["start_duration_colors"][i] = (
                step + random.random() * int(2 * avg_off_time),
                MIN_ON_TIME + (random.random() * (AVG_ON_TIME - MIN_ON_TIME) * 2),
                color_gen.get_color(step, i),
            )
        brightness = (step - sdc[0]) / (sdc[1] / 2)
        if brightness > 1:
            brightness = 2 - brightness
        brightness = max(brightness, 0)
        lights.set_pixel(
            i,
            int(sdc[2][0] * brightness),
            int(sdc[2][1] * brightness),
            int(sdc[2][2] * brightness),
            brightness,
        )
