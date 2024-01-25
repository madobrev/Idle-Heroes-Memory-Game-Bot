import Constants


class MatrixUtil:
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def create_matrix(self):
        matrix = []
        start_x = self.top_left[0]
        start_y = self.top_left[1]

        # Create the matrix with coordinates of all 16 (4x4) squares.
        for row in range(4):
            row_values = []
            for col in range(4):
                x = start_x + col * (Constants.CARD_SIZE + Constants.GAP_BETWEEN_CARDS) + Constants.CARD_SIZE / 2
                y = start_y + row * (Constants.CARD_SIZE + Constants.GAP_BETWEEN_CARDS) + Constants.CARD_SIZE / 2
                row_values.append((x, y))
            matrix.append(row_values)

        return matrix
