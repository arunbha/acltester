# ACLTester

A python script to check ACL connectivity to various hosts from a MAC or Linux Machine

## How to Run this

 - Copy the file to your MAC or Linux Machines ( Windows not supported)
 - Give execute permissions (chmod +x ACLTester.py
 - Run the script - ./ACLTester.py
 - The script will print some details to the console and an output file will also be genrated in the users Home Directory


## Configuration 

Configuration is defined as a Python Object. Example given below.
The script runs each section one by one.
There is option to enable/Disable each section ( enabled = True/False )
User can edit the list to add more hosts/IP?network to test

Each list entry is defined as an aray of three
 [ "A","B", "C"]
-  A - can be the IP address or hostname or a CIDR notation of a network
-  B - Currently supports only TCP
- C - the port number to test.
 
```python
config = [
    {
        "name": "Checking Access to Server Category 1",
        "enabled": True,
        "list": [
            ['google.com', 'TCP', 80],
            ['54.239.26.128', 'TCP', 443],
            ['yahoo.com', 'TCP', 443],
        ]
    },
    {
        "name": "Checking Access to Server Category 2",
        "enabled": True,
        "list": [
            ['apple.com', 'TCP', 443],
            ['17.178.104.0/24', 'TCP', 443],
            ['17.178.101.0/25', 'TCP', 443],
        ]
    }
]
```
