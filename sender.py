from network_com.message import Message
from network_agent.agent_updater import AgentUpdater
from scapy.layers.inet import IP, ICMP


def main():
    agup = AgentUpdater(ipsrc='192.168.1.205')
    ip = IP(src=agup.node_status['ip'], dst='192.168.0.2')
    icmp = ICMP()
    msg = Message(ip=ip, icmp=icmp)

    while True:
        agup.send_update_packet(packet=msg.create_packet(netstatus=agup.network_status()))
        c = input("Do you want send more packets? Y/n\n")
        if c != 'Y':
            print("Stopping...")
            break


if __name__ == '__main__':
    main()
