﻿# Connect Four

![](https://img.clipart-library.com/2/clip-connect-fours/clip-connect-fours-17.png)

This is a simple Connect Four game implemented using Python and sockets.

**How to play:**
1. **Start the server:** Run the `server.py` script.
2. **Connect clients:** Run the `client.py` script on two different machines or terminals.
3. **Play the game:** Players take turns entering their moves. The first player to get four in a row wins!

**Messaging protocol**
- `join` - allows players to join the game
- `move` - allows players to make moves in the game if they are valid and it's their turn
- `chat` - allows players to chat with eachother
- `quit` - allows players to quit the game

**Technologies used:**
* Python
* Sockets

**Additional resources:**
* [Python documentation](https://docs.python.org/3/)
* [sockets tutorial](https://docs.python.org/3/library/socket.html)
