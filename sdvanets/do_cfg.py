import os

DIR_MN = 'mininet-wifi'
DIR_POX = 'pox'
ABS_PATH = os.path.abspath('')
MN_WIFI_PATH = os.path.abspath('../%s/' % DIR_MN)
POX_PATH = os.path.abspath('../%s/' % DIR_POX)

ALL_PATHS = [ABS_PATH, MN_WIFI_PATH, POX_PATH]

__FILES_TO = 'map.sumocfg net.net.xml reroute.add.xml route.rou.xml file.settings.xml'


def do_change_sumo_files(dir_opt):
    if not os.path.exists('%s/sumo_files/%s/' % (ABS_PATH, dir_opt)):
        raise FileNotFoundError('Try with valid option.')

    print('Changing files sumo...')
    try:
        print('Removing all sumo files from %s/mn_wifi/sumo/data/' % MN_WIFI_PATH)
        os.system('cd %s/mn_wifi/sumo/data/ && rm -f -v %s' % (MN_WIFI_PATH, MN_WIFI_PATH))
        print('Copying sumo files...')
        os.system('cd %s/sumo_files/%s/ && cp -v %s %s/mn_wifi/sumo/data/'
                  % (ABS_PATH, dir_opt, __FILES_TO, MN_WIFI_PATH))

    except PermissionError:
        raise PermissionError('Try run again as superuser.')


def do_make():
    print('Doing mininet make install ...')
    try:
        os.system('cd %s && make install' % MN_WIFI_PATH)
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

        pox = PoxController(cmd='%s/pox.py' % POX_PATH,
                            script='forwarding.l3_learning',
                            ofst='openflow.spanning_tree --no-flood --hold-down',
                            debug='log.level --DEBUG',
                            pretty_log='samples.pretty_log',
                            ofdc='openflow.discovery host_tracker info.packet_dump',
                            ofport='openflow.of_01 --port=6653',
                            log='log --file=%s/log_files/pox.log' % ABS_PATH
                            )
        pox.run()
    except PermissionError:
        raise PermissionError('Try run again as superuser.')


def do_scenario(scenario='topology/minimal_scenario.py'):
    try:
        import subprocess
        pox = subprocess.Popen('gnome-terminal -- python %s' % scenario,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True)

        out, err = pox.communicate()
    except PermissionError:
        raise PermissionError('Try run again as superuser.')

    except FileNotFoundError:
        raise FileNotFoundError('Could not found your scenario: {%s}' % scenario)


def does_paths_exists():
    exists = os.path.exists(ABS_PATH)
    exists &= os.path.exists(MN_WIFI_PATH)
    exists &= os.path.exists(POX_PATH)

    return exists
