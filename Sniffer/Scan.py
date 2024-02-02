from scapy.all import Raw, sniff, get_if_list, IP, TCP
from datetime import datetime
import os
import json


class Sniffer:
    # Sniff a certain amount of packets on your network within a specified interface
    # Only saving packets with Raw data
    def __init__(self):
        self.packet_data = {}
        self.interface = ""

    def clear_console(self):
        # clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

    def save_datas(self, filename: str, datas: dict, indent=2):
        # Save datas in a JSON file
        if os.path.exists(filename):
            with open(filename, "r") as file:
                old_datas = json.load(file)
                old_datas.update(datas)
                datas = old_datas
        elif not os.path.exists(filename) and datas == {}:
            print("\nNo datas to save !\n")
            return
        with open(filename, "w") as file:
            json.dump(datas, file, indent=indent)
        print(f"\nDatas saved successfully in {filename}\n\nSniffer exited.\n")

    def get_available_interfaces(self):
        # Print available interfaces
        available_interfaces = get_if_list()
        print(f"\nAvailable interfaces : \n\n{available_interfaces}\n")
        return available_interfaces

    def print_packet(self, packet):
        # Only print packets with Raw data
        if Raw in packet:
            print(packet.summary())

    def save_packet(self, packet, data, timestamp):
        # Save packets to a dictionary
        self.packet_data[timestamp] = {'interface': self.interface,
                                       'source_ip': packet[IP].src,
                                       'destination_ip': packet[IP].dst,
                                       'data': data,
                                       'protocol': packet[IP].proto,
                                       'source_port': packet[TCP].sport,
                                       'destination_port': packet[TCP].dport
                                       }

    def analyze_packet(self, packets):
        # Analyze packets
        for packet in packets:
            self.print_packet(packet)
            if packet.haslayer(IP) and packet.haslayer(TCP):
                payload = packet[TCP].payload
                if isinstance(payload, Raw):
                    timestamp = datetime.fromtimestamp(packet.time).strftime('%Y-%m-%d %H:%M:%S')
                    try:
                        data = payload.load.decode('utf-8', errors='ignore')
                        self.save_packet(packet, data, timestamp)
                    except UnicodeDecodeError as e:
                        print("Unicode decoding error:", e)
                else:
                    pass

    def start_sniffing(self, count: int = 10, interface: str = 'lo0'):  # 'lo0' = localhost
        # Sniffing the last 10 packets by default
        print(f"\nSniffing the network on interface ▶︎ {interface} ◀︎\n\nPress Ctrl + C to stop sniffing ..\n\n")
        self.interface = interface
        if count == "all":
            sniff(iface=interface, prn=self.analyze_packet)
        else:
            sniff(count=count, iface=interface, prn=self.analyze_packet)
