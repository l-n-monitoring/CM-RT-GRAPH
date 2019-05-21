#!/usr/bin/python3

from fastsnmp import snmp_poller
from puresnmp import get,bulkwalk
import pymysql.cursors
import sys, getopt
import socket

host = socket.gethostname()

scriptName = "cmts-cmCount.py"

def sysName(IP,COMMUNITY):
    OID = '1.3.6.1.2.1.1.5.0'
    res = get(IP, COMMUNITY, OID)
    return res.decode("utf-8")

def connect():
	connection = pymysql.connect(host='localhost',
                             user='docsis',
                             password='docsis123',
                             db='docsis',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
	return connection

def disconnect(conn):
	conn.close()


def main(argv):
   ifindex = {}
   community = ''
   agent_host = ''
   mn = ''
   try:
      opts, args = getopt.getopt(argv,"hi:c:m:",["ip=","community=","measurement_name="])
   except getopt.GetoptError:
      print ('%s -i <hostname> -c <community> -m <measurement_name>' % (scriptName))
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('%s -i <hostname> -c <community> -m <measurement_name>' % (scriptName))
         sys.exit()
      elif opt in ("-i", "--ip"):
         agent_host = arg
      elif opt in ("-c", "--community"):
         community = arg
      elif opt in ("-m", "--measurement_name"):
         mn = arg

   if not agent_host or not community or not mn:
         print ('Usage: ./%s -i <hostname> -c <community> -m <measurement_name>' % (scriptName))
         sys.exit()

   hosts = [agent_host]
   hname = sysName(agent_host,community)
   #=============================
   # PSQL connect
   #=============================
   try:
   	conn = connect()
   except:
   	print ("I am unable to connect to the database")
   	sys.exit()

   cur = conn.cursor()

   query = ("select interfaces.ifindex,interfaces.ifalias,interfaces.ifdescr,interfaces.frequency,CMTS.cmts_name from CMTS,interfaces where CMTS.cmts_hostname='%s' and interfaces.cmtsid=CMTS.id and interfaces.iftype=205" % (agent_host))

   cur.execute(query)
   rows = cur.fetchall()
   for row in rows:
   	ifindex[row['ifindex']] = {'ifAlias': row['ifalias'], 'ifDescr': row['ifdescr'], 'docsIfUpChannelFrequency': row['frequency']}


   oid_group = {
                '1.3.6.1.4.1.4998.1.1.20.2.12.1.14': 'activeCMCount',
                '1.3.6.1.4.1.4998.1.1.20.2.12.1.15': 'registeredCMCount',
                '1.3.6.1.4.1.4998.1.1.20.2.12.1.13': 'totalCMCount'}

   snmp_data = snmp_poller.poller(hosts, (list(oid_group.keys()),), community)
   for d in snmp_data:
   	tmpoid = d[2].split('.')
   	tmp = int(tmpoid[1])
   	if oid_group[d[1]] not in ifindex[tmp]:
   		ifindex[tmp][oid_group[d[1]]] = int(d[3])
   	else:
   		ifindex[tmp][oid_group[d[1]]] = ifindex[tmp][oid_group[d[1]]] + int(d[3])

   for i in ifindex:
   	if len(ifindex[i]['ifAlias']) > 0:
   		print ("%s,agent_host=%s,host=%s,hostname=%s,ifIndex=%s,ifAlias=%s,ifDescr=%s,docsIfUpChannelFrequency=%s activeCMCount=%s,registeredCMCount=%s,totalCMCount=%s" % (mn,agent_host,host,hname,i,ifindex[i]['ifAlias'],ifindex[i]['ifAlias'],ifindex[i]['docsIfUpChannelFrequency'],ifindex[i]['activeCMCount'],ifindex[i]['registeredCMCount'],ifindex[i]['totalCMCount']))

if __name__ == "__main__":
   main(sys.argv[1:])
