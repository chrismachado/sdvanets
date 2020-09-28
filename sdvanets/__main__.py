from .do_cfg import *
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="[S]oftware [D]efined [V]ehicular [A]d-hoc [NET]work.\n"
                                                 "This project contains experiments using the concept of Software "
                                                 "Defined Network and combines with the concept of Vehicular Ad-hoc "
                                                 "Network to improve the communication between the network nodes.")
    parser.add_argument('-c', action='store_true', help='Allow script to run mn -c, mininet garbage collector')
    parser.add_argument('--set-sumo', nargs='?', help='Pass the sumo scenarios to set mininet\'s sumo files')
    parser.add_argument('--mn-path', nargs='?', const=str, help="Path to mininet-wifi directory")
    parser.add_argument('--mn-dirname', nargs='?', const=str, help="Mininet-wifi directory name")
    parser.add_argument('--remote', action='store_true', help='Do this command if you do not want pox controller')

    args = parser.parse_args()
    d_args = vars(args)

    if d_args['mn_dirname']:
        print(f'Defining mininet-wifi dirname {d_args["mn_dirname"]}')
        DIR_MN = d_args['mn_dirname']

    if d_args['mn_path']:
        print(f'Defining mininet-wifi path {d_args["mn_path"]}')
        MN_WIFI_PATH = d_args['mn_path']

    if d_args['set_sumo']:
        print('Preparing mininet scenario into mininet-wifi...')
        do_change_sumo_files(dir_opt=d_args['set_sumo'])
        do_make()

    if d_args['c']:
        print('Cleaning mininet garbage...')
        do_mn_c()

    if not d_args['remote']:
        print('Running Pox Controller...')
        do_pox()

    print('Running Scenario...')
    do_scenario()
