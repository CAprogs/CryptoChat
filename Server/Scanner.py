from scapy.all import sniff, IP, TCP
import json

class MyScanner:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.packet_data = []

    def packet_handler(self, packet):
        if IP in packet and TCP in packet and packet[IP].dst == self.target_ip:
            data = {
                'source_ip': packet[IP].src,
                'destination_ip': packet[IP].dst,
                'protocol': packet[IP].proto,
                'timestamp': str(packet.time),
                'source_port': packet[TCP].sport,
                'destination_port': packet[TCP].dport
            }
            self.packet_data.append(data)

    def start_sniffing(self):
        sniff(prn=self.packet_handler, store=0, filter="tcp")

    def save_results_to_json(self, filename='scan_results.json'):
        with open(filename, 'w') as file:
            json.dump(self.packet_data, file, indent=4)
        print(f"Scan results saved to {filename}")

# Exemple d'utilisation
target_ip = '192.168.1.1'
scanner = MyScanner(target_ip)
scanner.start_sniffing()
scanner.save_results_to_json()
