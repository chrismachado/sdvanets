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
from network_log.logger import Logging
from utils.subnetutils import SubnetUtils
from .default_agent import Agent


class VehicleAgent(Agent):

    def __init__(self, name, **kwargs):
        super(VehicleAgent, self).__init__(name, **kwargs)
        self.AGENT_CODE = 0x12  # 18

    def response(self, packet):
        pass

    def request(self):
        pass
