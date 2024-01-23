import os
import time
import tkinter as tk
import keyboard
import pyautogui
import cv2
import numpy as np


from CoordinateSaver import CoordinatesSaver
from MatrixUtil import MatrixUtil

icon_dir = os.path.abspath('icons')

ant = cv2.imread(os.path.join(icon_dir, 'Ant.png'), cv2.IMREAD_GRAYSCALE)
dead = cv2.imread(os.path.join(icon_dir, 'Dead.png'), cv2.IMREAD_GRAYSCALE)
fire = cv2.imread(os.path.join(icon_dir, 'Fire.png'), cv2.IMREAD_GRAYSCALE)
light = cv2.imread(os.path.join(icon_dir, 'Light.png'), cv2.IMREAD_GRAYSCALE)
ogre = cv2.imread(os.path.join(icon_dir, 'Ogre.png'), cv2.IMREAD_GRAYSCALE)
shaman = cv2.imread(os.path.join(icon_dir, 'Shaman.png'), cv2.IMREAD_GRAYSCALE)
skull = cv2.imread(os.path.join(icon_dir, 'Skull.png'), cv2.IMREAD_GRAYSCALE)
smile = cv2.imread(os.path.join(icon_dir, 'Smile.png'), cv2.IMREAD_GRAYSCALE)

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

window = tk.Tk()
window.title("Coordinate Selection")
window.attributes('-topmost', 1)

coordinates_saver = CoordinatesSaver()

top_left_button = tk.Button(window, text="Click Top Left", command=lambda: coordinates_saver.start_listener("TopLeft"))
bottom_right_button = tk.Button(window, text="Click Bottom Right",
                                command=lambda: coordinates_saver.start_listener("BottomRight"))

found_locations = {name: set() for name, _ in icon_bindings}


def are_coordinates_close(coord1, coord2, threshold=10):
    return abs(coord1[0] - coord2[0]) <= threshold and abs(coord1[1] - coord2[1]) <= threshold


def take_screenshot(center_x, center_y, side_length):
    half_side_length = side_length / 2

    top_left_x = int(center_x - half_side_length)
    top_left_y = int(center_y - half_side_length)
    bottom_right_x = int(center_x + half_side_length)
    bottom_right_y = int(center_y + half_side_length)

    width = bottom_right_x - top_left_x
    height = bottom_right_y - top_left_y

    screenshot = pyautogui.screenshot(region=(top_left_x, top_left_y, width, height))
    return screenshot




def find_matching_icon(flipped_card_image, icon_bindings):
    flipped_card_np = np.array(flipped_card_image)
    flipped_card_gray = cv2.cvtColor(flipped_card_np, cv2.COLOR_BGR2GRAY)

    max_confidence = -1
    best_match_name = None

    for icon_name, icon_path in icon_bindings:
        img = icon_path
        confidence = cv2.matchTemplate(flipped_card_gray, img, cv2.TM_CCOEFF_NORMED).max()

        if confidence > max_confidence:
            max_confidence = confidence
            best_match_name = icon_name

    if best_match_name is not None:
        print(f"Best match: {best_match_name} with confidence {max_confidence}")
    else:
        print("No matches found.")

id_count = 0

def start_game(event):
    pairs_found = 0
    TOTAL_PAIRS = 8
    click_count = 0

    print("TL", coordinates_saver.top_left_coord)
    print("BR", coordinates_saver.bottom_right_coord)

    top_left_coord = coordinates_saver.top_left_coord
    bottom_right_coord = coordinates_saver.bottom_right_coord

    memory_game = MatrixUtil(top_left_coord, bottom_right_coord)
    matrix = memory_game.create_matrix()

    while pairs_found < TOTAL_PAIRS:
        for row in matrix:
            for x, y in row:
                if click_count == 0:
                    pyautogui.click(x, y)
                pyautogui.click(x, y)
                time.sleep(0.8)
                print("Clicked at ", x, y)
                screenshot_after_flip = take_screenshot(x, y, 114)
                find_matching_icon(screenshot_after_flip,icon_bindings)

                global id_count
                screenshot_after_flip.save(f'difference_{id_count}.png')
                id_count += 1


            click_count += 1

            if keyboard.is_pressed('m'):
                print("Terminating the loop.")
                exit()

    print("Locations: ", found_locations)


start_button = tk.Button(window, text="Start")
start_button.bind("<Button-1>", start_game)

top_left_button.pack(pady=10)
bottom_right_button.pack(pady=10)
start_button.pack(pady=10)

window.mainloop()
