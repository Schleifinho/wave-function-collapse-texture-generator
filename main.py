import json
import toml
import sys
import numpy as np
import cv2 as cv2
from Wave import BorderTypes

from Wave import Wave

BORDER_MODE = BorderTypes.SEAMLESS #0 Nobe; 1 Seamless

def main():

    config = toml.load('config.toml')

    validate_config(config)

    north_south = np.array([ar for ar in config["NORTH_SOUTH"].values()])
    east_west = np.array([ar for ar in config["EAST_WEST"].values()])
    tile_size = config["DEFAULT"]["TILE_SIZE"]
    num_of_tiles = config["DEFAULT"]["NUMBER_OF_TILES"]
    field_width = config["DEFAULT"]["WIDTH"]
    field_height = config["DEFAULT"]["HEIGHT"]
    bg_color = config["DEFAULT"]["BG_COLOR"]
    image_path = config["DEFAULT"]["IMAGE_PATH"]
    border_mode = BorderTypes(config["DEFAULT"]["BORDER_MODE"])


    my_wave = Wave(num_of_tiles, north_south, east_west, field_width, field_height, border_mode)
    print(my_wave)

    canvas = np.full((field_height * tile_size, field_width * tile_size, 3), bg_color, np.uint8)

    folder = config['TILES']['FOLDER'] + "/"
    tiles_imgs = [cv2.imread(folder + tile) for tile in config['TILES']['TILE_IMGS']]

    # print(tiles_imgs)
    for candidate in my_wave.candidate_field.flat:
        if len(candidate) == 0:
            canvas[candidate.pos_x * tile_size:candidate.pos_x * tile_size + tile_size, candidate.pos_y * tile_size:candidate.pos_y * tile_size + tile_size] = tiles_imgs[candidate.candidates[0]]

    cv2.imwrite(image_path, canvas)


def validate_config(config):
    # Check if required keys are present
    required_keys = ['DEFAULT', 'NORTH_SOUTH', 'EAST_WEST', 'TILES']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing '{key}' section in the configuration.")

    # DEFAULT
    # Check specific settings within sections
    required_default_numbers = ['NUMBER_OF_TILES', 'WIDTH', 'HEIGHT', 'TILE_SIZE', 'BG_COLOR']
    for key in required_default_numbers:
        if key in config['DEFAULT']:
            elem = config['DEFAULT'][key]
            if not isinstance(elem, int) or elem <= 0:
                raise ValueError(f"Invalid {key} value in the 'DEFAULT' section.")
        else:
            raise ValueError(f"Missing {key} setting in the 'DEFAULT' section.")

    if "BORDER_MODE" in config['DEFAULT']:
        elem = config['DEFAULT']['BORDER_MODE']
        if not isinstance(elem, int) or not BorderTypes.has_value(elem):
            raise ValueError(f"Invalid 'BORDER_MODE' value in the 'DEFAULT' section. usually >= 0 and < {len(BorderTypes)}")
    else:
        raise ValueError(f"Missing {key} setting in the 'DEFAULT' section.")
    if 'IMAGE_PATH' in config['DEFAULT']:
        path = config['DEFAULT']['IMAGE_PATH']
        if not isinstance(path, str) or len(path) == 0 or not (path.endswith(".png") or path.endswith(".jpg")):
            raise ValueError("Invalid 'IMAGE_PATH' value in the 'DEFAULT' section (hint: .png or .jpg).")
    else:
        raise ValueError("Missing 'IMAGE_PATH' setting in the 'server' section.")

    # NEIGHBORS
    north_south = config["NORTH_SOUTH"]
    if len(north_south) != config["DEFAULT"]["NUMBER_OF_TILES"]:
        raise ValueError("NORTH_SOUTH section rows do not match 'NUMBER_OF_TILES'")

    for key, value in north_south.items():
        if len(value) != config["DEFAULT"]["NUMBER_OF_TILES"]:
            raise ValueError(f"{key} section colum do not match 'NUMBER_OF_TILES'")

    east_west = config["EAST_WEST"]
    if len(east_west) != config["DEFAULT"]["NUMBER_OF_TILES"]:
        raise ValueError("EAST_WEST section rows do not match 'NUMBER_OF_TILES'")

    for key, value in east_west.items():
        if len(value) != config["DEFAULT"]["NUMBER_OF_TILES"]:
            raise ValueError(f"{key} section colum do not match 'NUMBER_OF_TILES'")

    if 'FOLDER' in config['TILES']:
        folder = config['TILES']['FOLDER']
        if not isinstance(folder, str) or len(folder) == 0:
            raise ValueError("Invalid 'FOLDER' value in the 'TILES' section")
    else:
        raise ValueError("Missing 'FOLDER' setting in the 'server' section.")

    if 'TILE_IMGS' in config['TILES']:
        imgs = config['TILES']['TILE_IMGS']
        if not isinstance(imgs, list) or len(imgs) != config["DEFAULT"]["NUMBER_OF_TILES"]:
            raise ValueError("Invalid 'TILE_IMGS' error. Maybe colum do not match 'NUMBER_OF_TILES'")
    else:
        raise ValueError("Missing 'FOLDER' setting in the 'server' section.")


if __name__ == "__main__":
    main()