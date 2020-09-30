import os

DIR_MN = 'mininet-wifi'
DIR_POX = 'pox'
ABS_PATH = os.path.abspath('')
MN_WIFI_PATH = os.path.abspath(f'../{DIR_MN}/')
POX_PATH = os.path.abspath(f'../{DIR_POX}/')

ALL_PATHS = [ABS_PATH, MN_WIFI_PATH, POX_PATH]

__FILES_TO = 'map.sumocfg net.net.xml reroute.add.xml route.rou.xml file.settings.xml'


def do_change_sumo_files(dir_opt):
    """
    Change the current files from mininet's sumo directory to the files in the specified directory
    :param dir_opt: One of the folder inside sumo_files
    :return: None
    """
    if not os.path.exists(f'{ABS_PATH}/sumo_files/{dir_opt}/'):
        raise FileNotFoundError('Try with valid option.')

    print('Changing files sumo...')
    try:
        print(f'Removing all sumo files from {MN_WIFI_PATH}/mn_wifi/sumo/data/')
        os.system(f'cd {MN_WIFI_PATH}/mn_wifi/sumo/data/ && rm -f -v {__FILES_TO}')

        print('Copying sumo files...')
        os.system(f'cd {ABS_PATH}/sumo_files/{dir_opt}/ && cp -v {__FILES_TO} {MN_WIFI_PATH}/mn_wifi/sumo/data/')

    except PermissionError:
        raise PermissionError('Try run again as superuser.')


def do_make():
    """
    Run the mininet wifi's make install command
    :return: None
    """
    print('Doing mininet make install ...')
    try:
        os.system(f'cd {MN_WIFI_PATH} && make install')
    except PermissionError:
        raise PermissionError('Try run again as superuser.')


def do_mn_c():
    """
    Run the mininet's mn -c command.
    :return: None
    """
    try:
        os.system('mn -c')
    except PermissionError:
        raise PermissionError('Try run again as superuser.')


def do_pox():
    """
    Run the pox controller.
    :return: None
    """
    try:
        from network_controller.poxcontroller import PoxController

        pox = PoxController(cmd=f'{POX_PATH}/pox.py',
                            script='forwarding.l3_learning',
                            ofst='openflow.spanning_tree --no-flood --hold-down',
                            debug='log.level --DEBUG',
                            pretty_log='samples.pretty_log',
                            ofdc='openflow.discovery host_tracker info.packet_dump',
                            ofport='openflow.of_01 --port=6653',
                            log=f'log --file={ABS_PATH}/log_files/pox.log'
                            )
        pox.run()
    except PermissionError:
        raise PermissionError('Try run again as superuser.')


def do_scenario(scenario_path='topology/minimal_scenario.py'):
    """
    Run the selected scenario.
    :param scenario_path: path to scenario python file
    :return: None
    """
    try:
        import subprocess
        pox = subprocess.Popen(f'gnome-terminal -- python {scenario_path}',
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True)

        out, err = pox.communicate()
    except PermissionError:
        raise PermissionError('Try run again as superuser.')

    except FileNotFoundError:
        raise FileNotFoundError(f'Could not found your scenario: {scenario_path}')


def does_paths_exists():
    """
    Verify if all path exists.
    :return: bool
    """
    exists = os.path.exists(ABS_PATH)
    exists &= os.path.exists(MN_WIFI_PATH)
    exists &= os.path.exists(POX_PATH)

    return exists
