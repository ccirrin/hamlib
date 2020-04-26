import socket
import os
import threading
import init
import safesocket

# server.py - Server side functions
# -----------------------------------------------------------------------------
# Description: Provide functions that handle incoming GET requests, send the
# file to the host that requested it.

def sendFile(sock, http, file, cwd):
    # Handle sending a file from downloads to a requester
    safesocket.safesend(sock, http)
    f = open(os.path.join(cwd, file), "rb")
    http = f.read()
    safesocket.safesend(sock, http)
    f.close()


def peerListening(sock, cwd):
    # Run Server Listening  
    while True:
        connection = None
        try:
            connection, address = sock.accept()
        except:
            break
        connection.settimeout(15)
        threading.Thread(target = handleConnection, args = [connection, cwd]).start()
    
def handleConnection(sock, cwd):
    data = sock.recv(2048) 
    data = str(data)
    space = 0
    file = ""

    # Find location of file in request
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
    # File is requested from server
    if "GET" in data:
        http = "HTTP/1.1"
        # Check if we have a file
        if not os.path.exists(os.path.join(cwd, file)):
                # If no file found send nothing found
                print("\t-File does not exist: " + file)
                http += "404 Not Found\r\n\r\n"
                safesocket.safesend(sock, http.encode())
        else:
            # If so call sendFile
            print("\t-Sending file: " + file)
            http = "200 OK\r\n" +"Content-Length: " + str(os.stat(os.path.join(cwd, file)).st_size)+ " \r\n\r\n"
            http = bytes(http, encoding='utf8')
            sendFile(sock, http, file, cwd)
    sock.close()