import socket
import threading
import json
import argparse
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

def get_csu_cs_machine_ip(name):
    try:
        ip_address = socket.gethostbyname(name)
        return ip_address
    except socket.gaierror:
        return f"Unable to get IP address for domain {name}"

def parse_args():
    parser = argparse.ArgumentParser(description="Parse IP address and port or a machine name.")
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--ip", type=str, help="IP address of the server")
    group.add_argument("--port", type=int, help="Port number", default=12345)
    group.add_argument("--machine", type=str, help="Machine name of the server")

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()

    if args.machine:
        ip = get_csu_cs_machine_ip(args.machine)
    elif args.ip:
        ip = args.ip
    else:
        print("Please specify an ip or a machine")

    print(f"Trying to connect to {ip}:{args.port}")
    client = client(host=ip, port=args.port)
    client.start()