
import os, sys, commands, dmidecode, platform;
from SimpleXMLRPCServer import SimpleXMLRPCServer;
from xmlrpclib import Binary;

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

class VORPHServer:
    """ This is the main class VORPHServer (Virtual OR Physical Host Server).. We use only a single instance of this class.
        We use this single instance and create vorphost daemon."""

    def ping(self):
        """This function can be used to respond when called to make sure connectivity is not a problem"""
        return True;

    def raises_exception(self, msg):
        "If required, to make sure that RuntimeError is raised with the message passed in"
        raise RuntimeError(msg);

    # Function to return host information that is extracted by reading SMBIOS using python dmidecode module
    def getHostInfo(self):
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
               }

    def send_back_binary(self, bin):
        "Accepts one Binary argument, unpacks and repacks it to return it"
        data = bin.data;
        response = Binary(data);
        return response;

def createVORPHServer():
    "Function to create one instance about SimpleXMLRPCServer and one instance about VORPHServer and use"
    ipaddr = getIPAddress();
    port_number = 8010;

    print "ipaddr = %s" % ipaddr;
    hostInfoServer = SimpleXMLRPCServer((ipaddr, port_number), logRequests = True, allow_none = True);
    hostInfoServer.register_introspection_functions();
    hostInfoServer.register_multicall_functions();
    hostInfoServer.register_instance(VORPHServer())
    #hostInfoServer.register_function(self.getHostInfo);
    hostInfoServer.serve_forever();

