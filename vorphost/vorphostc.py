#!/usr/bin/python

import xmlrpclib, sys, socket, getopt, traceback, string;

def main():
   url = None;
   verbose = False;
   try:
      options, arguments = getopt.getopt(sys.argv[1:], "hs:v", ["help", "vorphostsurl="]);
      for option, argument in options:
          if option in ("-s", "--vorphostsurl"):
             url = argument;
          elif option in ("-h", "--help"):
             #usage();
             pass;
          elif option == "-v":
             verbose = True;
          else:
             assert False, "ERROR: Unhandled Option";

      if url is None:
         raise getopt.GetoptError("ERROR: Missing URL information");
   except getopt.GetoptError as err:
      print str(err);
      #usage();
      sys.exit(2);
   except:
      traceback.print_exc();
      sys.exit(2);

   #url = 'http://192.168.122.117:9000';
   #server = xmlrpclib.ServerProxy('http://localhost:9000');
   #server = xmlrpclib.ServerProxy('http://192.168.1.2:9000');
   #server = xmlrpclib.ServerProxy('http://192.168.122.117:9000');
   vorphost_server = xmlrpclib.ServerProxy(url, encoding='ISO-8859-1', verbose = True);
   print;

   # Each method invoked on the proxy is translated into a request to the server.
   # The arguments are formatted using XML, and then POSTed to the server. The server
   # unpacks the XML and figures out what function to call based on the method name
   # invoked from the client. The arguments are passed to the function, and the return
   # value is translated back to XML to be returned to the client.
   try:
      #print server.getHostInfo();
      print "Ping: ", server.ping();
   #  #except socket.error:
   except xmlrpclib.Fault as err:
      print "ERROR: A fault occurred";
      print "Fault code: %d" % err.faultCode;
      print "Fault string: %s" % err.faultString; print;
   except xmlrpclib.ProtocolError as err:
      print "ERROR: A protocol error occurred";
      print "URL: %s" % err.url;
      print "HTTP/HTTPS headers: %s" % err.headers;
      print "Error code: %d" % err.errcode;
      print "Error message: %s" % err.errms; print;
   except Exception, err:
       # Catch possible exception, print and exit with non-zero exit code;
       #text = "Error: " + err.faultString +  ". Connection using " + url  + " Failed !";
       #print "\n\033[1;31m%s\033[1;m" % (text); print;
       print "Please Make Sure That Server Is Accessible And Try Again .."; print;
       sys.exit(2);


def main():
   url = "http://192.168.1.3:8010";
   #url = 'http://192.168.122.117:9000';
   #server = xmlrpclib.ServerProxy('http://localhost:9000');
   #server = xmlrpclib.ServerProxy('http://192.168.1.2:9000');
   #server = xmlrpclib.ServerProxy('http://192.168.122.117:9000');
   vorphost_server = xmlrpclib.ServerProxy(url);

   # Each method invoked on the proxy is translated into a request to the server.
   # The arguments are formatted using XML, and then POSTed to the server. The server
   # unpacks the XML and figures out what function to call based on the method name
   # invoked from the client. The arguments are passed to the function, and the return
   # value is translated back to XML to be returned to the client.
   try:
       print; print server.getHostInfo(); print;
       #except socket.error:
   except:
       # Catch possible exception, print and exit with non-zero exit code;
       text = "Error 111: Connection using " + url  + " Failed !";
       print "\n\033[1;31m%s\033[1;m" % (text); print;
       print "Please Make Sure That Server Is Accessible And Try Again .."; print;
       sys.exit(2);

if __name__ == "__main__":
   main();
   print; sys.exit(0);

