"""
This module includes a function to make a Python program as a "Daemon" process/program

"""

import os, sys;

def make_daemon(stderr = '/dev/null', stdout = '/dev/null', stdin = '/dev/null'):
    '''We use this function to create a "Daemon" process/program. This forks the current process into a daemon.
       http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012 is used as a reference code.

       If we want, we can replace standard file descriptors (sys.stdin, sys.stdout, sys.stderr). 
       Default argument to all these arguments is /dev/null. '''

    # Do the UNIX double-fork magic, see Stevens' "Advanced Programming in the UNIX Environment" for details (ISBN 0201563177)
    try: 
        pid = os.fork();
        if pid > 0:
            sys.exit(0); # Exiting from first parent.
    except OSError, e: 
        sys.stderr.write("Fork #1 failed: (%d) %s\n" % (e.errno, e.strerror));
        sys.exit(1);
 
    # Decouple from parent environment.
    os.chdir("/");
    os.umask(0);
    os.setsid(); 

    # Make second fork.
    try: 
        pid = os.fork();
        if pid > 0:
            sys.exit(0); # Exiting from second parent.
    except OSError, e: 
        sys.stderr.write ("Fork #2 failed: (%d) %s\n" % (e.errno, e.strerror));
        sys.exit(1);
 
    # Start actual daemon from here!

    # Redirect standard file descriptors.
    si = file(stdin, 'r');
    so = file(stdout, 'a+');
    se = file(stderr, 'a+', 0);
    os.dup2(si.fileno(), sys.stdin.fileno());
    os.dup2(so.fileno(), sys.stdout.fileno());
    os.dup2(se.fileno(), sys.stderr.fileno());

