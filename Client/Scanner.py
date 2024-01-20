import nmap
#import scapy.all as scapy

class MyScanner:
    def __init__(self, target_ip):
        self.nm = nmap.PortScanner()
        self.target_ip = target_ip
        self.scan_result = None

    def mac_scan(self):
        try:
            self.scan_result = self.nm.scan(hosts=self.target_ip, arguments='-sn')
            
            # Check if the scan was successful
            if "scan" not in self.scan_result:
                print("Scan failed. Check your scan options and target IP range.")
                return None
            elif self.target_ip in self.nm.all_hosts():
                mac_address = self.nm[self.target_ip]['addresses']['mac']
                return mac_address
            else:
                print(f"Can't find the MAC address for {self.target_ip}")
                return None
        except Exception as e:
            print(f"Error : {e}")
            return None
