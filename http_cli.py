# http_cli.py

import socket
import sys
import http.client

# get user input for hostname
host = sys.argv[1]
# message for server
#message = sys.argv[2]  will need to collect file info and port num from cmdline
print("host: " + host)
#print(message)

# Set up a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get prot number
# port hardcoded
port = 80

# Connect as client to a selected server
# on a specified port
sock.connect((host, port))

# prepare message for server
message = 'GET /3/howto/sockets.html HTTP/1.1' + "\n\n"
print ("Here is your message: " + message)
sock.send(message.encode('ascii'))
while True:
        response = sock.recv(1024)
        if response == "": break
        print (response.decode('ascii')),

# Close the connection
sock.close()
print ("Success! Connection Closed")
