from mininet.log import setLogLevel
from topology import scenario

import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        ncars = 21 # default value
    else:
        ncars = int(sys.argv[1])
    
    setLogLevel('info')
    scenario.topology(ncars=ncars)
