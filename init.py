import client
import os
import threading
import sys
import server
import fire
import socket
from requests import get
# Handle the grabing of initial metadata
    # Call check metadata
# call upload functions if there are files in upload folder
# Create a list of files in upload and download folder

stop = False

def init():
    # Get ip address of host

    ip = get('https://api.ipify.org').text

    # Prompt user for channel they would like to join
    user = fire.promptuser(ip)

    # Check what files current user has and inform firebase
    os.chdir("channel" + user.channel)
    directory = os.getcwd()
    for root, dirs, fil in os.walk(directory):
        for f in fil:
            fire.addfile(user, f)
    
    # create a socket that handles listening for connections from other peers
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("",user.port))
    print("Server is running on port:", user.port)
    sock.listen(5)
    
    # Spin off server thread
    t = threading.Thread(target = server.peerListening, args = [sock], daemon=True)
    t.start()

    # Spin off client thread
    ct = threading.Thread(target = client.filechecker, args = [user, directory], daemon=True)
    ct.start()

    print("Type 'q' to quit!")
    a = input()
    while a != "q":
        a = input()

    stop = True
    # Inform server that files will no longer be available
    for root, dirs, fil in os.walk(os.getcwd()):
        for f in fil:
            fire.discontinuefile(user, f)

    sock.close()
           
if  __name__ == "__main__": 
    init()

