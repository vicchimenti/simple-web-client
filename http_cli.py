# Vic Chimenti
# CPSC 5510 FQ18
# http_cli.py
# v2.0
# v2 includes updates for web server assignment
# primary changes include better error handling
# Created           10/19/2018
# Last Modified     11/3/2018
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
try :
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e :
    print "ERROR Creating Socket: %s" % e
    sys.exit(1)


# Connect to the server as a client
sock.settimeout(5)
try :
    sock.connect((host, port))
except socket.gaierror, e :
    print "ERROR: Invalid Address : %s" % e
    sys.exit(1)
except socket.error, e :
    print "ERROR Connecting : %s" % e
    sys.exit(1)




# prepare message for server
message = "GET "  + path \
                  + " HTTP/1.1\r\nConnection: close\r\nHost: " \
                  + host \
                  + "\r\n\r\n"

# display GET Request
try :
    sys.stderr.write(message)
except :
    tb = sys.exc_info()
    print ("EXCEPTION: \n" + tb)




# send message to the web server
try :
    sock.sendall(message.encode('utf-8'))
except socket.error, e :
    print "ERROR Sending Data : %s" % e
    sys.exit(1)




# declare parsing variables and scrub for non-HTML/txt file type
full_response = "\n"
delim = "\r\n\r\n"
delim_in_bytes = delim.encode('utf-8')
byte_file = open('tempFile.txt', 'wb')
png = '.png'
jpg = '.jpg'
gif = '.gif'
pdf = '.pdf'
x = path.find(png)
xy = path.find(jpg)
xyz = path.find(gif)
xyzz = path.find(pdf)




# receive response from server/ check for file type
if x == -1 and xy == -1 and  xyz == -1 and xyzz == -1 :

    # receive message from server and decode from bytes
    while True :
        # not an image file type
        response = sock.recv(65536)
        full_response += response.decode('utf-8')
        if  not response : break

    # split the response into a header and a body
    response_header, response_body = (full_response.split(delim, 2))
    # re-add delimiter to header
    response_header += delim

else :

    # receive message back from server in byte stream
    while True :
        # image file type
        response = sock.recv(65536)
        byte_file.write(response)
        if  not response : break

    # split the response into header and body
    with open('tempFile.txt', 'rb') as f:
        data = f.read()
    byte_header, image_body = (data.split(delim_in_bytes, 2))
    # decode the header
    image_header = byte_header.decode('utf-8')
    image_header += delim



# process response, store data in variables and display results
if x == -1 and xy == -1 and  xyz == -1 and xyzz == -1 :

    # if not an image file
    try :
        sys.stderr.write(response_header)
    except :
        tb = sys.exc_info()
        print ("EXCEPTION: \n" + tb)

    # print message body
    sys.stdout.write(response_body)

else :

    # if image file
    try :
        sys.stderr.write(image_header)
    except :
        tb = sys.exc_info()
        print ("EXCEPTION: \n" + tb)

    # print message body
    sys.stdout.buffer.write(image_body)




# Close the connection
sock.close()
sys.exit()
# eof
