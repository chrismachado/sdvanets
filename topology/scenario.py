#!/usr/bin/python

"""Sample file for SUMO

***Requirements***:

sumo 1.1.0
sumo-gui"""

from mininet.node import Controller, RemoteController
from mininet.log import info
from mn_wifi.node import UserAP
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.sumo.runner import sumo
from mn_wifi.link import wmediumd, mesh
from mn_wifi.wmediumdConnector import interference


def topology(ncars):
    "Create a network."
    net = Mininet_wifi(controller=RemoteController, accessPoint=UserAP,
                       link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes: car\n")
    cars = []
    for id in range(0, ncars):
        cars.append(net.addCar('car%s' % (id + 1), wlans=2, encrypt='wpa2,'))

    info("*** Creating nodes: rsu\n")
    rsus = []
    for id in range(0, 4):
        rsus.append(net.addCar('rsu%s' % (id + 1), wlans=2, encrypt='wpa2,'))

    info("*** Creating nodes: controller\n")
    c1 = net.addController(name='c1', ip='127.0.0.1', port=6633, protocol='tcp')

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=4.5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Adding link\n")
    net.addLink(rsus[0], rsus[1])
    net.addLink(rsus[2], rsus[3])

    for rsu in rsus:
        net.addLink(rsu, intf=rsu.params['wlan'][1],
                    cls=mesh, ssid='mesh-ssid', channel=5)

    for car in cars:
        net.addLink(car, intf=car.params['wlan'][1],
                    cls=mesh, ssid='mesh-ssid', channel=5)

    info("*** Starting sumo")
    # change config_file name if you want
    # use --random for active the probability attribute of sumo
    net.useExternalProgram(program=sumo, port=8813,
                           config_file='map.sumocfg --random')

    info("*** Starting network\n")
    net.build()
    c1.start()

    for rsu in rsus:
        rsu.setIP('192.168.0.%s/24' % (int(rsus.index(rsu)) + 101),
                  intf='%s-wlan0' % rsu)
        rsu.setIP('192.168.1.%s/24' % (int(rsus.index(rsu)) + 101),
                  intf='%s-mp1' % rsu)

    poss = ['215.35,300.51,0.0', '300.81,206.09,0.0', '408.97,304.93,0.0', '519.27,206.09,0.0']
    for rsu, pos in zip(rsus, poss):
        rsu.setPosition(pos=pos)

    for car in cars:
        car.setIP('192.168.0.%s/24' % (int(cars.index(car)) + 1),
                  intf='%s-wlan0' % car)
        car.setIP('192.168.1.%s/24' % (int(cars.index(car)) + 1),
                  intf='%s-mp1' % car)

    info("*** Starting telemetry\n")
    # Track the position of the nodes
    nodes = net.cars + net.aps
    net.telemetry(nodes=nodes, data_type='position',
                 min_x=0, min_y=0,
                 max_x=850, max_y=650)

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()
