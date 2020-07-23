# coding: utf-8
from network_agent.vehicle_agent import VehicleAgent
import argparse
import os

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
    parser.add_argument('--critical', action='store_true', help='Log critical messages')
    parser.add_argument('--path', nargs='?', const=str, help="Root path for save files")
    parser.add_argument('--no-keep', dest='keep', action='store_false',
                        help='Don\'t Keep an existent car log or car position file')
    parser.set_defaults(keep=False)

    args = parser.parse_args()
    d_args = vars(args)
    # print(d_args)

    # if not d_args['keep']:
    #     abspath = os.path.abspath('./rsc')
    #     car_pos_list = os.listdir('%s/car_pos' % abspath)
    #     for item in car_pos_list:
    #         if item.endswith('.txt'):
    #             os.remove('%s/car_pos/%s' % (abspath, item))
    #             print('Removing %s/car_pos/%s' % (abspath, item))

    va = VehicleAgent(args=d_args)
    va.start_agent()
