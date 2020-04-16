import socket
import os

def sendFile(file,sock):
    # Handle sending a file from downloads to a requester
    http = "HTTP/1.1 200 OK\r\n" +"Content-Length: " + str(os.stat(file).st_size)+ " \r\n\r\n"
    http = bytes(http, encoding='utf8')
    sock.sendall(http)
    f = open(file,"rb")
    http= f.read()
    sock.sendall(http)
    f.close()


# listen()
    # create a socket that handles listening for connections from other peers
    # if a peer asks for a file 
        # Check if we have a file
            # if so call sendFile
        # if no file found
            # send nothing found