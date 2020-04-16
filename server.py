import socket
import os
import threading
def sendFile(sock,http,file):
    # Handle sending a file from downloads to a requester
    sock.sendall(http)
    f = open(file,"rb")
    http= f.read()
    sock.sendall(http)
    f.close()


def peerListening(port):
    # create a socket that handles listening for connections from other peers
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("",port))
    print("Server is running on port:", port)
    sock.listen(5)
    while True:
        connection, address = sock.accept()
        connection.settimeout(15)
        threading.Thread(target = handleConnection, args = (connection).start())
    
def handleConnection(sock):
    os.chdir("Downloads")
    data = sock.recv(2048) 
    data = str(data)
    for x in data:
            if x == " ":
                space+=1
                if space == 2:
                    break
            if space:
                file=file + x
    http = "HTTP/1.1"
    if '\\' in file:
        file = file.replace('\\','')
    if '/' in file:
        file = file.replace('/','')
    if " " in file:
        file = file.replace(' ','')
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

