from tkinter import *
from random import randint


def generate_spacing_lists(bsx, bsy, board_width: int, board_height: int):
    space_x = B_W // 7
    space_y = B_H // 6

    columns_x = column_spacing(bsx, 8, space_x)
    columns_y = column_spacing(bsy, 7, space_y)

    return columns_x, columns_y


def column_spacing(start: int, bounds: int, spacing):
    column_spacing = []

    for i in range(bounds):
        column_spacing.append(start)
        start += space_y
    return column_spacing


class PositionalMatrix:
    def __init__(self, canvas_width, canvas_height, board_width: int, board_height: int, rows: int, columns: int,
                 coin_padding: int = 3):
        self.coin_pad = coin_padding
        self.c_width = canvas_width
        self.c_height = canvas_height
        self.b_width = board_width
        self.b_height = board_height
        self.b_coords = self.calculate_board_coords()

        self.rows = rows
        self.cols = columns

        self.increments = self.generate_increments()
        self.spacings = self.generate_position_list()
        self.matrix = self.generate_position_matrix()

    def calculate_board_coords(self):
        pad_x, pad_y = (
            (self.c_width - self.b_width) // 2,
            (self.c_height - self.b_height) // 2
        )
        return (
            pad_x, pad_y,
            pad_x + self.b_width,
            pad_y + self.b_height
        )

    def generate_increments(self):
        return self.b_width // self.cols, self.b_height // self.rows

    def generate_position_list(self):
        return (
            [x for x in range(self.b_coords[0], self.b_width + 1, self.increments[0])],
            [y for y in range(self.b_coords[1], self.b_height + 1, self.increments[1])]
        )

    def generate_position_matrix(self):
        return [[(x + self.coin_pad, y + self.coin_pad, x + self.increments[0] - self.coin_pad, y + self.increments[1] -
                  self.coin_pad) for x in self.spacings[0]] for y in
                self.spacings[1]]

    def generate_x_windows(self):
        last_x = self.spacings[0][-1]
        x_windows = self.spacings[0].copy()
        x_windows.append(last_x + self.increments[0])
        return x_windows

    def generate_y_windows(self):
        last_y = self.spacings[1][-1]
        y_windows = self.spacings[0].copy()
        y_windows.append(last_y + self.increments[1])
        return y_windows

    def print(self):
        for row in self.matrix:
            print(row)


class StateMatrix:
    def __init__(self, rows, columns):
        self.rows = rows
        self.cols = columns
        self.matrix = None

        self.initialize_empty_board()

    def initialize_empty_board(self):
        self.matrix = [[0 for j in range(self.cols)] for i in range(self.rows)]

    def check_cell_state(self, row, col, player):
        if row < 0 or col < 0:
            return False
        try:
            if self.matrix[row][col] == player:
                return True
            else:
                return False
        except IndexError:
            return False

    def diagonal_win(self, row, col, player):

        up_r_step = (-1, 1)
        down_r_step = (1, 1)
        down_l_step = (1, -1)
        up_l_step = (-1, -1)

        steps = [up_r_step, down_r_step, down_l_step, up_l_step]

        up_r_pos = [row, col]
        down_r_pos = [row, col]
        down_l_pos = [row, col]
        up_l_pos = [row, col]

        positions = [up_r_pos, down_r_pos, down_l_pos, up_l_pos]

        l_win_coins = [(row, col)]
        r_win_coins = [(row, col)]

        for pos, step in zip(positions, steps):
            pos[0] += step[0]
            pos[1] += step[1]

        up_r = self.check_cell_state(*positions[0], player)
        down_r = self.check_cell_state(*positions[1], player)
        down_l = self.check_cell_state(*positions[2], player)
        up_l = self.check_cell_state(*positions[3], player)

        directions = [up_r, down_r, down_l, up_l]

        left_count = 1
        right_count = 1

        while any(directions):
            for i in range(len(directions)):
                print(f"DIRECTION: {i} {directions[i]} | POSITION: {positions[i]} | ")
                if directions[i]:
                    if i % 2 == 0:

                        right_count += 1
                        print(right_count)
                        r_win_coins.append(tuple(positions[i]))
                    else:
                        left_count += 1
                        l_win_coins.append(tuple(positions[i]))

                    positions[i][0] += steps[i][0]
                    positions[i][1] += steps[i][1]

                    directions[i] = self.check_cell_state(*positions[i], player)

            if left_count > 3:
                print("DIAG WIN")
                return l_win_coins
            if right_count > 3:
                print("DIAG WIN")
                return r_win_coins

    def one_directional_win(self, direction, row, col, player):

        dec_positions = [row, col]
        inc_positions = [row, col]
        win_coins = [inc_positions[direction]]

        dec_positions[direction] -= 1
        inc_positions[direction] += 1

        dec = self.check_cell_state(*dec_positions, player)
        inc = self.check_cell_state(*inc_positions, player)

        count = 1

        while dec or inc:
            if dec:
                print(f"DEC {direction} 0 row 1 col : {dec_positions[direction]}")
                win_coins.append(dec_positions[direction])
                dec_positions[direction] -= 1
                count += 1

                dec = self.check_cell_state(*dec_positions, player)

            if inc:
                print(f"INC {direction} 0 row 1 col : {dec_positions[direction]}")
                win_coins.append(inc_positions[direction])
                inc_positions[direction] += 1
                count += 1

                inc = self.check_cell_state(*inc_positions, player)

            if count > 3:
                print("TWO DIRECTIONAL WIN")
                win_coins.sort()
                if direction == 0:
                    return [(row, col) for row in win_coins]
                elif direction == 1:
                    return [(row, col) for col in win_coins]
        return False

    def update_cell(self, row, col, player):
        self.matrix[row][col] = player

    def find_bottom_empty_cell(self, col):
        i = len(self.matrix) - 1
        while True:
            if self.matrix[i][col] == 0:
                return i
            i -= 1

    def drop_piece(self, row, col, player):

        self.update_cell(row, col, player)
        return row

    def print(self):
        for row in self.matrix:
            print(row)


