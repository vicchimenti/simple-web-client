# Vic Chimenti
# CPSC 5510 FQ18
# http_cli.py
# Created           10/19/2018
# Last Modified     10/27/2018
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
#print("x :: " + str(x))

# if there is no colon in the user input
if x != -1 :
    # parse the host domain from the full URL
    host, portPathway = (full_URL.split(delim, 2))
    #parse domain from path
    delim = "/"
    x = portPathway.find(delim)
    portstr = portPathway[:x]
    path = portPathway[x:]
    #convert the port number into an integer
    port = int(portstr)

# if there is a colon in the user input
else :
    # parse domain from path
    delim = "/"
    x = full_URL.find(delim)
    host = full_URL[:x]
    path = full_URL[x:]




# Set up a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Connect as client to a selected server
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
sock.sendall(message.encode('utf8'))

# wait for entire response
full_response = "\n"
while True :
    # max receive size is 2^16
    response = sock.recv(65536)
    # decode bytes to string format
    response_str = response.decode('utf8')
    # concatenate string while receive loop lives
    full_response += response_str
    # end loop when server response is complete
    if  not response : break

# print full response as a string
print (full_response)




# search for end of header
try :
    delim = "\r\n\r\n"
    x = full_response.find(delim)
    print("x :: " + str(x))
    # if there is no delimiter
    if x != -1 :
        # parse the host domain from the full URL
        message_header, message_body = (full_response.split(delim, 2))
    else : print ("ERROR, Incorrect Header Response")
except :
    tb = sys.exc_info()
    print ("EXCEPTION: \n" + tb)
else : print (message_header)




# display message body
print (message_body)

# Close the connection
sock.close()

# eof
