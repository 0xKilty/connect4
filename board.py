from slots import Slots, TextStyling

class Board:
    def __init__(self):
        self.board = [[Slots.YELLOW for _ in range(7)] for _ in range(6)]

    def display_board(self):
        surround = lambda string, around: f"{around}{string}{around}"
        format_edges = lambda left, middle, right: left + f"───{middle}" * 6 + f"───{right}"
        top_edge =    format_edges("┌", "┬", "┐")
        middle_edge = format_edges("\n├", "┼", "┤\n")
        bottom_edge = format_edges("└", "┴", "┘")

        print(TextStyling.BOLD.value, TextStyling.BLUE.value)
        print(top_edge)
        middle_rows = []
        for row in self.board:
            middle_rows.append("│" + " │".join(slot.value for slot in row) + " │")
        print(middle_edge.join(middle_rows))
        print(bottom_edge)
        print(TextStyling.RESET.value)

board = Board()

board.display_board()

'''
  │  │  │
 ─┼──┼──┤
  └──┼──┘

     │ 
───┴─
     │   

              
 ┌─────┐ 

      
───┬─

  │    │  
  ├────┤  
     
'''
        