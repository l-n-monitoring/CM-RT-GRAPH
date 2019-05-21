#!/usr/bin/python3

from fastsnmp import snmp_poller
from puresnmp import get,bulkwalk
import sys, getopt
import socket

host = socket.gethostname()

scriptName = "cmts-fn.py"

def sysName(IP,COMMUNITY):
    OID = '1.3.6.1.2.1.1.5.0'
    res = get(IP, COMMUNITY, OID)
    return res.decode("utf-8") 



def main(argv):
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
	

   ifStack    =	"1.3.6.1.2.1.31.1.2.1.3"
   fn         = "1.3.6.1.4.1.4491.4.2.1.1.1.2"
   fnIfIndex  = "1.3.6.1.4.1.4491.4.2.1.2.1.2"

   result = bulkwalk(agent_host, community, [fn])

   for row in result:
       fnName = row.value.decode("utf-8")
       fnName = fnName.replace(' ','\ ')
       oid = ("%s" % (row.oid))
       restoid = oid.replace(fn,'')
       find = ("%s%s" % (fnIfIndex,restoid))
       findex = bulkwalk(agent_host, community, [find])

       for f in findex:
           foid = ("%s" % (f.oid))
           foid = foid.replace(find,'')
           soid = ("%s%s" % (ifStack,foid))
           sindex = bulkwalk(agent_host, community, [soid])
           for s in sindex:
               toid = soid
               toid = ("%s." % (toid))
               ioid = ("%s" % (s.oid))
               ioid = ioid.replace(toid,'')
               if ioid != '0':
                   print ("%s,agent_host=%s,host=%s,hostname=%s,ifIndex=%s,fnDescr=%s index=%s" % (mn,agent_host,host,sysName(agent_host,community),ioid,fnName,ioid))
               else:
                   foid = foid.replace('.','')
                   print ("%s,agent_host=%s,host=%s,hostname=%s,ifIndex=%s,fnDescr=%s index=%s" % (mn,agent_host,host,sysName(agent_host,community),foid,fnName,foid))

if __name__ == "__main__":
   main(sys.argv[1:])

