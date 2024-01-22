class MatrixUtil:
    def __init__(self, top_left, bottom_right, gap=25):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.gap = gap

    def create_matrix(self):
        matrix = []
        start_x, start_y = self.top_left
        end_x, end_y = self.bottom_right

        row_height = (end_y - start_y - self.gap) // 4
        col_width = (end_x - start_x - self.gap) // 4

        for row in range(4):
            row_values = []
            for col in range(4):
                x = start_x + col * col_width + col_width // 2
                y = start_y + row * row_height + row_height // 2
                row_values.append((x, y))
            matrix.append(row_values)

        return matrix


