from scapy.layers.inet import IP, ICMP, Ether

class Message(object):
    def __init__(data):
        self.data = data
        