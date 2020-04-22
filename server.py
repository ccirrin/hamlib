import socket
import os
import threading
import init
def sendFile(sock,http,file):
    # Handle sending a file from downloads to a requester
    sock.sendall(http)
    f = open(file,"rb")
    http= f.read()
    sock.sendall(http)
    f.close()


def peerListening(sock):
    #Run Server Listening  
    while True:
        connection = None
        try:
            connection, address = sock.accept()
        except:
            break
        connection.settimeout(15)
        threading.Thread(target = handleConnection, args = [connection]).start()
    
def handleConnection(sock):
    data = sock.recv(2048) 
    data = str(data)
    space = 0
    file = None
    #Find location of file in request
    for x in data:
            if x == " ":
                space+=1
                if space == 2:
                    break
            if space:
                file=file + x
    if '\\' in file:
        file = file.replace('\\','')
    if '/' in file:
        file = file.replace('/','')
    if " " in file:
        file = file.replace(' ','')
    #file is requested from server
    if "GET" in data:
        http = "HTTP/1.1"
        # Check if we have a file
        if not os.path.exists(file):
                # if no file found send nothing found
                http += "404 Not Found\r\n\r\n"
                sock.sendall(bytes(http, encoding= 'utf8'))
        else:
            # if so call sendFile
            http = "200 OK\r\n" +"Content-Length: " + str(os.stat(file).st_size)+ " \r\n\r\n"
            http = bytes(http, encoding='utf8')
            sendFile(sock,http,file)
    sock.close()

