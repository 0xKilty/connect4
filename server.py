import socket
import threading
import logging
import json
from src.game import Game

class Server:
    def __init__(self, host='localhost', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(2)
        self.clients = []
        self.game = Game()
        self.current_turn = 1

    def broadcast(self, message):
        for client in self.clients:
            try:
                client.sendall(f"{message}\n".encode())
            except Exception as e:
                logging.error(f"Unexpected error sending message: {e}")

    def handle_join(self, player_id, addr):
        log_message = f"{color_playerid(player_id)} joined from {addr[0]}:{addr[1]}" 
        self.broadcast(log_message)

    def handle_chat(self, player_id, message):
        chat_message = f"{color_playerid(player_id)}: {message}"
        self.broadcast(chat_message)

    def handle_quit(self, player_id):
        chat_message = f"{color_playerid(player_id)} is quitting"
        self.broadcast(chat_message)
        if client_socket in self.clients:
            self.clients.remove(client_socket)

    def handle_move(self, player_id, message):
        column_pick = message['data']['pick']
        if self.game.board.insert(int(column_pick), self.game.player1.icon if player_id == 1 else self.game.player2.icon):
            game_state_message = [
                f"{color_playerid(player_id)} picked column {column_pick}.",
                ' '.join(f" {num} " for num in list(range(1, 8))),
                str(self.game.board),
                f"{color_playerid(3 - player_id)}'s turn"
            ]
            self.broadcast('\n'.join(game_state_message))

            if self.game.board.check_winner(self.game.player1.icon if player_id == 1 else self.game.player2.icon):
                self.broadcast(f"Player {player_id} wins!")
                return True
            self.current_turn = 2 if player_id == 1 else 1
            return False
        else:
            client_socket.sendall("Column is full or invalid! Try again.\n".encode())
            return False

    def handle_client(self, client_socket, player_id, addr):
        self.clients.append(client_socket)
        try:
            while True:
                data = client_socket.recv(1024).decode()
                if not data: break
                message = json.loads(data)
                logging.debug(f"Received message from {color_playerid(player_id)}: {message}")

                if message['type'] == 'join':
                    self.handle_join(player_id, addr)
                elif message['type'] == 'move':
                    if player_id != self.current_turn:
                        client_socket.sendall("It's not your turn! Please wait.\n".encode())
                        continue
                    if self.handle_move(player_id, message):
                        break
                elif message['type'] == 'chat':
                    self.handle_chat(player_id, message['data']['message'])
                elif message['type'] == 'quit':
                    self.handle_quit(player_id)
                    break
                else:
                    logging.info(f"Received invalid packet type {message['type']}")
        except socket.error as e:
            logging.error(f"Socket error handling client {color_playerid(player_id)}: {e}")
        except json.JSONDecodeError:
            logging.error("Received malformed JSON message")
        except Exception as e:
            logging.error(f"Error handling {color_playerid(player_id)}: {e}")
        finally:
            logging.info(f"Closing connection for {color_playerid(player_id)}")
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            client_socket.close()


    def start(self):
        logging.info("Server started and waiting for clients...")
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                player_id = len(self.clients) + 1
                threading.Thread(target=self.handle_client, args=(client_socket, player_id, addr), daemon=True).start()
        finally:
            self.server_socket.close()
            logging.info("Server socket closed.")

def color_playerid(player_id):
    color = (2 * player_id) - 1
    return f"\033[3{color};1mPlayer {player_id}\033[0m"

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    server = Server()
    try:
        server.start()
    except KeyboardInterrupt:
        logging.info("Server exiting gracefully.")
