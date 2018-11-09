# Vic Chimenti
# CPSC 5510 FQ18
# http_cli.py
# v2.0
# Created           10/19/2018
# Last Modified     11/8/2018
# Simple Web Client in Python3
# /usr/local/python3/bin/python3




# v2 includes updates for web server assignment
# primary changes include better error handling
# fixed command line parameters feedback
# fixed URL handling feedback
# fixed HTTP Request feedback
# fixed image parsing algorithm




import socket           # network sockets
import sys              # io and error handling




# set defaults
port = 80                               # default port is 80 web server standard
path = ""                               # declare path with empty string
min_URL = 5                             # minimum length of an acceptable URL
buffer_length = 0                       # default buffer length
charset = "UTF-8"                       # default encoding protocol




# set constants
DOUBLE_SLASH = "//"                     # delimiter for parsing URLs
SINGLE_SLASH = "/"                      # delimiter for parsing URL paths
COLON = ":"                             # delimiter for parsing port from URL
SEMI_COLON = ";"                        # delimiter for parsing data from header
END_HEADER = "\r\n\r\n"                 # delimiter for parsing header and body
MATCH_ALL = "0.0.0.0"                   # for IP validity checking
CONTENT_TYPE = "Content-Type:"          # delimiter to find content type
CONTENT_LENGTH = "Content-Length:"      # delimiter to find buffer length







# get user input from command line
try :
    user_input = sys.argv[1]
except IndexError :
    print ("ERROR No Valid Command Line Input")
    sys.exit ("Exiting Program")
except KeyError :
    print ("ERROR Invalid Charcter Entered")
    sys.exit ("Exiting Program")
except Exception :
    print ("ERROR Invalid Command Line Entry")
    sys.exit ("Exiting Program")




# parse user_input to expose full URL
x = user_input.find (DOUBLE_SLASH)

# if no http:// protocol was entered by the user
if x == -1 : full_URL = user_input

# if an http:// protocol was entered with the URL
else : protocol, full_URL = (user_input.split (DOUBLE_SLASH , 2))

# validate full_URL
x = len(full_URL)
if x < 5 :
    print ("ERROR Invalid URL Format")
    sys.exit()





# parse full URL for domain, path and port number
x = full_URL.find (COLON)

# if there is a COLON in the user input
if x != -1 :
    # parse the host domain from the full URL
    host, portPathway = (full_URL.split (COLON , 2))
    # search for a path after the port number
    y = portPathway.find (SINGLE_SLASH)

    # if there is a path after the port number
    if y != -1 :
        portstr = portPathway[:y]
        path = portPathway[y:]
        port = int (portstr)
        print ("Portstr if : " + portstr)
        print ("Path if : " + path)
    else :
        port = int (portPathway)

# if there is no COLON in the user input, then use default port
else :
    # parse domain from path with new delimiter
    x = full_URL.find (SINGLE_SLASH)
    if x != -1 :
        host = full_URL[:x]
        path = full_URL[x:]
    else :
        host = full_URL
        path = SINGLE_SLASH

# confirm that the path contains any value after first slash
x = len(path)
if x <= 1 :
    path = SINGLE_SLASH




# ***** TS OUTPUT ********
print ("argument : " + sys.argv[1])
print ("user_input : " + user_input)
#print ("portPathway : " + portPathway)
print ("full_url : " + full_URL)
print ("Path : " + path)
print ("Host : " + host)
pseudoPort = str(port)
print ("pseudoPort = " + pseudoPort)




# validate URL entered and assign host IP number
try :
    host_ip = socket.gethostbyname(host)
except socket.gaierror:
    print ("ERROR Invalid URL Entered")
    sys.exit ("Exiting Program")

# convert host IP number to integer
host_ip_str = str(host_ip)
if host_ip_str == MATCH_ALL :
        print ("ERROR Invalid IP Number")
        sys.exit ("Exiting Program")

print ("host_ip_str : " + host_ip_str)




# Set up a TCP/IP socket
try :
    sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
except OSError :
    print ("ERROR Creating Socket")
    sys.exit ("Exiting Program")

# Connect to the server as a client
sock.settimeout(5)
try :
    sock.connect ((host, port))
except OSError :
    print ("ERROR Connecting")
    sys.exit ("Exiting Program")


# prepare message for server with delimiter included
message = "GET "  + path \
                  + " HTTP/1.1\r\nConnection: close\r\nHost: " \
                  + host \
                  + END_HEADER




# display GET Request
try :
    sys.stderr.write (message)
except :
    tb = sys.exc_info()
    print ("ERROR Standard Error Write : " + tb)




# send message to the web server
try :
    sock.sendall (message.encode (charset))
    sock.shutdown(1)
except UnicodeError :
    print ("Error Encoding Message")
    sys.exit ("Exiting Program")
except OSError :
    print ("ERROR Sending Data")
    sys.exit ("Exiting Program")




# encode the delimiter to binary
try :
    delim_in_bytes = END_HEADER.encode (charset)
except UnicodeError :
    print ("ERROR Encoding Delimiter")
    sys.exit ("Exiting Program")




# receive message back from server in byte stream
binary_message = bytearray()
try :
    while True :
        response = sock.recv (4096)
        binary_message += response
        if  not response : break
except OSError :
    print ("ERROR Receiving Response: ")
    sys.exit ("Exiting Program")

# split the response into header and body
binary_header, binary_body = (binary_message.split(delim_in_bytes, 2))

# decode the header
try :
    response_header = binary_header.decode (charset)
except OSError :
    print ("ERROR Decoding Image Header")
    sys.exit ("Exiting Program")

# add delimiter to header
response_header += END_HEADER

# Close the Socket
sock.close()




# parse header for content type
empty_message = "empty"
message_type = empty_message
TEXT = "text"
IMAGE = "image"
x = response_header.find(CONTENT_TYPE)
if x != -1 :
    ignore_field, ignore_type, message_type  = \
        response_header.partition(CONTENT_TYPE)
    message_type, ignore_SEMI_COLON, ignore_field = \
        message_type.partition(SEMI_COLON)




# process response, store data in variables and display results
if message_type != empty_message :
    x = message_type.find(TEXT)

    if x != -1 :
        # if page content in text/html
        try :
            sys.stderr.write (response_header)
        except sys.Exception as tb :
            tb = sys.exc_info()
            print ("ERROR Writing Response Header : " + tb)
            sys.exit ("Exiting Program")

        # print message body
        try :
            response_body = binary_body.decode(charset)
            sys.stdout.write (response_body)
        except sys.Exception as tb :
            tb = sys.exc_info()
            print ("ERROR Writing Response Body : " + tb)
            sys.exit ("Exiting Program")


    # confirm that non-text is an image type
    x = message_type.find(IMAGE)
    if x != -1 :

        # if image file
        try :
            sys.stderr.write (response_header)
        except sys.Exception as tb :
            tb = sys.exc_info()
            print ("ERROR Writing Image Response Header: " + tb)
            sys.exit ("Exiting Program")

        # print message body
        try :
            sys.stdout.buffer.write (binary_body)
        except sys.Exception as tb :
            tb = sys.exc_info()
            print ("ERROR Writing Image Response Body : " + tb)
            sys.exit ("Exiting Program")

else :
    # if empty response body
    try :
        sys.stderr.write (response_header)
    except sys.Exception as tb :
        tb = sys.exc_info()
        print ("ERROR Writing Response Header : " + tb)
        sys.exit ("Exiting Program")




# Close the program
sys.exit()
# eof
