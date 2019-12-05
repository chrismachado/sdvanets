# coding: utf-8

import scapy.all
import os
import time
import uuid
import logging

from scapy.all import conf
from scapy.all import AsyncSniffer, send
from scapy.layers.inet import Ether, IP, ICMP
from time import sleep
from random import randint
from threading import Thread
from datetime import datetime
from enum import IntEnum
from network_log.logger import Logging


class Statistic(IntEnum):
    # CNC = 1
    DSN = 8  # max number of car neighbors
    CNG = 120  # max number of packets received
    MIN_DSN = 50  #
    MED_DSN = 100


class VehicleAgent:

    def __init__(self, **kwargs):
        if 'args' not in kwargs:
            raise ValueError('Args need to be specified. Use -h to verify that.')
        self.args = kwargs.pop('args')
        path = self.args['path']
        if path is None:
            path = '/home/wifi/tcc/SDVANETS/rsc/'
        self.log = Logging(path=path, filename='sim-x.log',
                           log=self.args['log'])  # setup log file location
        self.start_tx_time = 2  # sec
        # self.tx_port = 2570  # connection port to send broadcast messages
        # self.rx_port = 7025  # connection port to receive broadcast messages
        self.ifaces_names = []  # Interfaces with yours ip address
        self.ifaces_ip = []  # Ip of interfaces
        self.tx_delay = 5  # transmission delay in seconds
        self.ifaces_dict = dict()
        self.broadcast_addresses = None  # Store broadcast address for each network
        self.receiver_packets = 0  # Count how many packets were received
        self.monitor_threads = None  # Store sniffer thread
        self.neighbors = []  # Store MAC of nearby cars
        self.neighbors_timeout = dict()  # Time to live for each neighbor
        self.network_status = []
        self.broadcast_count = 30  # Start number of packets to be send
        self.id = 0  # Initial ID for message
        self.DSN_FLAG = 0  # Current status of density flag
        self.CNG_FLAG = 0  # Current status of congestion flag
        self.runtime_packets = dict()  # Register the packets received during the simulation

        logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # suppress scapy warnings

    def start_agent(self):
        '''
        Start the agent and his functionalities
        :return: none
        '''
        self.get_ifaces_config()  # set iface and ifaces_ip values
        self.mount_broadcast_address()  # make all broadcast addresses
        self.log.config_log(self.ifaces_names[0].split('-')[0])
        iteration_count = 0

        try:
            self.log.log("Entered the simulation", 'info', self.args['m'])
            while True:
                sleep_time = randint(3, 5) - self.start_tx_time
                sleep(sleep_time)  # wait time to transmit
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
                    self.log.log(result, 'debug', self.args['d'])  # log the amount of received packets
                    if result is not None:
                        for raw_packet in result:
                            if raw_packet[IP].src not in self.ifaces_ip:
                                if raw_packet[Ether].src not in self.neighbors:
                                    self.log.log("New neighbor added %s" % raw_packet[Ether].src, 'info',
                                                 self.args['n'])
                                    self.add_neighbor(raw_packet[Ether].src)  # MAC Address
                                self.runtime_packets_log(packet=raw_packet)
                    msg = "Total received packets at iteration %d : %d" % (iteration_count, self.receiver_packets)
                    self.log.log(msg, 'info', flag=self.args['r'])
                self.network_status = []

                # Start timeout for neighbors
                for neighbor in self.neighbors:
                    process = Thread(target=self.update_neighbor, args=[neighbor])
                    process.start()

                # Flags updates
                for target in (self.congestion(), self.density(), self.verify_density_packets()):
                    process = Thread(target=target)
                    process.start()

                self.receiver_packets = 0
                iteration_count += 1
        except (KeyboardInterrupt, SystemExit):
            self.log.log("Leave the simulation", 'info', self.args['m'])
            exit(0)
        except Exception:
            self.log.log("VehicleAgent stops by unknown error", 'error', self.args['e'])
            exit(0)

    def get_ifaces_config(self):
        '''
        configure ifaces per name, ip and makes a dict.
        :return: none
        '''
        _routes = conf.route.routes  # getting ifaces config
        for _r in _routes:
            if _r[4] != '127.0.0.1':
                if _r[3] not in self.ifaces_names:
                    self.ifaces_names.append(_r[3])
                    self.ifaces_ip.append(_r[4])
                    self.ifaces_dict.update([(self.ifaces_names[-1], self.ifaces_ip[-1])])

    def broadcast(self):
        '''
        Send broadcast message to each network
        :return: none
        '''
        for src, dst, iface in zip(self.ifaces_ip, self.broadcast_addresses, self.ifaces_names):
            self.log.log("Sending into iface: %s." % iface, 'info', self.args['s'])
            send(self.build_own_packet(src=src, dst=dst), iface=iface, count=self.broadcast_count,
                 verbose=0)

    def rebroadcast(self):
        pass

    def assync_monitoring(self):
        '''
        Start threads for each interface that will sniff all packets incoming to the network
        :return: none
        '''
        if len(self.ifaces_names) != 0:
            self.monitor_threads = []
            for name, ip in zip(self.ifaces_names, self.ifaces_ip):
                monitor_process = AsyncSniffer(iface=name, filter='icmp and not host %s' % ip)
                monitor_process.start()
                self.monitor_threads.append(monitor_process)

    def mount_broadcast_address(self):
        '''
        Configure network broadcast address for each interface
        :return: none
        '''
        if self.broadcast_addresses is None:
            self.broadcast_addresses = []
            if len(self.ifaces_ip) != 0:
                for ip in self.ifaces_ip:
                    separator = '.'
                    splited_ip = ip.split(separator)
                    splited_ip[3] = '255'
                    self.broadcast_addresses.append(separator.join(splited_ip))

    def build_own_packet(self, src, dst):
        '''
        Creates packet to be sent in the network.
        :param src: source address
        :param dst: destination address
        :return: packet with layer 3, 4 and the message -> IP / ICMP / Message.
        '''
        return IP(src=src, dst=dst) / ICMP() / self.build_message()

    def add_neighbor(self, neighbor):
        '''
        Add neighbor to the list of neighbors and define timeout for it.
        :param neighbor: neighbor's mac address
        :return: none
        '''
        self.neighbors.append(neighbor)
        self.neighbors_timeout.update([(neighbor, randint(5, 7))])
        self.log.log("Neighbors %d." % len(self.neighbors), 'info', self.args['n'])

    def update_neighbor(self, neighbor):
        '''
        Update list of neighbor by the time of each neighbor have.
        :param neighbor: neighbor's mac address
        :return: none
        '''
        try:
            while self.neighbors_timeout[neighbor] >= 1:
                sleep(1)  # wait 1 second
                self.neighbors_timeout[neighbor] -= 1
            self.neighbors.remove(neighbor)
            self.neighbors_timeout.pop(neighbor)
        except KeyError as kex:
            pass

            # self.log.log("Key %s was already removed. " % kex, 'warn')

    def runtime_packets_log(self, packet):
        icmp_load = packet[ICMP].load
        if icmp_load in self.runtime_packets:
            self.runtime_packets[icmp_load] += 1
        else:
            self.runtime_packets[icmp_load] = 1
            self.log.log('new update message received %s' % icmp_load, 'info', self.args['r'])

    def build_message(self):
        '''
        Create message by using the id, flags and timestamp.
        :return: string
        '''
        timestamp = datetime.timestamp(datetime.now())
        # [ID, DSN, CNG, TIMESTAMP]
        message = "{},{},{},{}".format(self.generate_message_id(),
                                       self.DSN_FLAG,
                                       self.CNG_FLAG,
                                       timestamp)
        self.id += 1
        return "{%s}" % message

    def generate_message_id(self):
        return "<%s-%d>" % (self.ifaces_names[0].split('-')[0], self.id)

    def density(self):
        if len(self.neighbors) >= Statistic.DSN:
            self.DSN_FLAG = 1
        else:
            self.DSN_FLAG = 0

    def congestion(self):
        if self.receiver_packets >= Statistic.CNG:
            self.CNG_FLAG = 1
        else:
            self.CNG_FLAG = 0

    def verify_density_packets(self):
        if 0 < self.receiver_packets <= Statistic.MIN_DSN:
            self.broadcast_count = 100
        elif Statistic.MIN_DSN < self.receiver_packets <= Statistic.MED_DSN:
            self.broadcast_count = 50
        elif self.receiver_packets > Statistic.MED_DSN:
            self.broadcast_count = 20
