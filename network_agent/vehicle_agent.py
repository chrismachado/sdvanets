# coding: utf-8
import scapy.all
import time
import logging
import os

from scapy.all import conf
from scapy.all import AsyncSniffer, send
from scapy.layers.inet import Ether, IP, ICMP
from time import sleep
from random import randint
from threading import Thread
from enum import IntEnum
from network_log.logger import Logging
from utils.subnetutils import SubnetUtils


class Statistic(IntEnum):
    # CNC = 1
    DSN = 8  # max number of car neighbors
    CNG = 120  # max number of packets received
    MIN_DSN = 50  #
    MED_DSN = 100


class VehicleAgent:

    def __init__(self, **kwargs):
        if 'args' not in kwargs:
            raise ValueError('Args need to be specified. Use -h for help.')
        self.args = kwargs.pop('args')
        self.log = None  # Logger class
        self.start_tx_time = 2  # sec
        self.ifaces_names = []  # Interfaces with yours ip address
        self.ifaces_ip = []  # Ip of interfaces
        self.ifaces_netmask = []
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
        """
        Start the agent and his functionalities
        :return: VehicleAgent
        """
        self.get_ifaces_config()  # set iface and ifaces_ip values
        self.mount_broadcast_address()  # make all broadcast addresses
        self.config_log_features()

        iteration_count = 0
        try:
            self.log.log("Entered the simulation", 'info', self.args['m'])

            while True:
                # if self.car.params['position']:
                #     self.log.log("Current car position %s " % self.car.params['position'], 'info', self.args['d'])
                sleep_time = randint(3, 5) - self.start_tx_time
                sleep(sleep_time)  # wait time to transmit
                threads = []
                for fnc in (self.broadcast, self.async_monitoring):
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
                                self.rebroadcast(packet=raw_packet)
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

                # self.receiver_packets = 0
                iteration_count += 1
        except (KeyboardInterrupt, SystemExit):
            self.log.log("Leave the simulation", 'info', self.args['m'])
        except Exception as e:
            self.log.log("VehicleAgent stops by unknown error\n%s" % e, 'error', self.args['e'])
        finally:
            exit(0)

        return self

    def get_ifaces_config(self):
        """
        configure ifaces per name, ip and makes a dict.
        :return: self.ifaces_dict
        """
        _routes = conf.route.routes  # getting ifaces config
        for _r in _routes:
            if _r[4] != '127.0.0.1':
                if _r[3] not in self.ifaces_names and _r[1] != 0:
                    self.ifaces_names.append(_r[3])
                    self.ifaces_ip.append(_r[4])
                    self.ifaces_netmask.append(SubnetUtils(netmask=int(_r[1])).int_to_dotted_string())
                    self.ifaces_dict.update([(self.ifaces_names[-1], (self.ifaces_ip[-1], self.ifaces_netmask[-1]))])
        return self.ifaces_dict

    def broadcast(self):
        """
        Send broadcast message to each network
        :return: packets[]
        """
        packets = []
        for src, dst, iface in zip(self.ifaces_ip, self.broadcast_addresses, self.ifaces_names):
            self.log.log("Sending into iface: %s." % iface, 'info', self.args['s'])
            packets.append(self.build_own_packet(src=src, dst=dst))
            send(packets[-1], iface=iface, count=len(self.neighbors) + 1,
                 verbose=0)

        return packets

    def rebroadcast(self, packet):
        """
        Rebroadcast received message from other vehicles (we can implement a lot of things here)
        :param packet: Message received from other vehicles
        :return: packet
        """
        msg = "Device %s rebroadcast packet data %s " % (self.ifaces_names[0].split('-')[0], packet[ICMP].load)
        self.log.log(msg, 'info', True)
        send(packet, count=len(self.neighbors) + 1, verbose=1)
        return packet

    def async_monitoring(self):
        """
        Start threads for each interface that will sniff all packets incoming to the network
        :return: self.monitor_threads
        """
        if len(self.ifaces_names) != 0:
            self.monitor_threads = []
            for name, ip in zip(self.ifaces_names, self.ifaces_ip):
                monitor_process = AsyncSniffer(iface=name, filter='icmp and not host %s' % ip)
                monitor_process.start()
                self.monitor_threads.append(monitor_process)

    def mount_broadcast_address(self):
        """
        Configure network broadcast address for each interface
        :return: self.broadcast_addresses
        """
        if self.broadcast_addresses is None:
            self.broadcast_addresses = []
            if len(self.ifaces_ip) != 0:
                for ip in self.ifaces_ip:
                    separator = '.'
                    split_ip = ip.split(separator)
                    split_ip[3] = '255'
                    self.broadcast_addresses.append(separator.join(split_ip))

        return self.broadcast_addresses

    def build_own_packet(self, src, dst):
        """
        Creates packet to be sent in the network.
        :param src: source address
        :param dst: destination address
        :return: packet with layer 3, 4 and the message -> IP / ICMP / Message.
        """
        return IP(src=src, dst=dst) / ICMP() / self.build_message()

    def add_neighbor(self, neighbor):
        """
        Add neighbor to the list of neighbors and define timeout for it.
        :param neighbor: neighbor's mac address
        :return: self.neighbors
        """
        self.neighbors.append(neighbor)
        self.neighbors_timeout.update([(neighbor, randint(8, 12))])
        self.log.log("Neighbors %d." % len(self.neighbors), 'info', self.args['n'])
        return self.neighbors

    def update_neighbor(self, neighbor):
        """
        Update list of neighbor by the time of each neighbor have.
        :param neighbor: neighbor's mac address
        :return: self.neighbors_timeout
        """
        try:
            while self.neighbors_timeout[neighbor] >= 1:
                sleep(1)  # wait 1 second
                self.neighbors_timeout[neighbor] -= 1
            self.neighbors.remove(neighbor)
            self.neighbors_timeout.pop(neighbor)
        except KeyError as kex:
            self.log.log("Key %s was already removed. " % kex, 'warn')
        finally:
            return self.neighbors_timeout

    def runtime_packets_log(self, packet):
        """
        Store into the log file the runtime packet content
        :param packet: Packet from other vehicle, a build packet message
        :return: content of the packet
        """
        icmp_load = packet[ICMP].load
        if icmp_load in self.runtime_packets:
            self.runtime_packets[icmp_load] += 1
        else:
            self.runtime_packets[icmp_load] = 1
            self.log.log('new update message received %s' % icmp_load, 'info', self.args['r'])

        return icmp_load

    def config_log_features(self):
        """
        Configure log class with parameters.
        :return: self.log
        """
        filename = self.args['filename']
        store_log_hour = self.args['filetime']

        if filename is None:
            filename = 'default-log-name'

        if store_log_hour is not None:
            filename = '%s%s' % (filename, time.strftime(store_log_hour))
        path = self.args['path']
        if path is None:
            path = "%s/log_files/" % os.getcwd()
        self.log = Logging(path=path, filename='%s.log' % filename,
                           log=self.args['log'])  # setup log file location
        self.log.config_log(logger_name=filename)

        return self.log

    def build_message(self):
        """
        Create message by using the id, flags and timestamp.
        :return: string
        """
        timestamp = time.time()
        # [ID, DSN, CNG, TIMESTAMP]
        message = "{},{},{},{}".format(self.generate_message_id(),
                                       # self.file_utils.read_pos(),
                                       'position',
                                       len(self.neighbors),
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
