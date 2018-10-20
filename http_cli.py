# http_cli.py

import socket

# Set up a TCP/IP socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# Connect as client to a selected server
# on a specified port
s.connect(("docs.python.org",80))

# Protocol exchange - sends and receives
s.send("GET /3/howto/sockets.html HTTP/1.0\n\n")
while True:
        resp = s.recv(1024)
        if resp == "": break
        print resp,

# Close the connection
s.close()
print "\nSuccess! Connection Closed"
