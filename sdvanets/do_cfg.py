import os

DIR_MN = 'mininet-wifi'
ABS_PATH = os.path.abspath('')
MN_WIFI_PATH = os.path.abspath(f'../{DIR_MN}/')

__FILES_TO = 'map.sumocfg net.net.xml reroute.add.xml route.rou.xml'


def do_change_sumo_files(dir_opt):
    print('Changing files sumo...')
    try:
        print(f'Removing all sumo files from {MN_WIFI_PATH}/mn_wifi/sumo/data/')
        os.system(f'cd {MN_WIFI_PATH}/mn_wifi/sumo/data/ && rm -f -v {__FILES_TO}')

        print('Copying sumo files...')
        os.system(f'cd {ABS_PATH}/sumo_files/{dir_opt}/ && cp -v {__FILES_TO} {MN_WIFI_PATH}/mn_wifi/sumo/data/')

    except PermissionError:
        raise PermissionError('Try run again as superuser.')


def do_make():
    print('Doing mininet make install ...')
    try:
        os.system(f'cd {MN_WIFI_PATH} && make install')
    except PermissionError:
        raise PermissionError('Try run again as superuser.')


def do_mn_c():
    try:
        os.system('mn -c')
    except PermissionError:
        raise PermissionError('Try run again as superuser.')


def do_pox():
    try:
        from network_controller.poxcontroller import PoxController

        pox = PoxController(cmd='/home/ubuntu/pox/pox.py',
                            script='forwarding.l3_learning',
                            ofst='openflow.spanning_tree --no-flood --hold-down',
                            debug='log.level --DEBUG',
                            pretty_log='samples.pretty_log',
                            ofdc='openflow.discovery host_tracker info.packet_dump',
                            ofport='openflow.of_01 --port=6653',
                            log='log --file=/home/ubuntu/SDVANETS/log_files/pox.log'
                            )
        pox.run()
    except PermissionError:
        raise PermissionError('Try run again as superuser.')


def do_scenario():
    try:
        import subprocess
        pox = subprocess.Popen('gnome-terminal -- python topology/scenario.py',
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True)

        out, err = pox.communicate()
    except PermissionError:
        raise PermissionError('Try run again as superuser.')
