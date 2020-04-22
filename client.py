import init
import random
import socket
import os
import fire
import time

# client.py - Client side functions, 
# -----------------------------------------------------------------------------
# Description: provide functions that requests files and check if there are
# new files added to channel directory

# Repeatedly check files to sync states
def filechecker(user, directory):
    while True:
        print("checking files")
        checkfiles(user, directory)
        time.sleep(60)

# Sync states between host and database
def checkfiles(user, directory):
    localfiles = []

    # Check files in channel directory and track new files
    for root, dirs, fil in os.walk(directory):
        for f in fil:
            localfiles.append(f)
            fire.addfile(user, f)
    
    # Get all files on server
    files = fire.getfiles(user)
    print(files)

    # Request all files that current host does not have
    for f in files:
        if f not in localfiles:
            ips = fire.getips(user, f)
            if (len(ips) == 0):
                continue
            
            if (user.ip in ips):
                ips.remove(user.ip)
                if (len(ips) == 0):
                    continue

            ip = ips[random.randint(0,len(ips) - 1)]
            ips.remove(ip)
            
            success = requestFile(user, ip, f)
            while success != True and len(ips) != 0:
                # print("yeet: " + f)
                # Let database know that we could not retrieve file from this ip
                fire.informdb(user, ip, f)

                # Choose another ip
                ip = ips[random.randint(0,len(ips) - 1)]
                ips.remove(ip)

                # Try requesting from another IP
                success = requestFile(user, ip, f)
            
            if success:
                localfiles.append(f)
                fire.addfile(user, f)

# Request a file, return true if request was successful, false if not
def requestFile(user, ip, file):
    print("requesting file: " + file + " from ip: " + ip)

    # create client socket that handles requesting files from other peers
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

    try:
        sock.connect((ip, user.port))

        http="GET " + file + " HTTP/1.1\r\n\r\n"
        sock.sendall(bytes(http, encoding = "utf-8"))
        head = sock.recv(1024)
        head = str(head)
        
        #verify request       
        if "404" in head:
                sock.close()
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
        
        fd = open(file,"wb")
        fd.write(data)
        fd.close()
        sock.close()
        print("wrote file")
        return True
    except:
        print("exception")
        sock.close()
        return False