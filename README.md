# Connect Four

![](https://img.clipart-library.com/2/clip-connect-fours/clip-connect-fours-17.png)

This is a simple Connect Four game implemented using Python and sockets.

**How to play:**
1. **Start the server:** Run the `server.py` script. (`python3 server.py -p <PORT>`)
2. **Connect clients:** Run the `client.py` script on two different machines or terminals. (`python3 client.py -i <IP> -p <PORT>`)
3. **Play the game:** Players take turns entering their moves. The first player to get four in a row wins!

**Messaging protocol**
- `join` - allows players to join the game
- `move` - allows players to make moves in the game if they are valid and it's their turn
- `chat` - allows players to chat with eachother
- `quit` - allows players to quit the game

**Messaging protocol (After the end of a Game)**
- `yes` - starts a new game, if both clients type yes.
- `no` - ends the game.

**Security Concerns**
- **Denial of Service** - This client server architecture is vulnerable to DoS attacks in that there is no rate limiting in place on the server to slow large amounts of traffic.
- **Lack of Authentication** - Standalone, the game has no authentication and is vulnerable to port scanning and identification. 
- **Memory Corruption** - Even though Python is assumed to be memory safe, there still exists the possibility of a memory corruption vulnerability (e.g. buffer overflow) or a memory error (e.g. stack overflow).
- **Session Hijacking** - If a client disconnects, then reconnects, there is no knowing if that user is the same as the original, an attacker could continuously attempt to connect to the server, waiting for a client to disconnect and take their place.

**Retrospective**
- **What went right**
- **What could be improved upon**

**Technologies used:**
* Python
* Sockets

**Additional resources:**
* [Python documentation](https://docs.python.org/3/)
* [sockets tutorial](https://docs.python.org/3/library/socket.html)
