import socket
import threading
import json
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
                if not message: break
                print("\r\n" + message, end="")
                self.display_prompt()
            except Exception as e:
                print(f"Error: {e}")
                break

    def update_board(self, message):
        print(f"\n{message}\n")

    def display_prompt(self):
        print("q (quit) c (chat) pick a column [1-7]> ", end='', flush=True)

    def start(self):
        join_message = message_to_json("join")
        self.client_socket.sendall(join_message)
        threading.Thread(target=self.receive_messages, daemon=True).start()
        while True:
            self.display_prompt()
            cli_pick = input()
            if cli_pick == "c":
                chat_data = input("Message: ")
                message = message_to_json("chat", {"message": chat_data})
            elif cli_pick == "q":
                message = message_to_json("quit")
                self.client_socket.close()
            elif is_valid_column_pick(cli_pick):
                message = message_to_json("move", {"pick": cli_pick})
            else:
                print(f"Invalid option {cli_pick}")
                continue
            self.client_socket.sendall(message)

def message_to_json(message_type, data=None):
    message = {
        "type": message_type,
        "data": data
    }
    json_message = json.dumps(message)
    return json_message.encode()

def is_valid_column_pick(column_pick):
    if column_pick.isdigit():
        number = int(column_pick)
        return 1 <= number <= 7
    return False

if __name__ == "__main__":
    client = client()
    client.start()
