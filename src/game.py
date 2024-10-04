from .board import Board
from .player import Player
from .hardcodes import Slots, TextStyling, Logging

class Game:
    def __init__(self):
        self.board = Board()
        self.player1 = Player("1", Slots.RED)
        self.player2 = Player("2", Slots.YELLOW)

    def start(self):
        move = True
        log = ""
        possible_moves = list(range(1, 8))
        while True:
            playing_player = self.player1 if move else self.player2

            print(TextStyling.CLEAR.value)
            print(f"Player {playing_player.name} move: {playing_player.icon.value}\n")
            print('', ' '.join(f" {num} " for num in possible_moves))
            print(self.board)
            print(log)

            column_pick = input("Pick a column [1-7]: ")
            if column_pick.isdigit() and int(column_pick) in possible_moves:
                column_pick = int(column_pick)
            else:
                log = f"{Logging.ERROR.value} Invalid move! Please pick a valid column."
                continue

            if not self.board.insert(column_pick, playing_player.icon):
                log = f"{Logging.WARNING.value}  Column {column_pick} is full!"
                continue

            if self.board.check_winner(playing_player.icon):
                print(TextStyling.CLEAR.value)
                print(f"{TextStyling.BOLD.value}{TextStyling.GREEN.value}Player {playing_player.name} wins!{TextStyling.RESET.value}")
                print(self.board)
                break

            log = ""
            move = not move
