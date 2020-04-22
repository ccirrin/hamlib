import client
import os
import threading
import sys
import server
import fire
import socket

# Handle the grabing of initial metadata
    # Call check metadata
# call upload functions if there are files in upload folder
# Create a list of files in upload and download folder

files = []
ips = []
upfiles= []
stop = ""
def init():
    # Get ip address of host
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    # Prompt user for channel they would like to join
    user = fire.promptuser(ip)

    # Check what files current user has and inform firebase
    os.chdir("channel" + user.channel)
    for root, dirs, fil in os.walk(os.getcwd()):
        for f in fil:
            fire.addfile(user, f)
    
    # Spin off server thread
    t = threading.Thread(target = server.peerListening, args = [user])
    t.start()
    # Spin off client thread
    # cheeser

    print("Type 'q' to quit!")
    stop = input()
    while stop != "q":
        stop = input()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect( (user.ip, user.port))
    t.join()
    # Inform server that files will no longer be available
    for root, dirs, fil in os.walk(os.getcwd()):
        for f in fil:
            fire.discontinuefile(user, f)
           
if  __name__ == "__main__": 
    init()

