# -*- coding: utf-8 -*-


'''
This program was created with the intent to pull the current AWS IP-Ranges
JSON file and return you a list of all of the IP Prefixes for a specific 
Region based on your input. 

Created by David B. Zielinski aka "Mehetmet"

Last updated 2021-05-18
'''
import requests
import os

# Pull the latest ip-ranges JSON
url = 'https://ip-ranges.amazonaws.com/ip-ranges.json'
r = requests.get(url, allow_redirects=True)

open('ip-ranges.json', 'wb').write(r.content)


region = input("Please type the name of the AWS Region you wish to get an IP Prefix list for (ex. us-east-1)\n")
region = region.lower()

print("")

prevline1 = ""
prevline2 = ""

prefix = "ip_prefix"

with open('ip-ranges.json', 'r') as ipranges, open('allip.txt', 'w+') as allip:
    for line in ipranges.readlines():
        ec2ic = "EC2_INSTANCE_CONNECT"
        answer = '"region": "' + region + '",'
        if ec2ic in line:
            if answer in prevline1:
                if prefix in prevline2:
                    size = len(prevline2)
                    var1 = prevline2[:size - 3]
                    ipv4 = var1[20:]
                    allip.write(ipv4 + "\n")
        else:
            prevline2 = prevline1
            prevline1 = line

with open ('allip.txt', 'r') as allip2, open ('ip_prefixes.csv', 'w') as sortedprefixes:
    lines = allip2.readlines()
    newlines = list(dict.fromkeys(lines))
    newlines.sort()
    for var in newlines:
        sortedprefixes.write(var.rstrip('\n') + ',')
        
os.remove("allip.txt")    

isvalid = os.stat("ip_prefixes.csv").st_size == 0
if isvalid:
    print("Your query did not return any results.  Please verify the name of the AWS Region you entered, \"" + region + "\" exists.")
else:
    print("Thank you. A CSV file containing all IPv4 Prefixes for the AWS Region \"" + region + "\" EC2_INSTANCE_CONNECT service has been created, titled \"ip_prefixes.csv\" in the directory this script was run.")
