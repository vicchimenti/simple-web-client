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




import socket           # network sockets
import sys              # io and error handling




# set defaults
port = 80
path = ""

# get user input from command line
try :
    user_input = sys.argv[1]
except sys.IndexError as e :
    print ("ERROR No Valid Command Line Input : " + e)
    sys.exit ("Exiting Program")
except sys.KeyError as e :
    print ("ERROR Invalid Command Line Entry : " + e)
    sys.exit ("Exiting Program")




# parse user_input to expose full URL
delim = "//"
x = user_input.find (delim)

# if no http:// protocol was entered by the user
if x == -1 : full_URL = user_input

# if an http:// protocol was entered with the URL
else : protocol, full_URL = (user_input.split (delim , 2))




# search for user provided port number
delim = ":"
x = full_URL.find (delim)

# if there is a colon in the user input
if x != -1 :
    # parse the host domain from the full URL
    host, portPathway = (full_URL.split (delim, 2))
    # now parse the port number from the path with a new delimiter
    delim = "/"
    y = portPathway.find (delim)

    # if there is a path after the port number
    if y != -1 :
        #portstr, path = (portPathway.split (delim, 2))
        portstr = portPathway[:y]
        path = portPathway[y:]
        port = int (portstr)
        print ("Portstr : " + portstr)
        #path = delim + path
        print ("Path if : " + path)
    else :
        port = int (portPathway)

# if there is no colon in the user input
else :
    # parse domain from path with new delimiter
    delim = "/"
    x = full_URL.find (delim)
    host = full_URL[:x]
    path = full_URL[x:]



# TS OUTPUT
print ("argument : " + sys.argv[1])
print ("user_input : " + user_input)
print ("portPathway : " + portPathway)
print ("full_url : " + full_URL)
print ("Path : " + path)
print ("Host : " + host)
pseudoPort = str(port)
print ("pseudoPort = " + pseudoPort)


host_ip = socket.gethostbyname(host)
host_ip_str = str(host_ip)
print ("host_ip_str : " + host_ip_str)


# Set up a TCP/IP socket
try :
    sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
except socket.OSError as e :
    print ("ERROR Creating Socket: " + e)
    sys.exit ("Exiting Program")


# Connect to the server as a client
#sock.setblocking(False)
try :
    sock.connect ((host, port))
except OSError :
    print ("ERROR Connecting")
    sys.exit ("Exiting Program")




# prepare message for server
message = "GET "  + path \
                  + " HTTP/1.1\r\nConnection: close\r\nHost: " \
                  + host \
                  + "\r\n\r\n"

# display GET Request
try :
    sys.stderr.write (message)
except :
    tb = sys.exc_info()
    print ("ERROR Standard Error Write : " + tb)




# send message to the web server
try :
    sock.sendall (message.encode ('utf-8'))
except sys.UnicodeError as e :
    print ("Error Encoding Message : " + e)
    sys.exit ("Exiting Program")
except socket.OSError as e :
    print ("ERROR Sending Data : " + e)
    sys.exit ("Exiting Program")





# declare parsing variables and scrub for non-HTML/txt file type
full_response = "\n"
delim = "\r\n\r\n"
png = '.png'
jpg = '.jpg'
gif = '.gif'
pdf = '.pdf'

# encode the delimiter to binary
try :
    delim_in_bytes = delim.encode ('utf-8')
except sys.UnicodeError as e :
    print ("ERROR Encoding Delimiter : " + e)
    sys.exit ("Exiting Program")

# open file for input
byte_file = open ('tempFile.txt', 'wb')

# scan path for file type
x = path.find (png)
xy = path.find (jpg)
xyz = path.find (gif)
xyzz = path.find (pdf)




# receive response from server and check for file type
if x == -1 and xy == -1 and  xyz == -1 and xyzz == -1 :

    # receive message from server and decode from bytes
    try :
        while True :
            # not an image file type
            response = sock.recv (65536)
            full_response += response.decode ('utf-8')
            if  not response : break
    except sys.UnicodeError as e :
        print ("ERROR Decoding Response : " + e)
        sys.exit ("Exiting Program")
    except socket.OSError as e :
        print ("ERROR Receiving Response: " + e)
        sys.exit ("Exiting Program")

    # split the response into a header and a body
    response_header, response_body = (full_response.split(delim, 2))
    # re-add delimiter to header
    response_header += delim

else :

    # receive message back from server in byte stream
    try :
        while True :
            # image file type
            response = sock.recv (65536)
            byte_file.write (response)
            if  not response : break
    except socket.OSError as e :
        print ("ERROR Receiving Response: " + e)
        sys.exit ("Exiting Program")

    # split the response into header and body
    with open ('tempFile.txt', 'rb') as f:
        data = f.read()
    byte_header, image_body = (data.split(delim_in_bytes, 2))

    # decode the header
    try :
        image_header = byte_header.decode ('utf-8')
    except sys.UnicodeError as e :
        print ("ERROR Decoding Image Header : " + e)
        sys.exit ("Exiting Program")

    # add delimiter to header
    image_header += delim




# process response, store data in variables and display results
if x == -1 and xy == -1 and  xyz == -1 and xyzz == -1 :

    # if not an image file
    try :
        sys.stderr.write (response_header)
    except sys.Exception as tb :
        tb = sys.exc_info()
        print ("ERROR Writing Response Header : " + tb)
        sys.exit ("Exiting Program")

    # print message body
    try :
        sys.stdout.write (response_body)
    except sys.Exception as tb :
        tb = sys.exc_info()
        print ("ERROR Writing Response Body : " + tb)
        sys.exit ("Exiting Program")

else :

    # if image file
    try :
        sys.stderr.write (image_header)
    except sys.Exception as tb :
        tb = sys.exc_info()
        print ("ERROR Writing Image Response Header: " + tb)
        sys.exit ("Exiting Program")

    # print message body
    try :
        sys.stdout.buffer.write (image_body)
    except sys.Exception as tb :
        tb = sys.exc_info()
        print ("ERROR Writing Image Response Body : " + tb)
        sys.exit ("Exiting Program")




# Close the connection
sock.close()
sys.exit()
# eof
