import socket

# safesocket.py - Functions for safe send and receive
# -----------------------------------------------------------------------------
# Description: Functions to safely send all data and receive all data while
# utilizing sockets.

# function for sending safely (this is a basic function based off Python Socket documentation)
def safesend(cs, fb):
    # the while loop is to ensure that all of the file is sent
    # since cs.send() might not send everything if network is busy
    size = len(fb)
    sent = 0
    while sent < size:
        # try to send everything we have not sent yet
        s = cs.send(fb[sent:])
        if s <= 0:
            # socket connection interrupted
            raise RuntimeError("socket connection broken")
        
        # update the amount we have sent, to make sure it equals 'size'
        sent = sent + s
    return

# function for receiving safely (this is a basic function based off Python Socket documentation)
def safercv(cs, size):
    # the while loop is to ensure that all of the file is received
    # since cs.rcv() might not send everything if the network buffers are empty
    chunks = []
    rcvd = 0
    while rcvd < size:
        r = cs.recv(min(size - rcvd, 2048))
        if r == b'':
            # socket connection interrupted
            raise RuntimeError("socket connection broken")

        # update the total chunks we have received
        chunks.append(r)

        # update the number of bytes that we have received
        rcvd = rcvd + len(r)
    
    # return all the bytes we received
    return b''.join(chunks)