# hamlib
A peer-2-peer network that allows others to instantly share files accross their channels

MVP is getting peers to be able to send and receive files using firebase to host metadata for a single channel

Written with Python 3.8.2
But it worked with Python 3.6.8 on Xinu machine

We had to pip install these modules when testing on xinu machines:
    python3 pip install wheel
    python3 pip install firebase
    python3 pip install python-jwt
    python3 pip install PyCryptodome
    python3 pip install requests
    python3 pip install requests-toolbelt
    python3 pip install gcloud
    python3 pip install sseclient

Then to run the actual program type:
    python3 init.py