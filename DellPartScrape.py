#!/usr/bin/python3

import requests
import argparse
import os

# THIS IS ONLY NEEDED IF YOUR NETWORK SECURITY INJECTS A SELF-SIGNED SSL CERT FOR SSL INSPECTION ETC !!
from urllib3.exceptions import InsecureRequestWarning
# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
# -------------------

# DellPartScrape - search for Dell components on a list of servers by their service tags, by text file (one per line) or command line args
# 12-29-22 Alex Datsko alexdatsko@gmail.com

parser = argparse.ArgumentParser(
                    prog = 'DellPartScrape',
                    description = 'Scrapes dell.com/support Configuration page for a list of service tags, searches each one for a specific Dell part # in the output',
                    epilog = '')
parser.add_argument('filename', help='filename of service tags to check')                         # positional argument, optional
parser.add_argument('-s', '--servicetag', help='Service Tag of single Dell system to check')      # check for single service tag
parser.add_argument('-p', '--partnumber', help='Part number to check for')                        # check for this part number
parser.add_argument('-v', '--verbose',                                                            # verbose output flag
                    action='store_true')  # on/off flag
args = parser.parse_args()
#print(args.filename, args.count, args.verbose)

checkforthis=args.partnumber
servicetag=args.servicetag
verbose=args.verbose
filename=args.filename

#print(f"\n\ncheck: {checkforthis}\nservicetag: {servicetag}\nverbose: {verbose}\nfilename: {filename}\n")

initialurl1="https://www.dell.com/support/ips/en-us/Product/Contents?Name=overview&Lob=PowerEdge&IsProductRoute=false&Tag="
initialurl2="&DiagScanCommand=null&ProductCode=poweredge-t440&TypeOfProduct=3&_=1672271454515"
configurl1="https://www.dell.com/support/components/dashboard/en-us/Configuration/GetConfiguration?serviceTag="
configurl2="&showCurrentConfig=false&showOriginalConfig=True&_=1672271454518"
headers = {
'Cookie': 'eSupId=SID=3a0431d1-2636-405e-8325-2d1db9a9230b&ld=20230628; lwp=c=us&l=en&cs=04&s=bsd; DellCEMSession=577B40310F215DF56AED47F71643717A; akGD="country":"US", "region":"CA"; AKA_A2=A; akavpau_maintenance_vp=1672271879~id=993cc91f260b26c8a09a1c6286638da8; _abck=EA9C986CF97E4DD3996B97E7AF719CAA~0~YAAQnfTVFzsf1zaFAQAADmMlWwkgBV8zq+him6137QiY4Mq7V0Z7gAi/pfVx+Oxe8JUCS3x6q238ReMgHp+rm/2wFGKsrapatrt+nqVYqELfA4tPPV0n0mLDitZaNCmEiVj021u/WF55tS/Nm4j6NAuyNRmkLdNsot667r1sZwgnQw4mnzpU+9RSdBxcT1YStp0Fr9oTyv596wFmBsY00pCUee2dRavW1X/TfQDdLdlBkeodbQP6PHzxIAnXxW169zDQuEj/msLKadfc0MeqjsAN37JxCPsW2XVQDVfZRiSeQHnljjVuuPabUJnY7UAdu8crm1ydPrMsqstGZwvqyAwyUcehLpOXDOQiwEZY8VPE1G4cHqjc0Yzt12Fbk3mDRyEG79MS51ZhUAyzvv/bXD//Uw0H2og=~-1~-1~-1; ak_bmsc=1A8CBFEAC162F668694FD188E704217F~000000000000000000000000000000~YAAQqfTVF1B541SFAQAAItoSWxLoiMIvcxR99U90psxikGMKx1F822yPujYsUgzCqUN8980weGC2khVyhi4fRrCjWdrqxHMBkuwc63b/cKzLVwOQdaKiLFJfklhUaB3d7iRKI+Ud4IiNq/KfNBjjmU8m7LGN2Yazdiqus3wqNV4ni1Yjd3IKMzBIrXU1jGLt9/eP496MnEkDi4QYDv2wa+vYkN7SG6+uQG/Drq28dEsPfnrXNcuYr0wU5ZtDL5/Zv+8Gv3uCTHlWyvtsei7lwtAGpMTxWSth64wwLiP96CIk9xd3LnCmUD8AYWjSxI9b96w6V1PbzfWEn9npaUxCYRPXWcmkh1Wm8dcXIDqZU8vtQ2IQ91MKv462hxM3Wkt4wQOVcnTBx1i0ilxDTJJMzDg5Ufk87LgV8THuO+w+3sQsZ/dM7pbdeTKGMRB2SHLkoEz2LFQOeCuk8z//I1FSsmZZSsUvAb8jSowz55QPDD5DU/LpXNd9xds=; bm_sz=D0F2E41E10792BDD35E72A5206975D54~YAAQqfTVF1d441SFAQAAitYSWxKEcHp8OhPYT45cO4jWy8iCdMAvT79OCRkw1RgSmIi947m8budYg4nnGtDjQJvkJpTtAIdb0j3lZrLBsGyZ5/6aohzyxr1kr0hiXS16YABfkC+7uA/ClsFCpXriS8cR8PWt2kNbjKJfhKFTEwsMJegwOdQ1fFpDmNAv6N1QszjDU01c/Kp4G+CrksGhUkvOQp8Mx9StmLQB5CCm9KFUuWCLOTrurt9ba87cTF2QMEvOjJlB+nMJ8INKt4/b9VycJmnuTZVs3J7AFq/bgMzj~4473395~3682372; AMCV_4DD80861515CAB990A490D45%40AdobeOrg=1585540135%7CMCIDTS%7C19355%7CMCMID%7C43385616343822480135049372302249681323%7CMCAID%7CNONE%7CvVersion%7C4.4.0; dais-c=9dphbC5OzAb9/BqDJj8tcHBjwzgrLTM84gl23a4BFEEYiRP403qTvkuWp3fllbtgUDqDlUaFyOauI5kz3QA5LA==; bm_sv=18A14A8298C844E904B3BEA34C325465~YAAQFi0+F/tSM1WFAQAAvYwnWxLjNSvUb3vqSBPZ+JavKVT+LZDJorD31z6zEoLkFRoUaSVxy0okiOjFeYH5ZlgXev0MR9eXB5tgAu3mP+pfR6mA/elemIE30fU2KXz2xq51b7rGDfZmJn0UNcU2uPJXkCNWOnSSaEz1ZjuQ8XZKxUPRJ8XlGmj0q6lBE2Jpkp0ycaRBtd5ZhkqpPzvLp7GRMgpJEy6im04JrzmrcVoXYJeW+29ZIPMRrmm+hKnz~1; s_c49=c%3Dus%26l%3Den%26s%3Dbsd%26cs%3D04%26servicetag%3D3q2fg73%26systemid%3Dpoweredge-t440; gpv_pn=us%7Cen%7C04%7Cbsd%7Cesupport-productsupport%7Cproduct-support%7Cservicetag; s_ips=1315; s_tp=1657; cidlid=%3A%3A; s_vnc365=1703806240215%26vn%3D1; s_ivc=true; s_cc=true; __privaci_cookie_consent_uuid=ff13584c-02f8-40cd-bf87-09b70806717a:33; __privaci_cookie_consent_generated=ff13584c-02f8-40cd-bf87-09b70806717a:33; __privaci_cookie_no_action=no-action-consent; _cls_v=e6736444-ab46-4a8c-b3c1-71d7efca5744; _cls_s=4a1fba82-2726-466f-9da1-c6ed9b65ecd1:0; ipe_s=190f3676-0ac8-8440-eae6-de87cd12269d; VOCAAS_SESSION_ID=35F52DCBD21C423AB5DF9077704440DE; VOCAAS_STICKY_SESSION=3156244618F6DAA4E0E8D4D21C950F1B; s_sq=dellglobalonlinemaster%3D%2526c.%2526a.%2526activitymap.%2526page%253Dus%25257Cen%25257C04%25257Cbsd%25257Cesupport-productsupport%25257Cproduct-support%25257Cservicetag%2526link%253DView%252520product%252520specs%2526region%253Doverview-quicklink-1%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dus%25257Cen%25257C04%25257Cbsd%25257Cesupport-productsupport%25257Cproduct-support%25257Cservicetag%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.dell.com%25252Fsupport%25252Fhome%25252Fen-us%25252Fproduct-support%25252Fservicetag%25252F3Q2FG73%25252Foverview%252523%2526ot%253DA; OLRProduct=OLRProduct=3Q2FG73|; s_depth=6; check=true; mbox=session#5e2357a60311424ca7cfa8f9ccab54b0#1672273183; rumCki=false; s_dl=1; s_channelstack=%5B%5B%27Direct%2520Load%27%2C%271672271322776%27%5D%5D; sessionTime=2022%2C11%2C28%2C15%2C48%2C42%2C777; s_hwp=uscorp1%7C%7Cnull%7C%7C28%3A12%3A2022%3A15%3A48%7C%7CN%7C%7CN%7C%7Cnull%7C%7C0%7C%7Cnull%7C%7Cnull%7C%7CN%7C%7Cnull%7C%7Cnull%7C%7Cnull; dell_consent_map=139%7C140; _cs_mk=0.031225217517169668_1672271324640; _gcl_au=1.1.746875260.1672271325; s_ppv=us%257Cen%257C04%257Cbsd%257Cesupport-productsupport%257Cproduct-support%257Cservicetag%2C79%2C79%2C1315%2C1%2C1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
'Accept': '*/*',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate',
'Referer': 'https://www.dell.com/support/home/en-us/product-support/servicetag/3Q2FG73/overview',
'X-Requested-With': 'XMLHttpRequest',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'same-origin',
'Te': 'trailers'}

