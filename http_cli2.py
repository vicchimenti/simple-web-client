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




import socket           # network sockets
import sys              # io and error handling




# set defaults
port = 80                           # default port is 80 web server standard
path = ""                           # declare path variable with empty string
double_slash = "//"                 # delimiter for parsing URLs
single_slash = "/"                  # delimiter for parsing URL paths
colon = ":"                         # delimiter for parsing port from URL
endOf_header = "\r\n\r\n"           # delimiter for parsing header and body
min_URL = 5                         # minimum length of an acceptable URL
match_all_IP = "0.0.0.0"            # for IP validity checking
content_length = "Content-Length:"  # delimiter to find buffer length
buffer_length = 0                   # default buffer length
buffer_length_str = ""




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
x = user_input.find (double_slash)

# if no http:// protocol was entered by the user
if x == -1 : full_URL = user_input

# if an http:// protocol was entered with the URL
else : protocol, full_URL = (user_input.split (double_slash , 2))

# validate full_URL
x = len(full_URL)
if x < 5 :
    print ("ERROR Invalid URL Format")
    sys.exit()





# parse full URL for domain, path and port number
x = full_URL.find (colon)

# if there is a colon in the user input
if x != -1 :
    # parse the host domain from the full URL
    host, portPathway = (full_URL.split (colon , 2))
    # search for a path after the port number
    y = portPathway.find (single_slash)

    # if there is a path after the port number
    if y != -1 :
        portstr = portPathway[:y]
        path = portPathway[y:]
        port = int (portstr)
        print ("Portstr if : " + portstr)
        print ("Path if : " + path)
    else :
        port = int (portPathway)

# if there is no colon in the user input, then use default port
else :
    # parse domain from path with new delimiter
    x = full_URL.find (single_slash)
    if x != -1 :
        host = full_URL[:x]
        path = full_URL[x:]
    else :
        host = full_URL
        path = single_slash

# confirm that the path contains any value after first slash
x = len(path)
if x <= 1 :
    path = single_slash




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
if host_ip_str == match_all_IP :
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


# prepare message for server
message = "GET "  + path \
                  + " HTTP/1.1\r\nConnection: close\r\nHost: " \
                  + host \
                  + endOf_header




# display GET Request
try :
    sys.stderr.write (message)
except :
    tb = sys.exc_info()
    print ("ERROR Standard Error Write : " + tb)



# ***** TODO Send buf len or delim first *****
# send message to the web server
try :
    sock.sendall (message.encode ('utf-8'))
    sock.shutdown(1)
except UnicodeError :
    print ("Error Encoding Message")
    sys.exit ("Exiting Program")
except OSError :
    print ("ERROR Sending Data")
    sys.exit ("Exiting Program")




# declare parsing variables and scrub for non-HTML/txt file type
full_response = "\n"
png = ".png"
jpg = ".jpg"
gif = ".gif"
pdf = ".pdf"

# encode the delimiter to binary
try :
    delim_in_bytes = endOf_header.encode ('utf-8')
except UnicodeError :
    print ("ERROR Encoding Delimiter")
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
            response = sock.recv (4096)
            full_response += response.decode ('utf-8')
            if  not response : break
            if buffer_length is None :
                x = full_response.find(colon)
                if x != -1 :
                    buffer_length_str, ignored, full_response = full_response.partition(colon)
                    buffer_length = int (buffer_length_str)
            if len(full_response) < buffer_length : break


    except UnicodeError :
        print ("ERROR Receiving Response")
        sys.exit ("Exiting Program")



    # split the response into a header and a body
    # *** TS TODO *** Search for Delimiter First before splitting
    response_header, response_body = (full_response.split(endOf_header, 2))
    # re-add delimiter to header
    response_header += endOf_header

else :

    # receive message back from server in byte stream
    try :
        while True :
            # image file type
            response = sock.recv (4096)
            byte_file.write (response)
            if  not response : break
    except OSError :
        print ("ERROR Receiving Response: ")
        sys.exit ("Exiting Program")

    # split the response into header and body
    with open ('tempFile.txt', 'rb') as f:
        data = f.read()
    byte_header, image_body = (data.split(delim_in_bytes, 2))

    # decode the header
    try :
        image_header = byte_header.decode ('utf-8')
    except OSError :
        print ("ERROR Decoding Image Header")
        sys.exit ("Exiting Program")

    # add delimiter to header
    image_header += endOf_header

# Close the Connection
sock.close()


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




# Close the program
sys.exit()
# eof




# declare variables for to parse header content
CONTENT_LENGTH = "Content-Length:"      # delimiter to find buffer length

# scan header for Content-Length
x = response_header.find(CONTENT_LENGTH)
# acquire receive size
if x != -1 :
    ignore, length_field = response_header.split(CONTENT_LENGTH, 2)
    length_value, ignore_new_line, ignore = length_field.partition(NEW_LINE)
    buffer_length = int(length_value)
else :
    print ("ERROR Incomplete HTTP Response Header")
    sys.exit("Exiting Program")




# receive the body
binary_body = bytearray()
try :
    while True :
        body_response = sock.recv (4096)
        binary_body += body_response
        bytes_received += len(body_response)
        if bytes_received >= buffer_length : break
        #if not response : break
except OSError :
    print ("ERROR Receiving Response: ")
    sys.exit ("Exiting Program")












# declare variables for to parse header content
CONTENT_TYPE = "Content-Type:"          # delimiter to find content type
CHARSET_FIELD = "charset="
TEXT = "text"
IMAGE = "image"
#EMPTY_MESSAGE = "empty"
message_type = ""       #EMPTY_MESSAGE
char_field = ""         #EMPTY_MESSAGE




# parse header for content type
x = response_header.find(CONTENT_TYPE)
if x != -1 :
    # parse response header for content type field
    ignore_field, ignore_type, message_type  = \
        response_header.partition(CONTENT_TYPE)
    # parse content type field for the type
    message_type, ignore_SEMI_COLON, char_field = \
        message_type.partition(SEMI_COLON)
    # parse the remainder for the charset field
    ignore_field, char_field, charset = \
        char_field.partition(CHARSET_FIELD)
    # parse the charset field for the value
    charset, ignore, ignore_field = \
        charset.partition(NEW_LINE)
else :
    print ("ERROR Parsing Header")
    sys.exit ("Exiting Program")

print ("charset : " + charset)
print ("message_type : " + message_type)









byte_file = open('tempFile.txt', 'wb')


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
