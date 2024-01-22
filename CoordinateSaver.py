from pynput.mouse import Listener


class CoordinatesSaver:
    def __init__(self):
        self.position = None
        self.bottom_right_coord = None
        self.top_left_coord = None
        self.coord = []
        self.click_counter = 0
        self.listener = None

    def on_click(self, x, y, button, pressed):
        if pressed:
            x = int(x)
            y = int(y)
            self.coord.append((x, y))

            if len(self.coord) == 1:
                if self.position == "TopLeft":
                    self.top_left_coord = self.coord[0]
                    print("Top-left coordinates:", self.top_left_coord)
                elif self.position == "BottomRight":
                    self.bottom_right_coord = self.coord[0]
                    print("Bottom-right coordinates:", self.bottom_right_coord)

                self.coord.clear()
                self.stop_listener()

    def start_listener(self, position):
        self.position = position
        self.listener = Listener(on_click=self.on_click)
        self.listener.start()

    def stop_listener(self):
        if self.listener:
            self.listener.stop()
