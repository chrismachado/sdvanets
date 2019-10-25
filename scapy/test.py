import sys
from scapy.all import sr1
from scapy.layers.inet import IP, ICMP, IPOption

p = sr1(IP(dst='192.168.0.1')/ICMP()/"[1, 0, 1]")
if p:
    p.show()
