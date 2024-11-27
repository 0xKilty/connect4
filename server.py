import socket
import threading
import logging
import json
import time
from src.game import Game

class Server:
    def __init__(self, host='0.0.0.0', port=12345):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.up = False
        try:
            self.server_socket.bind((host, port))
            self.up = True
        except OSError as e:
            if e.errno == 98:
                logging.error(f"Error: Port {host}:{port} is already in use. Please try a different port.")
                self.server_socket.close()
                return
        self.server_socket.listen(2)
        self.clients = []
        self.game = Game()
        self.current_turn = 1
        self.waiting_for_play_again = False

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
        if self.waiting_for_play_again:
            return

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
                self.broadcast("Do you want to play again? (yes/no)")
                self.waiting_for_play_again = True
                self.play_again_decision = {1: None, 2: None}
                return True
            self.current_turn = 2 if player_id == 1 else 1
            return False
        else:
            client_socket.sendall("Column is full or invalid! Try again.\n".encode())
            return False

    def handle_client(self, client_socket, player_id, addr):
        self.clients.append(client_socket)
        self.play_again_decision = {1: None, 2: None}

        try:
            while True:
                data = client_socket.recv(1024).decode()
                if not data: break
                message = json.loads(data)
                logging.debug(f"Received message from {color_playerid(player_id)}: {message}")

                if message['type'] == 'join':
                    self.handle_join(player_id, addr)
                elif message['type'] == 'move':
                    if len(self.clients) != 2:
                        client_socket.sendall("Not enough players, please wait for another player to join.\n".encode())
                        continue
                    if not self.waiting_for_play_again:
                        if player_id != self.current_turn:
                            client_socket.sendall("It's not your turn! Please wait.\n".encode())
                            continue
                        if self.handle_move(player_id, message):
                            self.broadcast("Waiting for both players to decide...")
                    else:
                        client_socket.sendall("Please respond with 'yes' or 'no' to play again.\n".encode())
                elif message['type'] == 'play_again' and self.waiting_for_play_again:
                    response = message['data'].get('response', '').lower()
                    self.play_again_decision[player_id] = response
                    other_player_id = 3 - player_id
                    if self.play_again_decision[other_player_id] is None:
                        self.broadcast(f"{color_playerid(player_id)} has decided. Waiting for the other player...")
                    if self.play_again_decision[1] == "yes" and self.play_again_decision[2] == "yes":
                        self.reset_game()
                        self.waiting_for_play_again = False
                    elif "no" in self.play_again_decision.values():
                        self.broadcast("Game over. One of the players chose not to continue.")
                        break
                elif message['type'] == 'quit':
                    self.handle_quit(player_id)
                    break
                elif message['type'] == 'chat':
                    self.handle_chat(player_id, message['data']['message'])
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

    def reset_game(self):
        self.game = Game()
        self.current_turn = 1
        self.broadcast("A new game has started! Player 1's turn.")
        self.play_again_decision = {1: None, 2: None}
        self.waiting_for_play_again = False

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
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(f"server_{time.strftime('%Y%m%d_%H%M%S')}.log"),
            logging.StreamHandler()
        ]
    )


    server = Server()
    try:
        if server.up:
            server.start()
    except KeyboardInterrupt:
        logging.info("Server exiting gracefully.")
