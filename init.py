# Handle the grabing of initial metadata
    # Call check metadata
# call upload functions if there are files in upload folder
# Create a list of files in upload and download folder
files = []
ips = []
upfiles= []
import client
import uploads
import os
def init():
    os.chdir("Downloads")
    for root, dirs, fil in os.walk(os.getcwd()):
        for file in fil:
            if "Metadata" in file:
                continue
            files.append(file)
    client.checkMetadata()
    os.chdir("..\\Uploads")
    for root, dirs, fil in os.walk(os.getcwd()):
        for file in fil:
            upfiles.append(file)
    uploads.massUpload()


