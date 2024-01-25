import time
import tkinter as tk

import cv2
import keyboard
import numpy as np
import pyautogui

from CoordinateSaver import CoordinatesSaver
from MatrixUtil import MatrixUtil

ant = cv2.imread(r'icons\Ant.png', cv2.IMREAD_GRAYSCALE)
dead = cv2.imread(r'icons\Dead.png', cv2.IMREAD_GRAYSCALE)
fire = cv2.imread(r'icons\Fire.png', cv2.IMREAD_GRAYSCALE)
light = cv2.imread(r'icons\Light.png', cv2.IMREAD_GRAYSCALE)
ogre = cv2.imread(r'icons\Ogre.png', cv2.IMREAD_GRAYSCALE)
shaman = cv2.imread(r'icons\Shaman.png', cv2.IMREAD_GRAYSCALE)
skull = cv2.imread(r'icons\Skull.png', cv2.IMREAD_GRAYSCALE)
smile = cv2.imread(r'icons\Smile.png', cv2.IMREAD_GRAYSCALE)

icon_bindings = [
    ('ant', ant),
    ('dead', dead),
    ('fire', fire),
    ('light', light),
    ('ogre', ogre),
    ('shaman', shaman),
    ('skull', skull),
    ('smile', smile)
]

icon_locations = []
found_pairs = []

window = tk.Tk()
window.title("Coordinate Selection")
window.attributes('-topmost', 1)

coordinates_saver = CoordinatesSaver()

top_left_button = tk.Button(window, text="Click Top Left", command=lambda: coordinates_saver.start_listener("TopLeft"))
bottom_right_button = tk.Button(window, text="Click Bottom Right",
                                command=lambda: coordinates_saver.start_listener("BottomRight"))


def take_screenshot(center_x, center_y, side_length):
    half_side_length = side_length / 2

    # Get bounds of the flipped card
    top_left_x = int(center_x - half_side_length)
    top_left_y = int(center_y - half_side_length)
    bottom_right_x = int(center_x + half_side_length)
    bottom_right_y = int(center_y + half_side_length)

    width = bottom_right_x - top_left_x
    height = bottom_right_y - top_left_y

    # Get the flipped card
    screenshot = pyautogui.screenshot(region=(top_left_x, top_left_y, width, height))
    return screenshot


def find_matching_icon(flipped_card_image, icon_bindings, x, y):
    # Convert the flipped card image to a NumPy array
    flipped_card_np = np.array(flipped_card_image)
    # Convert the flipped card image to grayscale
    flipped_card_gray = cv2.cvtColor(flipped_card_np, cv2.COLOR_BGR2GRAY)

    max_confidence = -1
    best_match_name = None

    # Iterate through the available icon bindings
    for icon_name, icon_path in icon_bindings:
        img = icon_path

        # Convert icon image to grayscale if it has 3 channels (BGR)
        if img.shape[-1] == 3:
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            img_gray = img

        # Normalize both flipped card and icon images
        flipped_card_gray_norm = cv2.normalize(flipped_card_gray, None, 0, 255, cv2.NORM_MINMAX)
        img_gray_norm = cv2.normalize(img_gray, None, 0, 255, cv2.NORM_MINMAX)

        # Apply template matching
        result = cv2.matchTemplate(flipped_card_gray_norm, img_gray_norm, cv2.TM_CCORR_NORMED)
        confidence = np.max(result)

        # Update the best match if the current confidence is higher
        if confidence > max_confidence:
            max_confidence = confidence
            best_match_name = icon_name

    if best_match_name is not None:
        coordinates = [x, y]
        # Update the icon locations with the best match
        update_icon_locations(icon_locations, best_match_name, coordinates)
        print(f"Best match: {best_match_name} with confidence {max_confidence}")
    else:
        print("No matches found.")


def update_icon_locations(icon_locations, best_match_name, coordinates):
    for icon_info in icon_locations:
        existing_name = icon_info[0]

        if existing_name == best_match_name:
            if coordinates not in found_pairs:
                # There were other coordinates under the given icon name already => these new coordinates are the second
                # pair location. Add them to the stack of found_pairs, which are to be clicked onto next.
                found_pairs.append(coordinates)
                found_pairs.append(icon_info[1])
                print("MATCH FOUND")
            break
    else:
        # If no match was found in existing icon locations, add the new icon location
        icon_locations.append([best_match_name, coordinates])


def start_game(event):
    icon_locations.clear()
    found_pairs.clear()
    click_count = 0

    print("TL", coordinates_saver.top_left_coord)
    print("BR", coordinates_saver.bottom_right_coord)

    top_left_coord = coordinates_saver.top_left_coord
    bottom_right_coord = coordinates_saver.bottom_right_coord

    memory_game = MatrixUtil(top_left_coord, bottom_right_coord)
    matrix = memory_game.create_matrix()

    for row in matrix:
        for x, y in row:
            if click_count == 0:
                # When clicking on the GUI of the program, we need one click to set the focus on BlueStacks
                pyautogui.click(x, y)

            pyautogui.click(x, y)
            click_count += 1
            time.sleep(0.8)
            print("Clicked at ", x, y)
            screenshot_after_flip = take_screenshot(x, y, 114)
            find_matching_icon(screenshot_after_flip, icon_bindings, x, y)

            if click_count % 2 == 0:
                while len(found_pairs) > 0:
                    time.sleep(1)
                    pyautogui.click(found_pairs[0])
                    time.sleep(1.5)
                    pyautogui.click(found_pairs[1])
                    time.sleep(2)
                    found_pairs.pop(0)
                    found_pairs.pop(0)

        if keyboard.is_pressed('m'):
            print("Terminating the loop.")
            exit()


start_button = tk.Button(window, text="Start")
start_button.bind("<Button-1>", start_game)

top_left_button.pack(pady=10)
bottom_right_button.pack(pady=10)
start_button.pack(pady=10)

window.mainloop()
