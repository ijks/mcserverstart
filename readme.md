This is a small set of python scripts meant for starting any Minecraft server remotely, as long as its .jar or startup script is runnable. It simply uses standard TCP sockets with python's `socket` and `socketserver` modules. The client and server communicate using a set of standard messages:

Server responses:
 * MCSERV_00 - Empty message. Means the server didn't do anything whatsoever.
 * MCSERV_OK - (Re)start succesful. As far as the server knows, starting the server went fine.
 * MCSERV_AR - The server is already running. The client may send a restart request after this (not yet implemented successfully)
 * MCSERV_?? - Generic error (should actually be called unknown command). The server didn't understand the client's request.
 * MCSERV_ER - Server error. There was a serverside error.

Client requests:
 * MCSERV_ON - Turn the Minecraft server on.
 * MCSERV_RS - Restart an already running server. Not yet implemented