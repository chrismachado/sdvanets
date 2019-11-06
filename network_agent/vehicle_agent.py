# coding: utf-8

import scapy.all
from scapy.all import conf
from scapy.all import AsyncSniffer, sniff, send, sendp
from scapy.layers.inet import IP, UDP, ICMP
from time import sleep
from random import randint, random
from threading import Thread, Lock
from datetime import datetime

import os


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
        self.receiver_packets = None
        self.monitor_threads = None
        self.neighbors = []
        self.neighbors_timeout = dict()
        self.network_status = []

    def start_agent(self):
        self.get_ifaces_config()  # set iface and ifaces_ip values
        self.mount_broadcast_address()  # make all broadcast addresses

        mutex = Lock()
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
                process.join(timeout=5)

            # Time for receive packets
            sleep(3)
            for process in self.monitor_threads:
                # process.join(timeout=5) # if you specify how many packets do you want to collect use this
                result = process.stop()
                self.network_status.append(process.results)
                print(result)
                if result is not None:
                    for raw_packet in result:
                        if raw_packet[1].src not in self.ifaces_ip:
                            # raw_packet.show()
                            if raw_packet[0].src not in self.neighbors:
                                print("New neighbor added %s" % raw_packet[0].src)
                                self.add_neighbor(raw_packet[0].src)
                            print(raw_packet[1].src, end='\t')
                            print(raw_packet[3].load)
            self.network_status = []

            for neighbor in self.neighbors:
                process = Thread(target=self.update_neighbor, args=[neighbor])
                process.start()

    def get_ifaces_config(self):
        _routes = conf.route.routes  # getting ifaces config

        for _r in _routes:
            if _r[4] != '127.0.0.1':
                if _r[3] not in self.ifaces_names:
                    self.ifaces_names.append(_r[3])
                    self.ifaces_ip.append(_r[4])
                    self.ifaces_dict.update([(self.ifaces_names[-1], self.ifaces_ip[-1])])

    def broadcast(self, count=20):
        for address in self.broadcast_addresses:
            print("Sending for address %s." % address)
            send(self.build_own_packet(dst=address), count=count)

    def rebroadcast(self):
        pass

    def assync_monitoring(self):
        if len(self.ifaces_names) != 0:
            print("Assynchronous monitoring start")
            self.monitor_threads = []

            for iface in self.ifaces_names:
                print("\tInterface %s" % iface)
                monitor_process = AsyncSniffer(iface=iface, filter='icmp')
                monitor_process.start()
                self.monitor_threads.append(monitor_process)

    def network_analyzer(self, packets):
        if packets is not None:
            return

    def mount_broadcast_address(self):
        if self.broadcast_addresses is None:
            self.broadcast_addresses = []
            if len(self.ifaces_ip) != 0:
                for ip in self.ifaces_ip:
                    separator = '.'
                    splited_ip = ip.split(separator)
                    splited_ip[3] = '255'
                    self.broadcast_addresses.append(separator.join(splited_ip))

    def build_own_packet(self, dst):
        # return IP(src=self.ifaces_ip[0], dst=dst) / UDP(sport=self.rx_port, dport=self.tx_port) / "[test message]"
        # this is for test only
        timestamp = datetime.timestamp(datetime.now())
        message = "<{},{}>".format(timestamp, '[1,0,0]')
        return IP(src=self.ifaces_ip[0], dst=dst) / ICMP() / message

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
        self.neighbors_timeout.update([(neighbor, randint(2, 5))])

    def update_neighbor(self, neighbor):
        try:
            while self.neighbors_timeout[neighbor] >= 1:
                print("Process id %s" % os.getpid())
                sleep(1)
                self.neighbors_timeout[neighbor] -= 1
                print("Neighbor %s | Timeout %d" % (neighbor, self.neighbors_timeout[neighbor]))
            self.neighbors.remove(neighbor)
            del self.neighbors_timeout[neighbor]
        except KeyError as kex:
            print("Key %s was already removed. " % kex)
