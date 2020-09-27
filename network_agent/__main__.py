from network_agent.default_agent import Agent
from network_agent.rsu_agent import RSUAgent
from network_agent.vehicle_agent import VehicleAgent

import argparse
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Sending and monitoring messages in vehicle ad-hoc network (VANET). "
                                                 "Using flags to update the network.")
    parser.add_argument('--log', action='store_true', help='Enable log messages')
    parser.add_argument('-s', action='store_true', help='Log sent messages')
    parser.add_argument('-n', action='store_true', help='Log new neighbors')
    parser.add_argument('-r', action='store_true', help='Log received messages')
    parser.add_argument('-m', action='store_true', help='Log basic messages')
    parser.add_argument('-e', action='store_true', help='Log error messages')
    parser.add_argument('-d', action='store_true', help='Log debug messages')
    parser.add_argument('-w', action='store_true', help='Log warning messages')
    parser.add_argument('-c', action='store_true', help='Log critical messages')
    parser.add_argument('--filename', nargs='?', const=str, help="Define filename to log file")
    parser.add_argument('--filetime', nargs='?', const=str, help='Pass the time format to be appended in filename. '
                                                                 '(e.g) python -m network_agent --log --filetime %%Y '
                                                                 '--filename test this command will result in the name:'
                                                                 ' test{0}.log'.format(time.strftime('%Y')))
    parser.add_argument('--path', nargs='?', const=str, help="If you want your won root path for save log files")
    parser.add_argument('--name', nargs='?', const=str, help="Define name of agent (should be same of the car)")
    parser.add_argument('--rsu', action='store_true', help='Set the agent to be a RSU')
    parser.add_argument('--verbose', action='store_true', help='Allow the agent to send verbose messages')

    args = parser.parse_args()
    d_args = vars(args)

    if d_args.pop('rsu'):
        agent = RSUAgent(name=d_args.pop('name'), args=d_args)
    else:
        agent = VehicleAgent(name=d_args.pop('name'), args=d_args)

    agent.run()
