# DellPartScrape
Alex Datsko (alexdatsko@gmail.com) 12-29-22

Scrapes Dell's Configuration page for specific part numbers. Can check for a single service tag, or multiple fed, by a text file (one per line).

**NOTE: There are a ton of headers that could be subject to change over time so please tread carefully.**

Library requirements: requests,urllib3

Can be installed with: 
`pip install requests urllib3`

**Usage:**
python3 DellPartScrape.py [-h] [-s/--servicetag [SERVICETAG]] -p/--partnumber PARTNUMBER [-v/--verbose] [filename]

The following arguments are required: -p/--partnumber

**Examples:**

`python3 dellscrape.py -s 8ZCQHH2 -p 4HGTJ`

Will search the configuration page of service tag 8ZCQHH2 for Dell Part # 4HGTJ - which is a 600g SAS HDD:  HD,600G,SAS12,15K,2.5,S-VAL,EC	4

`python3 dellscrape.py servicetags.txt -p 400-AJRH`

Will search for all service tags (one per line) in servicetags.txt for Dell Part # 400-AJRH which is the assembly of : 600GB 15K RPM SAS ISE 2.5in Ho t-plug Hard Drive (including screws, etc)

`python3 dellscrape.py file.txt -p 4HGTJ --verbose`

Shows ALL raw output, etc