class Board:
    def __init__(self, coords, pm: list, canvas: Canvas):

        self.coords = coords

        self.canvas = canvas
        self.matrix = pm

        self.current_row = 0
        self.current_col = 0

        self.all_coins = []

        self.win_coins = []

    def draw_next_slot(self):

        if self.current_row > len(self.matrix) - 1:
            self.current_row = 0
            self.current_col = 0
            return

        col = self.matrix[self.current_row][self.current_col]
        self.canvas.create_oval(*col, fill="white")
        self.canvas.after(25, self.draw_next_slot)

        if self.current_col >= len(self.matrix[0]) - 1:
            self.current_row += 1
            self.current_col = 0
        else:
            self.current_col += 1

    def initialize_empty_board(self):
        self.canvas.create_rectangle(*self.coords, fill="#4169E1")
        self.draw_next_slot()

    def draw_coin(self, row, col, fill):
        coin = self.canvas.create_oval(*self.matrix[row][col], fill=fill)
        self.all_coins.append(coin)

    def animate_win(self):
        if len(self.win_coins) <= 0:
            return

        self.draw_coin(self.win_coins[-1][0], self.win_coins[-1][1], fill="red")
        del self.win_coins[-1]
        self.canvas.after(100, self.animate_win)

    def animate_coins_fall(self):
        to_delete = []

        if len(self.all_coins) < 1:
            return
        for move_coin in self.all_coins:
            if self.canvas.coords(move_coin)[1] > self.coords[3]:
                to_delete.append(move_coin)
            else:
                self.canvas.move(move_coin, 0, 10)

        for delete_coin in to_delete:
            self.canvas.delete(delete_coin)
            self.all_coins.remove(delete_coin)

        self.canvas.after(10, self.animate_coins_fall)


class Game:
    def __init__(self, c_width, c_height, b_width, b_height, rows=6, cols=7, p1_color='yellow', p2_color='orange',
                 debug=False):
        self.debug = debug

        self.root = Tk()
        self.canvas = Canvas(self.root, width=c_width, height=c_height, bg='white')
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)

        self.turn = 0
        self.player = 1
        self.player_colors = {1: p1_color, 2: p2_color}

        self.positional_matrix = PositionalMatrix(c_width, c_height, b_width, b_height, rows, cols)
        self.state_matrix = StateMatrix(rows, cols)
        self.board = Board(self.positional_matrix.b_coords, self.positional_matrix.matrix, self.canvas)

        self.x_windows = self.positional_matrix.generate_x_windows()
        self.y_windows = self.positional_matrix.generate_y_windows()

        self.board.initialize_empty_board()

        print(len(self.state_matrix.matrix))
        print(len(self.positional_matrix.matrix))
        print(self.y_windows)
        print(self.x_windows)
        self.root.mainloop()

    def reset_game(self):
        self.canvas.delete("all")
        self.state_matrix.initialize_empty_board()
        self.board.initialize_empty_board()

    def handle_click(self, event):

        self.turn += 1

        col = self.get_clicked_column(event.x)

        if not self.debug:
            row = self.state_matrix.find_bottom_empty_cell(col)
            if self.turn % 2 == 0:
                self.player = 1
            else:
                self.player = 2
        else:
            row = self.get_clicked_row(event.y)

        self.state_matrix.drop_piece(row, col, self.player)

        win = (
                self.state_matrix.one_directional_win(0, row, col, self.player) or
                self.state_matrix.one_directional_win(1, row, col, self.player) or
                self.state_matrix.diagonal_win(row, col, self.player)
        )

        if win:
            print(win)
            self.board.win_coins = win
            self.board.animate_win()
            self.canvas.after(500, self.board.animate_coins_fall)
            self.canvas.after(2000, self.reset_game)
            return

        self.board.draw_coin(row, col, self.player_colors[self.player])
        self.state_matrix.print()

    def get_clicked_column(self, click_x):
        for i in range(1, len(self.x_windows)):
            if self.x_windows[i - 1] <= click_x <= self.x_windows[i]:
                return i - 1

    def get_clicked_row(self, click_y):
        for i in range(1, len(self.y_windows)):
            if self.y_windows[i - 1] <= click_y <= self.y_windows[i]:
                return i - 1
