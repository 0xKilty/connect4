import socket
import threading
from src.game import Game

class server:
    def __init__(self, host='localhost', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)
        self.clients = []
        self.game = Game()
        self.current_turn = 1

    def broadcast(self, message):
        message_with_newline = message + "\n"
        for client in self.clients:
            try:
                client.sendall(message_with_newline.encode())
            except Exception as e:
                print(f"Error sending message: {e}")

    def handle_client(self, client_socket, player_id):
        self.clients.append(client_socket)
        try:
            while True:
                column_pick = client_socket.recv(1024).decode()
                if not column_pick:
                    break

                if player_id != self.current_turn:
                    client_socket.sendall("It's not your turn! Please wait.\n".encode())
                    continue

                if self.game.board.insert(int(column_pick), self.game.player1.icon if player_id == 1 else self.game.player2.icon):
                    self.broadcast(f"Player {player_id} picked column {column_pick}.")
                    self.broadcast(str(self.game.board))  # Send the updated board

                    if self.game.board.check_winner(self.game.player1.icon if player_id == 1 else self.game.player2.icon):
                        self.broadcast(f"Player {player_id} wins!")
                        break
                    
                    self.current_turn = 2 if player_id == 1 else 1
                else:
                    client_socket.sendall("Column is full or invalid! Try again.\n".encode())
        finally:
            client_socket.close()
            self.clients.remove(client_socket)

    def start(self):
        print("Server started and waiting for clients...")
        while True:
            client_socket, addr = self.server_socket.accept()
            player_id = len(self.clients) + 1
            print(f"Client {player_id} connected from {addr}")
            threading.Thread(target=self.handle_client, args=(client_socket, player_id), daemon=True).start()

if __name__ == "__main__":
    server = server()
    server.start()
