# hamlib
A peer-2-peer network that allows others to instantly share files across their channels

### Python Requirements
Written with Python 3.8.2.
But tested with Python 3.6 and 3.7 on Xinu machine.

### Filename Requirements
As a side note the port provided must be forwarded and ','s (commas) are not allowed in the names of files.

As per firebase specifications, filenames must be UTF-8 encoded, can be a maximum of 768 bytes, and cannot contain ., $, #, [, ], /, or ASCII control characters 0-31 or 127. You cannot use ASCII control characters in the values themselves, either.

### How to Run
We had to pip install these modules when testing on Xinu machines:
* python3 -m pip install wheel
* python3 -m pip install firebase
* python3 -m pip install python-jwt
* python3 -m pip install PyCryptodome
* python3 -m pip install requests
* python3 -m pip install requests-toolbelt
* python3 -m pip install gcloud
* python3 -m pip install sseclient

Then to run the actual program type:
* python3 init.py
