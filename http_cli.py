# Vic Chimenti
# CPSC 5510 FQ18
# http_cli.py
# Created           10/19/2018
# Last Modified     10/28/2018
# Simple Web Client in Python3
# usr/bin/python3


import socket
import sys




# default port number to 80
port = 80

# get user input from command line
user_input = sys.argv[1]




# parse user_input to expose full URL
delim = "//"
x = user_input.find(delim)

# if no http:// protocol was entered by the user
if x == -1 : full_URL = user_input

# if an http:// protocol was entered with the URL
else : protocol, full_URL = (user_input.split(delim , 2))




# search for user provided port number
delim = ":"
x = full_URL.find(delim)

# if there is a colon in the user input
if x != -1 :
    # parse the host domain from the full URL
    host, portPathway = (full_URL.split(delim, 2))
    # now parse the port number from the path with a new delimiter
    delim = "/"
    x = portPathway.find(delim)
    portstr = portPathway[:x]
    path = portPathway[x:]
    #convert the port number from a string into an integer
    port = int(portstr)

# if there is no colon in the user input
else :
    # parse domain from path with new delimiter
    delim = "/"
    x = full_URL.find(delim)
    host = full_URL[:x]
    path = full_URL[x:]




# Set up a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server as a client
sock.connect((host, port))




# prepare message for server and display
try :
    message = "GET "  + path \
                      + " HTTP/1.1\r\nConnection: close\r\nHost: " \
                      + host \
                      + "\r\n\r\n"
except :
    tb = sys.exc_info()
    print ("EXCEPTION: \n" + tb)
else :
    print (message)

# send message to the web server
sock.sendall(message.encode('utf-8'))

byte_file = open(tempFile.txt, 'wb')
while True :
    # max receive size is 2^16
    response = sock.recv(65536)
    byte_file.write(response, 'rb')
    # decode bytes to string format
    #response_str = response.decode('utf-8')
    # concatenate string while receive loop lives
    #full_response += response_str
    if  not response : break


# declare parsing variables and scrub for non-HTML/txt file type
full_response = "\n"
delim = "\r\n\r\n"
delim_in_bytes = delim.encode('utf-8')
mutable_response = bytearray(b'\x00\x0F')
png = '.png'
jpg = '.jpg'
gif = '.gif'
pdf = '.pdf'
x = path.find(png)
xy = path.find(jpg)
xyz = path.find(gif)
xyzz = path.find(pdf)


# print("x = : " + str(x) + str(xy) + str(xyz) + str(xyzz))
if not any ((x, xy, xyz, xyzz)) :
    # path is not an image type
    while True :
        # max receive size is 2^16
        response = sock.recv(65536)
        # decode bytes to string format
        response_str = response.decode('utf-8')
        # concatenate string while receive loop lives
        full_response += response_str
        if  not response : break
    #declare header and body variables
    header = body = '\n'
    # parse the response search for end of header
    try :
        x = full_response.find(delim)
        # if the delimiter is found extract the header and body
        if x != -1 :
            header = full_response[:x]
            body = full_response[x:]
            # add the delimiter back to the end of the header
            header += delim
            #remove the delimiter from the front of the body
            body = body.replace(delim, '\n', 1)
        else : print ("ERROR, Incorrect Header")
    except :
        tb = sys.exc_info()
        print ("EXCEPTION: \n" + tb)
    else : print (header)

    # display message body
    print (body)
    # Close the connection
    sock.close()
    sys.exit()



else :
    #path is an image type
    while True :
        # max receive size is 2^16
        response = sock.recv(65536)
        if  response.find(delim_in_bytes) : break
        else :
            # decode bytes to string format
            response_str = response.decode('utf-8')
            # concatenate string while receive loop lives
            full_response += response_str

    #response = bytes(mutable_response)
    print(full_response)
    # Close the connection
    sock.close()
    sys.exit()

# sys.exit()
# print("x != -1: " + str(x) + str(xy) + str(xyz) + str(xyzz))
# wait for entire response







# Close the connection
#sock.close()

# eof
