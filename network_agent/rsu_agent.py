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


class RSUAgent(Agent):

    def __init__(self, name, **kwargs):
        super(RSUAgent, self).__init__(name, **kwargs)
        self.AGENT_CODE = 0x11  # 17

    def response(self, packet):
        pass

    def request(self):
        pass
