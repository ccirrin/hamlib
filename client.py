import os

def checkMetadata():
    # get the metadata from firebase and check if there are any new files
    #fmeta = firebase()
    # for line in fmeta:
    #     if "Files:" in line:
    #         break
    metadata = open('metadata','r')
    for line in metadata:
        if "Files:" in line:
            break

    # if file match add to the downloads array

    # if a file is not found call requestFile from a random user in lists
# requestFile()
    # choose a random peer thats online and try to download a file from them
    # switch after 20 seconds