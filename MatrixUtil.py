class MatrixUtil:
    def __init__(self, top_left, bottom_right, gap=24):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.gap = gap

    def create_matrix(self):
        matrix = []
        start_x = self.top_left[0]
        start_y = self.top_left[1]

        row_height = 114
        col_width = 114

        for row in range(4):
            row_values = []
            for col in range(4):
                # Calculate the center of each square
                x = start_x + col * (col_width + self.gap) + col_width / 2
                y = start_y + row * (row_height + self.gap) + row_height / 2
                row_values.append((x, y))
            matrix.append(row_values)

        return matrix
