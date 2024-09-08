from .hardcodes import Slots, TextStyling

class Board:
    def __init__(self):
        self.board = [[Slots.EMPTY for _ in range(7)] for _ in range(6)]
        self.highlighted = []

    def __str__(self):
        format_edges = lambda left, middle, right: left + f"───{middle}" * 6 + f"───{right}"
        top_edge =      format_edges("┌", "┬", "┐\n")
        middle_edge = format_edges("\n├", "┼", "┤\n")
        bottom_edge = format_edges("\n└", "┴", "┘")

        middle_rows = []
        for row in self.board:
            middle_rows.append("│" + " │".join(slot.value for slot in row) + " │")

        board_string = []
        board_string.append(TextStyling.BOLD.value + TextStyling.BLUE.value)
        board_string.append(top_edge)
        board_string.append(middle_edge.join(middle_rows))
        board_string.append(bottom_edge)
        board_string.append(TextStyling.RESET.value)

        return ''.join(board_string)

    def insert(self, column_number, slot_type):
        column_index = column_number - 1

        if self.board[0][column_index] != Slots.EMPTY:
            return False

        for row in reversed(self.board):
            if row[column_index] == Slots.EMPTY:
                row[column_index] = slot_type
                return True

        return False
    
    def check_winner(self, slot_type):
        for row in range(6):
            for col in range(7):
                if self.board[row][col] == slot_type:
                    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
                    for row_step, col_step in directions:
                        winning_indexes = self.check_direction(row, col, row_step, col_step, slot_type)
                        if winning_indexes:
                            return winning_indexes
        return None
    
    def check_direction(self, row, col, row_step, col_step, slot_type):
        indexes = []
        for i in range(4):
            r = row + i * row_step
            c = col + i * col_step
            if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == slot_type:
                indexes.append((r, c))
            else:
                break
        return indexes if len(indexes) == 4 else None

