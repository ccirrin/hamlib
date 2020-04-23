# hamlib
A peer-2-peer network that allows others to instantly share files across their channels

Written with Python 3.8.2
But it worked with Python 3.6 and 3.7 on Xinu machine

As a side note the port provided must be forwarded

We had to pip install these modules when testing on xinu machines:
    python3 -m pip install wheel
    python3 -m pip install firebase
    python3 -m pip install python-jwt
    python3 -m pip install PyCryptodome
    python3 -m pip install requests
    python3 -m pip install requests-toolbelt
    python3 -m pip install gcloud
    python3 -m pip install sseclient

Then to run the actual program type:
    python3 init.py