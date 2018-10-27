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
#print("user_input: " + user_input)




# parse user_input to expose full URL
delim = "//"
x = user_input.find(delim)
#print("x //: " + str(x))

# if no http:// protocol was entered by the user
if x == -1 : full_URL = user_input
    #print("full URL if: " + full_URL)

# if an http:// protocol was entered with the URL
else : protocol, full_URL = (user_input.split(delim , 2))
    #print("full URL else: " + full_URL)




# search for user provided port number
delim = ":"
x = full_URL.find(delim)
#print("x :: " + str(x))

# if there is no colon in the user input
if x != -1 :
    # parse the host domain from the full URL
    host, portPathway = (full_URL.split(delim, 2))
    #print("host if: " + host)
    #print("portPath if: " + portPathway)
    #parse domain from path
    delim = "/"
    x = portPathway.find(delim)
    portstr = portPathway[:x]
    path = portPathway[x:]
    #print("host if: " + host)
    #print("Path if: " + path)
    #print("portstr if: " + portstr)
    #convert the port number into an integer
    port = int(portstr)

# if there is a colon in the user input
else :
    # parse domain from path
    delim = "/"
    x = full_URL.find(delim)
    host = full_URL[:x]
    path = full_URL[x:]
    #print("host else: " + host)
    #print("Path else: " + path)




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

#delim = "\r\n\r\n"
# wait for entire response
#response = sock.recv(65536)
full_response = "\r\n"
while True :
    response = sock.recv(65536)
    full_response.join([response, full_response])
    if  not response : break
print (full_response.decode('utf8'))
#print ("response_body: " + response_body.decode('utf8'))





# Close the connection
sock.close()
#print ("Success! Connection Closed")


#        try :
#            response_header = response
#        except :
#            tb = sys.exc_info()
#            print ("EXCEPTION: \n" + tb)
#            sys.exit()
#        else :
#            print("response_header: " + response_header.decode('utf8'))
