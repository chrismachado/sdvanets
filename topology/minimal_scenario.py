#!/usr/bin/python

"""Sample file for SUMO

***Requirements***:

sumo 1.1.0
sumo-gui"""

from mininet.node import RemoteController
from mininet.log import info
from mn_wifi.node import UserAP
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.sumo.runner import sumo
from mn_wifi.link import wmediumd, mesh
from mn_wifi.wmediumdConnector import interference


def topology():
    "Create a network."
    net = Mininet_wifi(controller=RemoteController, accessPoint=UserAP,
                       link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes: car\n")
    cars = []
    for id in range(0, 8):
        cars.append(net.addCar('car%s' % (id + 1), wlans=2, encrypt='wpa2,'))

    info("*** Creating nodes: rsu\n")
    rsus = []
    for id in range(0, 3):
        rsus.append(net.addCar('rsu%s' % (id + 1), wlans=2, encrypt='wpa2,'))

    info("*** Creating nodes: controller\n")
    c1 = net.addController(name='c1', ip='127.0.0.1', port=6653, protocol='tcp')

    poss = ['100.00,100.00,0.0', '250.00,100.00,0.0', '400.00,100.00,0.0']
    e1 = net.addAccessPoint('e1', ssid='vanet-ssid', mac='00:00:00:11:00:01',
                            mode='g', channel='1', passwd='123456789a',
                            encrypt='wpa2', position=poss[0])
    e2 = net.addAccessPoint('e2', ssid='vanet-ssid', mac='00:00:00:11:00:02',
                            mode='g', channel='6', passwd='123456789a',
                            encrypt='wpa2', position=poss[1])
    e3 = net.addAccessPoint('e3', ssid='vanet-ssid', mac='00:00:00:11:00:03',
                            mode='g', channel='1', passwd='123456789a',
                            encrypt='wpa2', position=poss[2])

    info("*** Configuring Propagation Model\n")
    net.setPropagationModel(model="logDistance", exp=3.8)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Adding link\n")
    net.addLink(rsus[0], rsus[1])
    net.addLink(rsus[1], rsus[2])

    net.addLink(e1, e2)
    net.addLink(e2, e3)

    for rsu in rsus:
        net.addLink(rsu, intf=rsu.wintfs[1].name,
                    cls=mesh, ssid='mesh-ssid', channel=5)

    for car in cars:
        net.addLink(car, intf=car.wintfs[1].name,
                    cls=mesh, ssid='mesh-ssid', channel=5)

    info("*** Starting sumo\n")
    # change config_file name if you want
    # use --random for active the probability attribute of sumo
    net.useExternalProgram(program=sumo, port=8813,
                           # config_file='map.sumocfg',
                           extra_params=["--start --delay 1000"],
                           clients=1, exec_order=0
                           )

    info("*** Starting network\n")
    net.build()
    c1.start()
    e1.start([c1])
    e2.start([c1])
    e3.start([c1])

    for rsu in rsus:
        rsu.setIP('192.168.0.%s/24' % (int(rsus.index(rsu)) + 101),
                  intf='%s-wlan0' % rsu)
        rsu.setIP('192.168.1.%s/24' % (int(rsus.index(rsu)) + 101),
                  intf='%s-mp1' % rsu)

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
                  max_x=650, max_y=650)

    info("*** Starting agents\n")
    for car in net.cars:
        if car.name in [rsu.name for rsu in rsus]:
            car.cmd('xterm -e python3 -m network_agent '
                    '--log -srnm --filename %s --name=%s --verbose --rsu &' % (car, car))
        else:
            car.cmd('xterm -e python3 -m network_agent --name=%s -srmn --verbose &' % car)

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()


if __name__ == '__main__':
    from mininet.log import setLogLevel

    setLogLevel('info')
    topology()
