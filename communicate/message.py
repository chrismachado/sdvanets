
from scapy.layers.inet import IP, ICMP
from scapy.all import send

class Message(object):

    def __init__(self, data, ip_src, ip_dst):
        self.data = data
        self.ip = IP(src=ip_src, dst=ip_dst)
        self.msg = self.ip/ICMP/self.data

    def send_msg(self, count=1):
        send(self.msg, count=count)





