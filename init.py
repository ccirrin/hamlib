import client
import os
import threading
import sys
import server
import fire
import socket
from requests import get

# init.py - Run the main function 
# -----------------------------------------------------------------------------
# Description: Initialize program, prompt user for info, and start client
# and server threads. Cleanup at end of execution as well.

def main():
    user = None
    try:
        # Get ip address of host
        ip = get('https://api.ipify.org').text

        # Prompt user for channel they would like to join
        user = fire.promptuser(ip)

        chandir = "channels"
        try:
            # Change directory to channels directory
            os.chdir(chandir)
        except:
            # Make directory
            os.mkdir(chandir)
            os.chdir(chandir)

        chandir = user.channel
        try:
            # Change directory to specific channel directory
            os.chdir(chandir)
        except:
            # Make directory
            os.mkdir(chandir)
            os.chdir(chandir)
        
        # Create a socket that handles listening for connections from other peers
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("",user.port))
        print("Server is running on port:", user.port)
        sock.listen(5)
        
        # Spin off server thread
        t = threading.Thread(target = server.peerListening, args = [sock], daemon=True)
        t.start()

        # Spin off client thread
        ct = threading.Thread(target = client.filechecker, args = [user], daemon=True)
        ct.start()

        # Wait for client to press 'q' to quit the program
        print("Type 'q' to quit, or switch channels by typing in the channel number!")
        a = input()
        while a != "q":
            a = input()
            if a != "q":
                for root, dirs, fil in os.walk(os.getcwd()):
                    for f in fil:
                        fire.discontinuefile(user, f)
                user = fire.switchChannel(user,a)
                ct._stop
                ct = threading.Thread(target = client.filechecker, args = [user], daemon=True)
                ct.start()
                print("Switched to channel: ",a)
    except Exception as e:
        print(e)
    finally:
        if (user != None):
            # Inform server that files will no longer be available
            for root, dirs, fil in os.walk(os.getcwd()):
                for f in fil:
                    fire.discontinuefile(user, f)
            
            # Close server socket
            sock.close()

        print("Thank you for using Hamlib!")
           
if  __name__ == "__main__": 
    main()

