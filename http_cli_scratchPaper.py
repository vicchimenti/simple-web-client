





    print(image_header)

    print ("\n byte_header \n")
    print (byte_header)

    print(response_body)
    print(response_header)

        print ("byte_body \n")
        print (byte_body)



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




sys.exit()
#sys.exit()
# sys.exit()
# print("x != -1: " + str(x) + str(xy) + str(xyz) + str(xyzz))
# wait for entire response

    # decode byte file and save as string
    print ("if :")
    with open('tempFile.txt', 'rt') as f : full_response = f.read()
    # seperate the header from the body
    x = full_response.find(delim)
    response_header = full_response[:x]
    response_body = full_response[x:]
    #response_header, response_body = (full_response.split(delim))
    response_header += delim
    print(response_body)
    #print(response_header)


# receive message back from server in byte stream
byte_file = open('tempFile.txt', 'wb')
while True :
    # max receive size is 2^16
    response = sock.recv(65536)
    byte_file.write(response)
    if  not response : break
