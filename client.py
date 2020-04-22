import init
import random
import socket
import os
import fire

# client.py - Client side functions, 
# -----------------------------------------------------------------------------
# Description: provide functions that requests files and check if there are
# new files added to channel directory

# Sync states between host and database
def checkfiles(user, directory, prevfiles):
    localfiles = []

    # Check files in channel directory and track new files
    for root, dirs, fil in os.walk(os.getcwd()):
        for f in fil:
            if f not in prevfiles:
                fire.addfile(user, f)
    
    # Get all files on server
    files = fire.getfiles(user)

    # Request all files that current host does not have
    for f in files:
        if f not in localfiles:
            ips = fire.getips(user, f)
            ip = ips[random.randint(0,len(ips) - 1)]
            ips.remove(ip)

            while requestFile(user, ip, f) != True and len(ip) != 0:
                # Let database know that we could not retrieve file from this ip
                fire.informdb(user, ip, f)

                # Choose another ip
                ip = ips[random.randint(0,len(ips) - 1)]
                ips.remove(ip)  

# Request a file, return true if request was successful, false if not
def requestFile(user, ip, file):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fd = open(file,"wb")

    try:
        sock.connect((ip, user.port))

        http="GET " + file + " HTTP/1.1\r\n\r\n"
        sock.sendall(bytes(http, encoding = "utf-8"))
        head = sock.recv(1024)
        head = str(head)
        
        #verify request       
        if "404" in head:
                sock.close()
                fd.close()
                print("Error 404: File "+ file +" not found. Trying different IP.")
                return False
        
        #find file length
        length = head[head.index("Content-Length"):]
        space = 0
        size = ""
        for x in length:
                if space:
                    size=size + x
                if x == " ":
                    space+=1
                    if space == 2:
                        break
        
        size = int(size)
        data = bytes()
        
        #receive messages until entire file arrives
        while size > 0:
            data += sock.recv(1024)
            size -= 1024
        
        fd.write(data)
        fd.close()
        sock.close()
        return True

    except:
        fd.close()
        sock.close()
        return False