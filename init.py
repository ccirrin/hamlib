import client
import os
import threading
import sys
import server
import fire
import socket
import re
from requests import get

# init.py - Run the main function 
# -----------------------------------------------------------------------------
# Description: Initialize program, prompt user for info, and start client
# and server threads. Cleanup at end of execution as well.

def cleanup(user, cwd):
    if (user != None):
            # Inform server that files will no longer be available
            for root, dirs, fil in os.walk(cwd):
                for f in fil:
                    fire.discontinuefile(user, f)

def joinchannel(ip):
    user = None
    try:
        # Prompt user for port and channel they would like to join
        user = fire.promptuser(ip)

        print("Joining channel:", user.channel)
        print("Type '^C' to leave channel or '^C' to leave program")

        # Create a socket that handles listening for connections from other peers
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("",user.port))
        print("Server is running on port:", user.port)
        sock.listen(5)

        # Make channel directory if it does not exist
        chandir = "channels/" + str(user.channel)
        if (not os.path.isdir(chandir)):
            os.makedirs(chandir)

        # Spin off server thread
        t = threading.Thread(target = server.peerListening, args = [sock, chandir], daemon=True)
        t.start()

        # Spin off client thread
        ct = threading.Thread(target = client.filechecker, args = [user, chandir], daemon=True)
        ct.start()

        print("Type '^C' to leave program or hit enter to join another channel")
        input()
        
        # Stop the threads
        ct._stop
        t._stop
    except KeyboardInterrupt:
        # Cleanup current channel and exit
        cleanup(user, chandir)
        sock.close()
        print("Thank you for using Hamlib!")
        sys.exit()
    except Exception as e:
        print(e)
    finally:
        # Cleanup current channel
        cleanup(user, chandir)
        sock.close()

def main():
    print("Welcome to Hamlib!")
    
    # Get ip address of host
    ip = get('https://api.ipify.org').text

    while True:
        joinchannel(ip)
           
if  __name__ == "__main__": 
    main()

