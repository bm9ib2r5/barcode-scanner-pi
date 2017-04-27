#!/usr/bin/python

# ver 0.01

import evdev
from evdev import InputDevice, ecodes, categorize
import logging
import netifaces
import os
import shlex
import string
import subprocess
import sys
dev = InputDevice('/dev/barcode0')

# Provided as an example taken from Centos 6 box:
scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
}

# Set DISPLAY environmental variable
os.environ["DISPLAY"] = ":0.0"

# Logfile
logging.basicConfig(filename='logs/barcodescanner-pi.log', format='%(asctime)s %(message)s', datefmt='%Y/%d/%m %H:%M:%S', level=logging.DEBUG)

# MAC / IP
hwaddrETH0 = string.replace(netifaces.ifaddresses('eth0')[netifaces.AF_LINK][0]['addr'], ":", "")
ipETH0 = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']

print "======================================="
print "CLIENT ID:      CID-" + hwaddrETH0
print "MAC:            " + hwaddrETH0
print "IP:             " + ipETH0
print "======================================="


logging.info('Started: CID-%s %s %s',hwaddrETH0, hwaddrETH0, ipETH0)
p1cmd=shlex.split('/usr/bin/pkill qupzilla')
p1 = subprocess.Popen(p1cmd)
stdout, stderr = p1.communicate()
returnCodep1 = p1.returncode
logging.info('Running command: %s / returncode: %s', p1cmd, returnCodep1)
print("Running command: " + str(p1cmd) + " / returncode: " + str(returnCodep1))

p2cmd=shlex.split('/usr/bin/qupzilla -fs --current-tab="https://www.barcodelookup.com/"')
logging.info('Running command: %s', p2cmd)
p2 = subprocess.Popen(p2cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
returnCodep2 = p2.returncode
logging.info('Running command: %s / returncode: %s', p2cmd, returnCodep2)
print("Running command: " + str(p2cmd) + " / returncode: " + str(returnCodep2))
# stdout, stderr = p2.communicate()
# p2.wait()

barcode = ""
for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        data = categorize(event) 
        if data.keystate == data.key_down:
            if data.scancode == 28:
                logging.info('Received barcode: %s', barcode)
                p3cmd=shlex.split('/usr/bin/qupzilla --current-tab="https://www.barcodelookup.com/' + barcode + '"')
                p3 = subprocess.Popen(p3cmd)
                stdout, stderr = p3.communicate()
                returnCodep3 = p3.returncode
                logging.info('Running command: %s / returncode: %s', p3cmd, returnCodep3)
                print("Running command: " + str(p3cmd) + " / returncode: " + str(returnCodep3))
                barcode = ""
	    elif data.scancode !=28:
		barcode +=str(scancodes[data.scancode])
