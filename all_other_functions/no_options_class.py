class NoOptions:
    def __init__(self, amount, margin_H, margin_W, square_H, square_W, spacing_W, spacing_H,
                 busbar_width, min_finger_width, matrix, matrix_rows):
        self.amount = amount
        self.margin_H = margin_H
        self.margin_W = margin_W
        self.square_W = square_W
        self.square_H = square_H
        self.spacing_W = spacing_W
        self.spacing_H = spacing_H
        self.busbar_width = busbar_width
        self.min_finger_width = min_finger_width
        self.matrix = matrix
        self.matrix_rows = matrix_rows
        self.i = 0
        self.prev = False
        self.list_of_previous = None
        self.iterations = 0
        self.no_options = 0
        self.solution = None
        self.pop_up_closed = False
