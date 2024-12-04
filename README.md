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

**How to run the game**

On the server, simply run
```python
$ python3 server.py
```

Then to connect using a client, run
```python
$ python3 client.py --ip <server ip>
```

**Roadmap**

We would like to take this project further in terms of UI. Using a Web UI and setting up the server to handle many games at once would make the game more easily accessible to people hence gaining a lot more users. Then we can take it a step further with an account system for users to keep track of the games they have played and who they player against. Then we can introduce an elo system to make matchmaking more fair where better players will be paired with better players. It starts with accessibility for people in the form of a website, then accounts, then an elo system. That is where we would take this project.

**Retrospective**
- **What went right**
  - Client server architecture works well and there are few errors for the communication and if there are errors, they are properly handled.
  - The game state and game requierments are good where there have to be 2 players in order for the game to start and both players need to be present for a move to take place. Then all the rules and logic of connect four are taken into account and function properly.
- **What could be improved upon**
  - The UI is not great as there are some weird formatting issues on some terminals, so a better option would be to create a Web UI.
  - If, from the perspective of the server, a player disconnects, then reconnects, there is no way of knowing if that is the same player, so the session could be hijacked. There are a couple of other security concerns that need to be addressed.

**Technologies used:**
* Python
* Sockets

**Additional resources:**
* [Python documentation](https://docs.python.org/3/)
* [sockets tutorial](https://docs.python.org/3/library/socket.html)
