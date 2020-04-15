# Handle the grabing of initial metadata
    # Call check metadata
# if there are files missing in download call peers to get files
# call upload functions if there are files in upload folder
# Create a list of files in upload and download folder
files = []
ips = []
import client
import os
if __name__ == "__main__":
    os.chdir("Downloads")
    metadata = open("Metadata",'w')
    metadata.write("IPs:\nFiles:\n")
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if "Metadata" in file:
                continue
            metadata.write(file+"\n")
    client.checkMetadata()
    