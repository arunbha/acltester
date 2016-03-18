#!/usr/bin/env python
import subprocess
import os
from datetime import datetime
import cStringIO
import time

"""ACLTester.py: Script to Test the Connectivity to Servers from a Mac/Linux machine"""

__author__ = "Arun Bhakthavalsalam"
__version__ = "1.0.0"
__email__ = "arunb01@gmail.com"
__maintainer__= "Arun Bhakthavalsalam"
__status__ = "Production"


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


class ACLTester:
    def __init__(self):
        mytime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        self.path = os.path.expanduser("~/ACLTester-") + mytime + ".log"
        self.fp = open(self.path, 'ab')
        print "Starting Tests"
        self.runTests()
        print "Tests completed"
        print "Output File: %s" % self.path

    def runTests(self):
        self.runACLTests()
        self.fp.close()

    def cidrACLTest(self,incidr, type, port):
        # Get address string and CIDR string
        (addrString, cidrString) = incidr.split('/')
        # Split address into octets and turn CIDR into int
        addr = addrString.split('.')
        cidr = int(cidrString)
        # Initialize the netmask and calculate based on CIDR mask
        mask = [0, 0, 0, 0]
        for i in range(cidr):
            mask[i/8] = mask[i/8] + (1 << (7 - i % 8))
        # Initialize net and binary and netmask with addr to get network
        net = []
        for i in range(4):
            net.append(int(addr[i]) & mask[i])
        # Duplicate net into broad array, gather host bits, and generate broadcast
        broad = list(net)
        brange = 32 - cidr
        for i in range(brange):
            broad[3 - i/8] = broad[3 - i/8] + (1 << (i % 8))
        # Print information, mapping integer lists to strings for easy printing
        start = addrString
        end = ".".join(map(str, broad))
        ip2int = lambda s: reduce(lambda a, b: (a << 8) + b, map(int, s.split('.')), 0)
        int2ip = lambda n: '.'.join([str(n >> (i << 3) & 0xFF) for i in range(0, 4)[::-1]])
        startint = ip2int(start)
        endint  = ip2int(end)
        n= startint+1
        iplist = []
        output = cStringIO.StringIO()
        output.write("Testing from "+start+"  to "+end)
        if startint < endint:
            while n < endint:
                iplist.append(int2ip(n))
                n += 1
        print "\t\t\t IP  Range check : %d IPs" % len(iplist)
        i = 1
        for ip in iplist:
            print "\t\t\t checking %d of %d" %(i, len(iplist))
            i += 1
            output.write("\n\t\t\t\t"+ self.checkACL([ip, type, port]))
        contents =  output.getvalue()
        output.close()
        return contents

    def checkACL(self, entry):
        if len(entry) != 3:
            return "Incorrect Config format"
        if '/' in entry[0]:
            #CIDR Notation
            return  self.cidrACLTest(entry[0], entry[1], entry[2])
        else:
            if entry[1] == 'TCP':
                command = "nc -z -w 3 -G 2 %s %s" % (entry[0], entry[2])
            else:
                command = "nc -z -w 3 -u %s %s" % (entry[0], entry[2])
            try:
                response = subprocess.check_output(command.split(), stderr=subprocess.STDOUT)
            except:
                response = "Failed to Connect for %s %s %s\n" % (entry[0], entry[1], entry[2])
            return response[:-1]

    def runACLTests(self):
        print " Running ACL Tests for %d sections" % len(config)
        print >> self.fp, "Running ACL Tests for %d sections" % len(config)
        index=1
        for section in config:
            print "\t Section (%d of %d) Name: %s" % ( index, len(config), section['name'])
            print >> self.fp, "Section ( %d of %d ) Name: %s" % (index, len(config), section['name'])
            index +=1
            i= 1
            if section['enabled'] != True:
                print "Skipping section"
                continue
            for entry in section['list']:
                print "\t\t checking %d of %d" % ( i, len(section['list']))
                i += 1
                print >> self.fp, "\t %s %s %d - %s" % (entry[0], entry[1], entry[2], self.checkACL(entry))



if __name__ == "__main__":
    ACLTester()
