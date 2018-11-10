# Vic Chimenti
# CPSC 5510 FQ18
# http_cli.py
# v2.0
# Created           10/19/2018
# Last Modified     11/9/2018
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
NEW_LINE = "\r\n"                       # delimiter for new line return
END_HEADER = "\r\n\r\n"                 # delimiter for parsing header and body
END_RESPONSE = "\r\n\t\r\n\t"           # custom delimiter for checking http_svr
MATCH_ALL = "0.0.0.0"                   # for IP validity checking




# get user input from command line
try :
    user_input = sys.argv[1]
except IndexError :
    sys.stderr.write ("ERROR No Valid Command Line Input : ")
    sys.exit ("Exiting Program")
except KeyError :
    sys.stderr.write ("ERROR Invalid Charcter Entered : ")
    sys.exit ("Exiting Program")
except Exception :
    sys.stderr.write ("ERROR Invalid Command Line Entry : ")
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
    sys.stderr.write ("ERROR Invalid URL Format : ")
    sys.exit("Exiting Program")




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




# validate URL entered and assign host IP number
try :
    host_ip = socket.gethostbyname(host)
except socket.gaierror:
    sys.stderr.write ("ERROR Invalid URL Entered : ")
    sys.exit ("Exiting Program")

# convert host IP number to integer
host_ip_str = str(host_ip)
if host_ip_str == MATCH_ALL :
        sys.stderr.write ("ERROR Invalid IP Number : ")
        sys.exit ("Exiting Program")




# Set up a TCP/IP socket
try :
    sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
except OSError :
    sys.stderr.write ("ERROR Creating Socket : ")
    sys.exit ("Exiting Program")

# Connect to the server as a client
sock.settimeout(10)
try :
    sock.connect ((host, port))
except OSError :
    sys.stderr.write ("ERROR Connecting : ")
    sys.exit ("Exiting Program")




# prepare message for server with delimiter included
message = "GET "  + path \
                  + " HTTP/1.1\r\nConnection: close\r\nHost: " \
                  + host \
                  + END_HEADER

# display GET Request
try :
    sys.stderr.write (message)
except Exception :
    sys.stderr.write ("ERROR Standard Error Write : ")
    sys.exit("Exiting Program")




# send message to the web server
try :
    sock.sendall (message.encode (charset))
    sock.shutdown(1)
except UnicodeError :
    sys.stderr.write ("Error Encoding Message : ")
    sys.exit ("Exiting Program")
except OSError :
    sys.stderr.write ("ERROR Sending Data : ")
    sys.exit ("Exiting Program")




# encode the Response delimiter to binary
try :
    response_delim_in_bytes = END_RESPONSE.encode (charset)
except UnicodeError :
    sys.stderr.write ("ERROR Encoding Delimiter : ")
    sys.exit ("Exiting Program")




# encode the Header delimiter to binary
try :
    header_delim_in_bytes = END_HEADER.encode (charset)
except UnicodeError :
    sys.stderr.write ("ERROR Encoding Delimiter : ")
    sys.exit ("Exiting Program")




# receive message back from server in byte stream
binary_message = bytearray()
# receive header first
try :
    while True :
        response = sock.recv (65536)
        binary_message += response
        if not response : break
except OSError :
    sys.stderr.write ("ERROR Receiving Response : ")
    sys.exit ("Exiting Program")

# Close the Socket
sock.close()



# ********** TODO : Evaluate this Split, it may be causing an issue ********
# split the data into header and body
binary_body = bytearray()
binary_header = bytearray()
binary_header, binary_body = binary_message.split(header_delim_in_bytes, 2)




# decode the header
try :
    response_header = binary_header.decode (charset)
except OSError :
    sys.stderr.write ("ERROR Decoding Image Header : ")
    sys.exit ("Exiting Program")
# add delimiter
response_header += END_HEADER



# print the Header
try :
    sys.stderr.write (response_header)
except Exception :
    sys.stderr.write ("ERROR Writing Response Header : ")
    sys.exit ("Exiting Program")




# declare variables for to parse header content
CONTENT_TYPE = "Content-Type:"          # delimiter to find content type
CHARSET_FIELD = "charset="
TEXT = "text"
IMAGE = "image"
message_type = ""
char_field = ""




# check for status code
STATUS_CODE = "200 OK"
sc = response_header.find(STATUS_CODE)

# if the status code is 200 OK
if sc != -1 :

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
        sys.stderr.write ("ERROR Parsing Header : ")
        sys.exit ("Exiting Program")


    # determine content type and print the message body
    y = message_type.find(TEXT)
    z = message_type.find(IMAGE)
    if y != -1 :
        # print text/html message body
        try :
            response_body = binary_body.decode(charset)
            sys.stdout.write (response_body)
            sys.stderr.write ("")
        except Exception :
            sys.stderr.write ("ERROR Writing Text Response Body : ")
            sys.exit ("Exiting Program")

    elif z != -1 :
        # print image message body
        try :
            sys.stdout.buffer.write (binary_body)
            sys.stderr.write ("")
        except Exception :
            sys.stderr.write ("ERROR Writing Image Response Body : ")
            sys.exit ("Exiting Program")

    else :
        sys.stderr.write ("ERROR Invalid Content-Type : ")
        sys.exit ("Exiting Program")


# or else the Status Code is not 200 OK
else :
    try :
        response_body = binary_body.decode(charset)
        sys.stdout.write (response_body)
    except Exception :
        sys.stderr.write ("ERROR Writing Response Body : Status Code not 200 OK : ")
        sys.exit ("Exiting Program")




# Close the program
sys.exit()
# eof
