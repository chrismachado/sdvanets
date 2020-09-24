from mininet.log import setLogLevel
from topology import scenario

import sys

# TODO: mudar o nome do arquivo e permitir que a escolha entre duas simulações

if __name__ == '__main__':
    setLogLevel('info')
    scenario.topology()