if not servicetag:
  if not filename:
    filename="servicetags.txt"
  if not os.path.isfile(filename):
    print("[!] Error: Filename servicetags.txt doesn't exist and no other file or service tag was specified. Exiting..")
    exit()
  f=open(filename,'r')
  servicetags=[line for line in f.readlines()]
  f.close()
  print("[.] Service tags read from file servicetags.txt ..")
  if verbose:
    print(f"[.] Service tags: {servicetags}")
else:
  servicetags=[servicetag]

for servicetag in servicetags:
  r=""
  print(f"[.] Checking service tag {servicetag}",end='')  # end='' because looks like servicetag has a \n at the end
  url = initialurl1+servicetag+initialurl2
  r = requests.get(url, headers=headers, verify=False)
  if r.status_code != 200:
    print(f"[!] ERROR: URL: {r.url}\nCode: {r.status_code}")
  if verbose:
    for key,val in r.headers.items():
      print(key,':',val)
    print(f"{r.text}\n\n\n\n")
  servicetagEnc=r.text.split('ServiceStore/IntegratedEStore?serviceTag=')[1].split("', '")[0]

  r2=""
  configurl=configurl1+servicetagEnc+configurl2
  r2 = requests.get(configurl, headers=headers, verify=False)
  if r2.status_code != 200:
    print(f"[!] ERROR: URL: {r2.url}\nCode: {r2.status_code}")
  if verbose:
    for key,val in r2.headers.items():
      print(key,':',val)
    print(f"{r2.text}\n\n")
  if checkforthis in r2.text:
    print(f"  [+] HIT: {checkforthis} found on {servicetag}")
