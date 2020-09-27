from network_controller.poxcontroller import PoxController

if __name__ == '__main__':
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
