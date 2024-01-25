class MatrixUtil:
    def __init__(self, top_left, bottom_right, gap=24):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.gap = gap

    def create_matrix(self):
        matrix = []
        start_x = self.top_left[0]
        start_y = self.top_left[1]

        square_side_size = 114

        # Create the matrix with coordinates of all 16 (4x4) squares.
        for row in range(4):
            row_values = []
            for col in range(4):
                x = start_x + col * (square_side_size + self.gap) + square_side_size / 2
                y = start_y + row * (square_side_size + self.gap) + square_side_size / 2
                row_values.append((x, y))
            matrix.append(row_values)

        return matrix
