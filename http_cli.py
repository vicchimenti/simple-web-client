# http_cli.py

import socket

# Set up a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get server name
host = socket.gethostname()

# get prot number
# port hardcoded
port = 80

# Connect as client to a selected server
# on a specified port
sock.connect((host, port))

# Protocol exchange - sends and receives
sock.send("GET /3/howto/sockets.html HTTP/1.0\n\n")
while True:
        response = sock.recv(1024)
        if response == "": break
        print (response.decode('ascii')),

# Close the connection
sock.close()
print ("Success! Connection Closed")
