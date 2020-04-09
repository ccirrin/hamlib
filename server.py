# sendFile()
    # Handle sending a file from downloads to a requester

# listen()
    # create a socket that handles listening for connections from other peers
    # if a peer asks for a file 
        # Check if we have a file
            # if so call sendFile
        # if no file found
            # send nothing found