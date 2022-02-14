##################### 
#
#    Author: Bahadir (Baho) Parmaksiz
#       
#    Q: What does this script do?
#    A: It gets all valid DNS records in any .zone File and puts it in a .csv File
#       so you can see all DNS records in a tabular view or use it in another script.
#       Preferably use Excel to view the data. 
#    
#    Q: How to use this script?
#    A: First of all, you need Python 3+.
#       Then you copy all zone files into a folder. 
#       Then copy this script into the same folder and run it. 
#       You will get a "zones.csv" and a "output.txt" file.
#       The latter is for debugging reasons. "zones.csv" is the one you need.
#       Then do whatever you want with the csv data.
#       
#    LICENSED UNDER: 
#       MIT License
#       
#       Copyright (c) 2021 Bahadir Parmaksiz
#       
#       Permission is hereby granted, free of charge, to any person obtaining a copy
#       of this software and associated documentation files (the "Software"), to deal
#       in the Software without restriction, including without limitation the rights
#       to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#       copies of the Software, and to permit persons to whom the Software is
#       furnished to do so, subject to the following conditions:
#       
#       The above copyright notice and this permission notice shall be included in all
#       copies or substantial portions of the Software.
#       
#       THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#       IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#       FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#       AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#       LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#       OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#       SOFTWARE.
#
######################

import glob
import os
import re
import csv
from typing import Sequence

##### !!! Baho's RegEx Magic !!!
dnsmatchrule1 = "^(?!\;)(@|(?:[A-Za-z0-9*\-\_\@\.])+\.?)\s*([0-9MmSsHhDdWw]{0,6})?\s*(IN|CH|HS|CS)?\s+(NS\s+(?:[A-Za-z0-9*\-\_\@\.])+\.|A\s+\\b(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.?){3}(?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9]))\\b|MX\s+(?:[0-9]){0,3}\s+(?:[A-Za-z0-9*\-\_\@\.])+\.|CNAME\s+(?:[A-Za-z0-9*\-\_\@\.])+\.?|TXT\s+(?:\"?.*\"?)|AAAA\s+\\b(?:(?:[0-9a-f]){0,4}:?){0,7}(?:(?:[0-9a-f]){0,4})\\b|SRV\s*(?:[0-9]){0,6}\s*(?:[0-9]){0,6}\s*(?:[0-9]){0,6}\s*(?:[A-Za-z0-9*\-\_\@\.])+\.?|SOA\s*(?:[A-Za-z0-9*\-\_\@\.])+\.?\s*(?:[A-Za-z0-9*\-\_\@\.])+\.?\s*\([\s0-9]*\))"
#####
rx_seq = re.compile(dnsmatchrule1, re.MULTILINE) 

logfile = open("output.txt", "w")

zonefiles = glob.glob("./*.zone") # get all zonefiles in current directory

csvfile = open("zones.csv","w", newline='')
csvzonewriter = csv.writer(csvfile, delimiter=";")

    #############################
    ## CSV Headers definition:
    ## DNS Zone
    ## Group  1 Name
    ## Group  2 TTL
    ## Group  3 Class
    ## Group  4 Type
    ## Group  5 Priority
    ## Group  6 Weight
    ## Group  7 Port
    ## Group  8 TXT Value
    ## Group  9 Destination
    ## Group 10 Primary Master
    ## Group 11 Mail Address
    ## Group 12 Serial
    ## Group 13 Refresh
    ## Group 14 Retry
    ## Group 15 Expire
    ## Group 16 Negative Caching
    #############################

csvzonewriter.writerow(["DNS Zone","Name","TTL","Class","Type","Priority","Weight",
                        "Port", "Destination", "TXT Value", "Primary Master", "Mail Address",
                        "Serial","Refresh","Retry", "Expire", "Negative Caching"])

logfile.write ("\nAll files:\n")
for file in zonefiles:
    logfile.write(file+"\n")

for file in zonefiles:
    filehandler = open(file, "r")
    zonecontent = filehandler.read()
    logfile.write("\nFile: "+file+"\n\nMATCHES:")

    for match in rx_seq.finditer(zonecontent):
         # extracting records and beautifying it
        _domain = file[2:-len(".zone")]
        _record = match[0].replace("\t"," ").replace("\n","").strip()
        _name = match.group(1)
        _ttl = match.group(2)
        _class = match.group(3)
        _priority = ""
        _weight = ""
        _port = ""
        _destination = ""
        _txt_value = ""
        _primary_master = ""
        _mail_address = ""
        _serial = ""
        _refresh = ""
        _retry  = ""
        _expire = ""
        _negative_caching = ""

        # Value field handling
        _valueGroup = match.group(4).replace("\t"," ").replace("\n","").strip()
        _type = _valueGroup.split()[0]
        _value = _valueGroup[len(_type):].strip()
        _splitValues = _value.split()
        
        # Getting the right properties for each type
        if _type == "SOA":
            _primary_master = _splitValues[0]
            _mail_address = _splitValues[1]
            _serial = _splitValues[3]
            _refresh = _splitValues[4]
            _retry = _splitValues[5]
            _expire = _splitValues[6]
            _negative_caching = _splitValues[7].replace(")","")
        elif _type == "CNAME":
            _destination = _value
        elif _type == "A":
            _destination = _value
        elif _type == "TXT":
            _txt_value = _value
        elif _type == "NS":
            _destination = _value
        elif _type == "AAAA":
            _destination = _value
        elif _type == "MX":
            _priority = _splitValues[0]
            _destination = _splitValues[1]
        elif _type == "SRV":
            _priority = _splitValues[0]
            _weight = _splitValues[1]
            _port = _splitValues[2]
            _destination = _splitValues[3]
        else:
            print("\n")

        csvzonewriter.writerow([_domain,_name,_ttl,_class,_type,_priority,_weight,
                                _port,_destination,_txt_value,_primary_master,_mail_address,
                                _serial,_refresh,_retry,_expire,_negative_caching])

        logfile.write("\nMatch: "+_record)

    logfile.write("\n")

