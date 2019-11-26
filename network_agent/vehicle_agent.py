# coding: utf-8

import scapy.all
import os
import time
import uuid

from scapy.all import conf
from scapy.all import AsyncSniffer, sniff, send, sendp, sr1, sr, srp1
from scapy.layers.inet import Ether, IP, UDP, ICMP
from time import sleep
from random import randint, random
from threading import Thread, Lock
from datetime import datetime
from math import sqrt

from enum import IntEnum


class Statistic(IntEnum):
    CNC = 1
    DSN = 4  # max number of car neighbors
    CNG = 50  # max number of packets received
    MIN_DSN = 50  #
    MED_DSN = 100


class VehicleAgent(object):
    def __init__(self):
        self.start_tx_time = 2  # sec
        self.tx_port = 2570  # connection port to send broadcast messages
        self.rx_port = 7025  # connection port to receive broadcast messages
        self.ifaces_names = []  # Interfaces with yours ip address
        self.ifaces_ip = []  # Ip of interfaces
        self.tx_delay = 5  # s
        self.ifaces_dict = dict()
        self.broadcast_addresses = None
        self.receiver_packets = 0  # Count how many packets were received
        self.monitor_threads = None
        self.neighbors = []
        self.neighbors_timeout = dict()
        self.network_status = []
        self.broadcast_count = 30

    def start_agent(self):
        self.get_ifaces_config()  # set iface and ifaces_ip values
        self.mount_broadcast_address()  # make all broadcast addresses

        while True:
            sleep_time = randint(3, 5) - self.start_tx_time
            print("Waiting for %d sec before transmitting" % sleep_time)
            sleep(sleep_time)
            threads = []
            for fnc in (self.broadcast, self.assync_monitoring):
                process = Thread(target=fnc)
                process.start()
                threads.append(process)

            for process in threads:
                process.join(timeout=3)

            # Time for receive packets
            sleep(randint(3, 5))
            for process in self.monitor_threads:
                # process.join(timeout=5) # if you specify how many packets do you want to collect use this
                result = process.stop()
                self.network_status.append(process.results)
                self.receiver_packets += len(process.results)
                # print(result)
                if result is not None:
                    for raw_packet in result:
                        if raw_packet[IP].src not in self.ifaces_ip:
                            # raw_packet.show()
                            if raw_packet[Ether].src not in self.neighbors:
                                # print("New neighbor added %s" % raw_packet[Ether].src)
                                self.add_neighbor(raw_packet[Ether].src)  # MAC Address
                            print(self.ifaces_names[0].split('-')[0], end='\t')  # My Address
                            print(raw_packet[IP].src, end='\t')  # IP Address
                            print()
                            # print(raw_packet[ICMP].load)  # Data
            self.network_status = []

            for neighbor in self.neighbors:
                process = Thread(target=self.update_neighbor, args=[neighbor])
                process.start()

            self.verify_density()

            self.receiver_packets = 0

    def get_ifaces_config(self):
        _routes = conf.route.routes  # getting ifaces config

        for _r in _routes:
            if _r[4] != '127.0.0.1':
                if _r[3] not in self.ifaces_names:
                    self.ifaces_names.append(_r[3])
                    self.ifaces_ip.append(_r[4])
                    self.ifaces_dict.update([(self.ifaces_names[-1], self.ifaces_ip[-1])])

    def broadcast(self):
        for src, dst, iface in zip(self.ifaces_ip, self.broadcast_addresses, self.ifaces_names):
            # print("Sending for address %s." % address)
            # start = time.time()
            send(self.build_own_packet(src=src, dst=dst), iface=iface, count=self.broadcast_count,
                 verbose=0)
            # end = time.time() - start

    def broadcast_v2v(self):
        iface = self.ifaces_names[1]
        dst = self.broadcast_addresses[1]
        print(dst, "  -  ", iface)
        # print("Sending for address %s." % address)
        # start = time.time()
        send(self.build_own_packet(src=self.ifaces_ip[1], dst=dst), iface=iface, count=self.broadcast_count, verbose=0)
        # end = time.time() - start

    def rebroadcast(self):
        pass

    def assync_monitoring(self):
        if len(self.ifaces_names) != 0:
            print("Assynchronous monitoring start")
            self.monitor_threads = []

            for iface in self.ifaces_names:
                # print("\tInterface %s" % iface)
                monitor_process = AsyncSniffer(iface=iface, filter='icmp')
                monitor_process.start()
                self.monitor_threads.append(monitor_process)

    # def network_analyzer(self, packets):
    #     if packets is not None:
    #         return

    def mount_broadcast_address(self):
        if self.broadcast_addresses is None:
            self.broadcast_addresses = []
            if len(self.ifaces_ip) != 0:
                for ip in self.ifaces_ip:
                    separator = '.'
                    splited_ip = ip.split(separator)
                    splited_ip[3] = '255'
                    self.broadcast_addresses.append(separator.join(splited_ip))

    def build_own_packet(self, src, dst):
        # TODO montar o status de congestionamento da rede a partir de nós próximos ou muitos pacotes sendo transmitidos
        #  ao mesmo tempo
        return IP(src=src, dst=dst) / ICMP() / self.build_message()

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
        self.neighbors_timeout.update([(neighbor, randint(2, 5))])

    def update_neighbor(self, neighbor):
        try:
            while self.neighbors_timeout[neighbor] >= 1:
                # print("Process id %s" % os.getpid())
                sleep(1)
                self.neighbors_timeout[neighbor] -= 1
                # print("Neighbor %s | Timeout %d" % (neighbor, self.neighbors_timeout[neighbor]))
            self.neighbors.remove(neighbor)
            del self.neighbors_timeout[neighbor]
        except KeyError as kex:
            pass
            # print("Key %s was already removed. " % kex)

    def build_message(self):
        timestamp = datetime.timestamp(datetime.now())

        # [ID, DSN, CNG, TIMESTAMP]
        message = "{},{},{},{}".format(self.generate_message_id(timestamp=timestamp),
                                       self.density(),
                                       self.congestion(),
                                       timestamp)
        return "{%s}" % message

    @staticmethod
    def generate_message_id(timestamp):
        return uuid.uuid1()

    def connectivity(self):
        return 1

    def density(self):
        if len(self.neighbors) >= Statistic.DSN:
            return 1
        return 0

    def congestion(self):
        if self.receiver_packets >= Statistic.CNG:
            return 1
        return 0

    def verify_density(self):
        if 0 < self.receiver_packets <= Statistic.MIN_DSN:
            self.broadcast_count = 100
        elif Statistic.MIN_DSN < self.receiver_packets <= Statistic.MED_DSN:
            self.broadcast_count = 50
        elif self.receiver_packets > Statistic.MED_DSN:
            self.broadcast_count = 20
