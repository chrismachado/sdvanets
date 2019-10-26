class Message(object):

    def __init__(self, ip=None, icmp=None):
        self.params = {'ip': ip, 'icmp': icmp}

    def create_packet(self, netstatus):
        if self.params['ip'] is not None and self.params['icmp'] is not None:
            return self.params['ip'] / self.params['icmp'] / netstatus
        else:
            print("Error to create packet packet, missing information \nIP > %x\nICMP > %x " % (
                self.params['ip'], self.params['icmp']))
            return
