from scapy.all import send, sniff
from random import randint
from math import exp
from enum import IntEnum


class Statistic(IntEnum):
    NEAR_VEHICLES_LIMIT = 13
    CONGESTION_TIME = 1000  # ms


class AgentUpdater(object):

    def __init__(self, ipsrc=None, ethmac=None):
        self.node_status = {'ip': ipsrc, 'mac': ethmac}
        self.near_vehicles = randint(5, 20)
        self.cng_timestamp = randint(1, 2000) * exp(self.near_vehicles)
        self.net_sniff_logs = []

    def network_updater(self):
        pass

    def network_status(self):
        return self.make_packet(1, self.cng_status(), self.dsn_status())

    def send_update_packet(self, packet, count=200):
        try:
            print("Sending")
            send(packet, count=count)
        except Exception:
            print("Unexpected error.")
            raise

    def network_sniff(self, filter, max_count=1):
        print("Sniffing")
        self.net_sniff_logs = sniff(filter=filter, count=max_count)
        for log in self.net_sniff_logs:
            print("Content of message %s" % log.load.decode("utf-8"))

    def dsn_status(self):
        if self.near_vehicles > Statistic.NEAR_VEHICLES_LIMIT:
            return 1
        else:
            return 0

    def cng_status(self):
        if self.cng_timestamp >= Statistic.CONGESTION_TIME:
            return 1
        else:
            return 0

    def make_packet(self, CNC, CNG, DSN):
        '''

        :param CNC: Connectivity status (0, 1)
        :param CNG: Congestion status (0, 1)
        :param DSN: Density status (0, 1)
        :return: string
        '''
        return "[%d,%d,%d]" % (CNC, CNG, DSN)
