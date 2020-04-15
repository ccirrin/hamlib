import os
import init
def checkMetadata():
    # get the metadata from firebase and check if there are any new files
    #fmeta = firebase()
    # for line in fmeta:
    #     if "Files:" in line:
    #         break
    metadata = open('metadata','r')
    for line in metadata:
        init.ips.append(line.rstrip("\n"))
        if "Files:" in line:
            break
    for line in metadata:
        templine = line.rstrip("\n")
        # if file match do nothing
        if templine in init.files:
            continue
        # if a file is not found call requestFile from a random user in IP list
        else
            requestFile(templine)


# requestFile()
    # choose a random peer thats online and try to download a file from them
    # switch after 20 seconds