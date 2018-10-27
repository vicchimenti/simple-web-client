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
    print("full URL if: " + full_URL)
else :
    protocol, full_URL = (user_input.split(delim , 2))
    print("full URL else: " + full_URL)


# search for user provided port number
delim = ":"
x = full_URL.find(delim)
print("x :: " + str(x))
if x != -1 :
    host, portPathway = (full_URL.split(delim, 2))
    print("host if: " + host)
    print("portPath if: " + portPathway)
    delim = "/"
    x = portPathway.find(delim)
    portstr = portPathway[:x]
    path = portPathway[x:]
    print("host if: " + host)
    print("Path if: " + path)
    print("portstr if: " + portstr)
    port = int(portstr)
else :
    # parse domain from path
    delim = "/"
    x = full_URL.find(delim)
    host = full_URL[:x]
    path = full_URL[x:]
    print("host else: " + host)
    print("Path else: " + path)



# Set up a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect as client to a selected server
sock.connect((host, port))

# prepare message for server
message = "GET "  + path + " HTTP/1.1\r\nConnection: close\r\nHost: " + host + "\r\n\r\n"
print ("Here is your message: \n" + message)
sock.send(message.encode('utf-8'))
#sock.sendall(message.encode())
#response = sock.recv(4096)
#print (response.decode('utf-8'))
while True :
    response = sock.recv(40430)
    if  not response : break
    #if  response == " ": break
    print (response.decode('utf-8'))
    #sys.exit()

# Close the connection
sock.close()
print ("Success! Connection Closed")
sys.exit()
