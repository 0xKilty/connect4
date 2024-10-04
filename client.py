import socket
import threading
from src.game import Board, Slots, TextStyling

class client:
    def __init__(self, host='localhost', port=12345):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        self.board = Board()
        self.player_number = None

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if message:
                    if "picked" in message or "wins" in message or "not your turn" in message:
                        print(message + "\n")
                    elif "Column is full or invalid!" in message:
                        print(message + "\n")
                    else:
                        self.update_board(message)
            except Exception as e:
                print(f"Error: {e}")
                break

    def update_board(self, message):
        print(f"\n{message}\n")

    def start(self):
        threading.Thread(target=self.receive_messages, daemon=True).start()
        while True:
            column_pick = input("Pick a column [1-7]: ")
            self.client_socket.sendall(column_pick.encode())

if __name__ == "__main__":
    client = client()
    client.start()
