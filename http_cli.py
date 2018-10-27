import socket
import sys


# default port number to 80
port = 80

# get user input from command line
user_input = sys.argv[1]
print("user_input: " + user_input)

# parse user_input to expose full URL
delim = "//"
x = user_input.find(delim)
print("x //: " + str(x))
if x == -1 :
    full_URL = user_input
else :
    li = list(user_input.split(delim , 2))
    full_URL = li[1]
print("full URL: " + full_URL)

# search for user provided port number
delim = ":"
x = full_URL.find(delim)
print("x :: " + str(x))
if x != -1 :
    li = list(full_URL.split(delim, 2))
    host = li[0]
    portPathway = li[1]
    print("host: " + host)
    print("portPath: " + portPathway)
    delim = "/"
    port = portPathway[:delim]
    path = portPathway[delim:]
else
    # parse domain from path
    delim = "/"
    x = full_URL.find(delim)
    host = full_URL[:x]
    path = full_URL[x:]



print("host: " + host)
print("Path: " + path)

# message for server
#message = sys.argv[2]  will need to collect file info and port num from cmdline

#print(message)

# Set up a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sys.exit()

# Connect as client to a selected server
# on a specified port
sock.connect((host, port))

# prepare message for server
message = "GET "  + path + "\n\n"
print ("Here is your message: " + message)
sock.send(message.encode('ascii'))
while True:
        response = sock.recv(1024)
        if response == "": break
        print (response.decode('ascii')),

# Close the connection
sock.close()
print ("Success! Connection Closed")
