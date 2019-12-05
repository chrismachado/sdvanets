from network_agent.vehicle_agent import VehicleAgent
import argparse
import sys

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
    parser.add_argument('--path', nargs='?', const=str)

    args = parser.parse_args()
    d_args = vars(args)
    # print(d_args)

    VehicleAgent(args=d_args).start_agent()
