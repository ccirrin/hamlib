import init
import random
import socket
def checkMetadata():
    # get the metadata from firebase and check if there are any new files
    #fmeta = firebase()
    # for line in fmeta:
    #     if "Files:" in line:
    #         break
    for line in fmetadata:
        if "IPs:" in line:
            continue
        init.ips.append(line.rstrip("\n"))
        if "Files:" in line:
            break
    for line in fmetadata:
        templine = line.rstrip("\n")
        # if file match do nothing
        if templine in init.files:
            continue
        # if a file is not found call requestFile from a random user in IP list
        else:
            requestFile(templine)
            init.files.append(templine)
    
    



def requestFile(file):
    # choose a random peer thats online and try to download a file from them
    ip = init.ips[random.randint(0,len(init.ips)+1)]
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(ip)
    http="GET " + file + " HTTP/1.1\r\n\r\n"
    sock.sendall(bytes(http, encoding = "utf-8"))
    head = sock.recv(1024)
    head = str(head)
    #verify request       
    while "404" in head:
            sock.close()
            print("Error 404: File "+ file+" not found. Trying different IP.")
            ip = init.ips[random.randint(0,len(init.ips)+1)]
            sock.connect(ip)
            sock.sendall(bytes(http, encoding = "utf-8"))
            head = sock.recv(1024)
            head = str(head)
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
    size= int(size)
    data =bytes()
    #receive messages until entire file arrives
    while size > 0:
        data += sock.recv(1024)
        size -= 1024
    fd = open(file,"wb")
    fd.write(data)
    fd.close()
    return