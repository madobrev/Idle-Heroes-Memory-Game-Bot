import os
import time
import tkinter as tk

import keyboard
import pyautogui

from CoordinateSaver import CoordinatesSaver
from MatrixUtil import MatrixUtil

ant = os.path.abspath(r'icons\Ant.PNG')
dead = os.path.abspath(r'icons\Dead.PNG')
fire = os.path.abspath(r'icons\Fire.PNG')
light = os.path.abspath(r'icons\Light.PNG')
ogre = os.path.abspath(r'icons\Ogre.PNG')
shaman = os.path.abspath(r'icons\Shaman.PNG')
skull = os.path.abspath(r'icons\Skull.PNG')
smile = os.path.abspath(r'icons\Smile.PNG')

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


icon_occurrences = {}
coordinates_to_click = []


def search_for_icon():
    for name, path in icon_bindings:
        try:
            locations = list(pyautogui.locateAllOnScreen(path, confidence=0.9))
            for item in locations:
                if all(not are_coordinates_close(item, loc) for loc in found_locations[name]):
                    print(name, "found at", item)
                    coordinate = [item[0], item[1]]
                    if icon_occurrences.get(name) is not None:
                        coordinate_tuple = [icon_occurrences[name], coordinate]
                        coordinates_to_click.append(coordinate_tuple)
                        to_be_removed = (name, path)
                        icon_bindings.remove(to_be_removed)
                        return
                    icon_occurrences[name] = coordinate
                    found_locations[name].add(item)
                    return
        #   time.sleep(0.5)
        except Exception as e:
            print(f"Error during icon search for {name}: {e}")
            continue


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
        for _ in range(2):
            for row in matrix:
                for x, y in row:
                    if click_count == 0:
                        pyautogui.click(x, y)

                    pyautogui.click(x, y)
                    time.sleep(2)
                    print("Clicked at ", x, y)
                    click_count += 1
                    search_for_icon()

                    if click_count % 2 == 0:
                        if len(coordinates_to_click) > 0:
                            pyautogui.click(coordinates_to_click[0][0], coordinates_to_click[0][1])
                            pairs_found += 1

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
