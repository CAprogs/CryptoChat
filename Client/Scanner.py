from scapy.all import Raw, sniff, get_if_list, IP, TCP
from datetime import datetime


class Sniffer:
    # This class is used to sniff the network and save the results to a JSON file
    def __init__(self):
        self.packet_data = []

    def get_available_interfaces(self):
        # Print available interfaces
        available_interfaces = get_if_list()
        print(f"\nAvailable interfaces : \n{available_interfaces}\n")

    def print_packet(self, packet):
        # Only print packets with Raw data
        if Raw in packet:
            print(packet.summary())

    def save_packet(self, packet, data, timestamp):
        # Save packets to a dictionary
        self.packet_data.append({
            'source_ip': packet[IP].src,
            'destination_ip': packet[IP].dst,
            'data': data,
            'protocol': packet[IP].proto,
            'timestamp': timestamp,
            'source_port': packet[TCP].sport,
            'destination_port': packet[TCP].dport,
            })

    def analyze_packet(self, packets):
        # Analyze packets
        for packet in packets:
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
        # Start sniffing the network (sniffing the last 10 packets by default)
        if count == "all":
            sniff(iface=interface, prn=self.analyze_packet)
        else:
            sniff(count=count, iface=interface, prn=self.analyze_packet)
        print(f"\nSession terminated !\n{self.packet_data}")  # replace with a saving function


'''
# Uncomment this to test !
if __name__ == '__main__':

    # Initialize the sniffer
    sniffer = Sniffer()

    try:
        print("\nSniffing the network ...\n")
        sniffer.start_sniffing(count=10)
    except KeyboardInterrupt:
        print(f"\nSession terminated !\n{sniffer.packet_data}")
'''
