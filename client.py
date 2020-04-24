import init
import random
import socket
import os
import fire
import time
import safesocket

# client.py - Client side functions 
# -----------------------------------------------------------------------------
# Description: Provide functions that requests files and check if there are
# new files added to channel directory.

# Repeatedly check files to sync states
def filechecker(user):
    while True:
        print("\t-Checking files")
        checkfiles(user)
        time.sleep(30)

# Sync states between host and database
def checkfiles(user):
    localfiles = []

    # Check files in channel directory and track new files
    for root, dirs, fil in os.walk(os.getcwd()):
        for f in fil:
            localfiles.append(f)
            fire.addfile(user, f)
    
    # Get all files on server
    files = fire.getfiles(user)

    # Request all files that current host does not have
    for f in files:
        if f not in localfiles:
            # Get all ips from server that have file 'f'
            ips = fire.getips(user, f)
            
            # Remove current host ip from list if it is somehow in there
            while ((user.ip, user.port) in ips):
                ips.remove((user.ip, user.port))
            
            # Try to request file from random peer until we get it
            while True:

                # If no one on server has file, don't bother requesting
                if (len(ips) == 0):
                    break

                # Choose another ip
                ip = ips[random.randint(0,len(ips) - 1)]
                ips.remove(ip)
                
                # Try requesting from another IP
                if (requestFile(user, ip, f)):
                    # If we now have the file, let the database know
                    localfiles.append(f)
                    fire.addfile(user, f)
                    break

                # Let database know that we could not retrieve file from this ip
                fire.informdb(user, ip, f)

# Request a file, return true if request was successful, false if not
def requestFile(user, ip, file):
    assert(len(ip) == 2)
    print("\t-Requesting file: " + file + " from ip: " + ip[0])

    # Create client socket that handles requesting files from other peers
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

    try:
        sock.connect((ip[0], ip[1]))

        http="GET " + file + " HTTP/1.1\r\n\r\n"
        safesocket.safesend(sock, http.encode())
        head = sock.recv(1024)
        head = str(head)
        
        # Verify request       
        if "404" in head:
                sock.close()
                print("\t-Did not receive file: " + file + " from ip: " + ip[0])
                return False
        
        # Find file length
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
        data = safesocket.safercv(sock, size)
        
        fd = open(file,"wb")
        fd.write(data)
        fd.close()
        sock.close()
        print("\t-Received file: " + file + " from ip: " + ip[0])
        return True
    except:
        sock.close()
        print("\t-Did not receive file: " + file + " from ip: " + ip[0])
        return False