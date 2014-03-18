#!/usr/bin/python

import os, sys, commands, dmidecode, platform;
from SimpleXMLRPCServer import SimpleXMLRPCServer;

#def delete_log_file():
#    global log_file;
#    if os.path.exists(log_file):
#       os.remove(log_file);

def getIPAddress():
    """This function currently works for Linux hosts only.
       This function uses /sbin/ifconfig to get first IP available on the host.
       For example, if the host is using two IP addresses 192.168.1.2 and 192.168.122.2 then this function returns 192.168.1.2
       If no IP address is found, then string "localhost" will be returned."""

    ipaddr = "";
    if platform.system() == 'Linux':
       ipaddr = commands.getoutput("for ip in $(/sbin/ifconfig | grep -A 4 Ethernet | awk '/inet/ {print $2}' | sed -e s/addr://); do echo $ip; done");
       if ipaddr:
          # Replace \n character by space character, if more then one IP address exist
          # For example, ipaddr = '192.168.1.2\n192.168.122.1', if the host uses two IPs.
          ipaddr = ipaddr.replace('\n', ' ');

          # Assumption: We use only first IP for this vorphost python daemon. So we neglect other IP(s), if any
          ipaddr = ipaddr.split()[0];
       else: ipaddr = "localhost";   # localhost is default
    elif platform.system() == 'Windows': pass;
    return ipaddr;

# Function to return host information that is extracted by reading SMBIOS using python dmidecode module
def getHostInfo():
  for val in dmidecode.system().values():
      if type(val) == dict and val['dmi_type'] == 1:
         return {
                  "Platform" : platform.system(),
                  "OS Information" : platform.uname(),
                  "Host IP In Use By vorphost Daemon" : getIPAddress(),
                  "Manufacturer" : val['data']['Manufacturer'],
                  "Product Name" : val['data']['Product Name'],
                  "Serial Number" : val['data']['Serial Number'],
                  "Version" : val['data']['Version'],
                  "UUID" : val['data']['UUID'],
                  "Wake-Up Type" : val['data']['Wake-Up Type'],
                  "SKU Number" : val['data']['SKU Number'],
                  "Family" : val['data']['Family'],
               };
 
def createServer():
    ipaddr = getIPAddress();
    port_number = 8010;

    hostInfoServer = SimpleXMLRPCServer((ipaddr, port_number), logRequests = True);
    hostInfoServer.register_function(getHostInfo);
    hostInfoServer.serve_forever();
    print "Please use URL http://" + ipaddr + "/:" + port_number + " to access vorphost daemon !\n";

# Start program from here
log_file = "/var/log/vorphost_log_file.txt";
if __name__ == "__main__":
    if os.geteuid() != 0:
       exit("\nSTOP: You need to have root privileges to run this script.\nPlease use \'sudo\' if required, and try again!\n");

    # Register atexit function
    #import atexit;
    #atexit.register(delete_log_file);

    # Create a new log file everytime
    file = open(log_file, "w");
    file.close();

    try:
        import daemon;
        daemon.make_daemon(stdout = log_file, stderr = log_file);
        createServer();
        #print getHostInfo();
    except ImportError:
        print "ERROR: Importing daemon failed !";
        sys.exit(1);
    except KeyboardInterrupt:
        print "ERROR: KeyboardInterrupt is caught !";
        sys.exit(1);


