#!/usr/bin/python3

from puresnmp import get
import ipaddress
import sys
import json
import os

CMMAC = sys.argv[1].lower()
cmtses = []

def returnDecMAC(CMMAC):
	rtnMAC = []
	tmpMAC = CMMAC.split(":")
	for t in tmpMAC:
		rtnMAC.append(str(int(t,16)))
	return ".".join(rtnMAC)


## Some globalDefs

TEMPLATE_DIR = '/opt/CM-RT-GRAPH/telegraf/rtPoller/templates/'
CMTS_JSON = 'cmts.json'
TELEGRAF_CONFIG_DIR = '/etc/telegraf/telegraf.d/'
CMTS_TEMPLATE = ("%stmp.cmts.conf" % (TEMPLATE_DIR))
CM_TEMPLATE = ("%stmp.cm.conf" % (TEMPLATE_DIR))


with open("%s%s" % (TEMPLATE_DIR,CMTS_JSON), 'r') as f:
    cmtses = json.load(f)


DECMAC = returnDecMAC(CMMAC)
PTR_OID = ("1.3.6.1.2.1.10.127.1.3.7.1.2.%s" % (DECMAC))


for cmts in cmtses:
	ptr = None
	try:
		ptr = get(cmts['hostname'],cmts['community'],PTR_OID,cmts['port'])
	except:
		print("No such OID on CMTS:",cmts['hostname'],"proceed to the next one!")
		continue

	if ptr is not None:
		CM_IP_OID = ("1.3.6.1.2.1.10.127.1.3.3.1.3.%s" % (ptr))
		CMIP = get(cmts['hostname'],cmts['community'],CM_IP_OID,cmts['port'])
		CMIP = str(ipaddress.IPv4Address(CMIP))

		TMP_CM = open(CM_TEMPLATE,"r")
		CM_TELEGRAF_FILE = ("%stmp.cm.%s.conf" % (TELEGRAF_CONFIG_DIR,CMMAC))
		TELE_CM = open(CM_TELEGRAF_FILE,"w")
		for line in TMP_CM:
			if 'CM_IP' in line:
				line = line.replace('CM_IP',CMIP)
			elif 'CM_COMMUNITY' in line:
				line = line.replace('CM_COMMUNITY',cmts['cmCommunity'])
			elif 'CM_HEX_MAC' in line:
				line = line.replace('CM_HEX_MAC',CMMAC)
			TELE_CM.write(line)

		TMP_CMTS = open(CMTS_TEMPLATE,"r")
		CMTS_TELEGRAF_FILE = ("%stmp.cmts.%s.conf" % (TELEGRAF_CONFIG_DIR,CMMAC))
		TELE_CMTS = open(CMTS_TELEGRAF_FILE,"w")
		for line in TMP_CMTS:
			if 'CMTS_HOSTNAME' in line:
				line = line.replace('CMTS_HOSTNAME',cmts['hostname'])
			if 'PORT' in line:
				line = line.replace('PORT',cmts['port'])
			if 'CMTS_COMMUNITY' in line:
				line = line.replace('CMTS_COMMUNITY',cmts['community'])
			if 'CM_HEX_MAC' in line:
				line = line.replace('CM_HEX_MAC',CMMAC)
			if 'PTR' in line:
				line = line.replace('PTR',str(ptr))
			TELE_CMTS.write(line)
		os.system("service telegraf reload")
