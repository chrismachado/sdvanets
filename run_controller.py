from network_controller.poxcontroller import PoxController
import os

ABS_PATH = os.path.abspath('')
POX_PATH = os.path.abspath(f'../pox')
LOG_NAME = 'pox'

if __name__ == '__main__':
    pox = PoxController(cmd=f'{POX_PATH}/pox.py',
                        script='forwarding.l3_learning',
                        ofst='openflow.spanning_tree --no-flood --hold-down',
                        debug='log.level --DEBUG',
                        pretty_log='samples.pretty_log',
                        ofdc='openflow.discovery host_tracker info.packet_dump',
                        ofport='openflow.of_01 --port=6653',
                        log=f'log --file={ABS_PATH}/log_files/{LOG_NAME}.log'
                        )
    pox.run()
