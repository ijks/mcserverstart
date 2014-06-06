#Introduction
This is a small set of python scripts meant for starting any Minecraft server remotely, as long as its .jar or startup script is runnable. It simply uses standard TCP sockets with python's `socket` and `socketserver` modules. The client and server communicate using a set of standard messages. The client asks the user if they want to start the configured server. It then sends a start request, and if the MC server is not running, the Python server will start it. If the server is already running, the client can shut down, or alternatively, send a restart request.

# Messages
Server responses:
 * MCSERV_00 - Empty message. Means the server didn't do anything whatsoever.
 * MCSERV_OK - (Re)start succesful. As far as the server knows, starting the server went fine.
 * MCSERV_AR - The server is already running. The client may send a restart request after this (not yet implemented successfully)
 * MCSERV_?? - Generic error (should actually be called unknown command). The server didn't understand the client's request.
 * MCSERV_ER - Server error. There was a serverside error.

Client requests:
 * MCSERV_ON - Turn the Minecraft server on.
 * MCSERV_RS - Restart an already running server. Not yet implemented

#Things to add
 * Restart function. Having problems with that, because `Popen.kill()` doesn't really seem to do anything to the server...
 * Maybe turn it into a complete server wrapper? Who knows...
 * New world command