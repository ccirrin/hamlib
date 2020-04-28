from firebase import Firebase
import client
import ipaddress
import re
import os
import threading
import secret

# fire.py - Interface for firebase
# -----------------------------------------------------------------------------
# Description: Provide functions that interface with firebase database in order
# to keep track of files and ips.

firebase = Firebase(secret.firebaseConfig)
auth = firebase.auth()
db = firebase.database()

class User:
    def __init__(self, port, ip, numip, channel, key):
        self.port = port
        self.ip = ip
        self.numip = numip
        self.channel = channel
        self.key = key

# Prompt user for channel
def promptuser(ip):
    assert(isinstance(ip, str))

    numip = str(int(ipaddress.IPv4Address(ip)))

    print("What channel would you like to join? (sequence of alphanumeric characters)")
    channel = input()
    channel = re.sub(r"\W+", "", channel)

    if (channel == ""):
        raise Exception("Empty string is not a valid channel")

    print ("What port would you like to use?")
    port = int(input())

    user = User(port, ip, numip, channel, numip + "-" + str(port))
    return user

# Update file list and user.key to show that it now has 'filename'
def addfile(user, filename):
    assert(isinstance(user, User))
    assert(isinstance(filename, str))

    try:
        filename = filename.replace(".", ",")
        data = {}
        data[user.key] = True
        db.child(user.channel).child(filename).update(data)
    except:
        return

# Get all files on the channel with the condition that some host on the server has that file
def getfiles(user):
    assert(isinstance(user, User))

    try:
        files = db.child(user.channel).get()
        nfiles = []
        for f in files.each():
            x = False
            ips = f.val()
            
            for i in ips:
                if (ips[i] == True):
                    x = True
            
            if (x):
                nfiles.append(f.key().replace(",", "."))
        
        return nfiles
    except:
        return []


# Get all ips that have 'filename'
def getips(user, filename):
    assert(isinstance(user, User))
    assert(isinstance(filename, str))
    
    try:
        filename = filename.replace(".", ",")
        ips = db.child(user.channel).child(filename).get()
        nips = []
        for i in ips.each():
            if (i.val() == True):
                key = i.key()
                key = key.split("-")
                assert(len(key) == 2)
                key = (str(ipaddress.IPv4Address(int(key[0]))), int(key[1]))
                nips.append(key)
        return nips
    except:
        return []

# Discontinue offering the file for 'user' (run this when the user goes offline, or deletes a file)
def discontinuefile(user, filename):
    assert(isinstance(user, User))
    assert(isinstance(filename, str))

    try:
        filename = filename.replace(".", ",")
        data = {}
        data[user.key] = False
        db.child(user.channel).child(filename).update(data)
    except:
        return

# Inform database that an ip no longer has a file (expect IP in 192.???.???.??? form)
def informdb(user, key, filename):
    assert(isinstance(user, User))
    assert(len(key) == 2)
    assert(isinstance(filename, str))
    
    try:
        filename = filename.replace(".", ",")
        ip = key[0]
        port = key[1]
        numip = str(int(ipaddress.IPv4Address(ip)))

        data = {}
        data[numip + "-" + str(port)] = False
        db.child(user.channel).child(filename).update(data)
    except:
        return