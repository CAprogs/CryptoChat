"""                     _             _           _
   ___ _ __ _   _ _ __ | |_ ___   ___| |__   __ _| |_
  / __| '__| | | | '_ \| __/ _ \ / __| '_ \ / _` | __|
 | (__| |  | |_| | |_) | || (_) | (__| | | | (_| | |_
  \___|_|   \__, | .__/ \__\___/ \___|_| |_|\__,_|\__| Sniffer
            |___/|_|

by @CAprogs (https://github.com/CAprogs)
"""


from Sniffer.Scan import Sniffer
import os


if __name__ == '__main__':

    sniffer = Sniffer()

    try:
        sniffer.clear_console()

        print("\nSniffer's ready ...\n")
        interfaces = sniffer.get_available_interfaces()

        sniffed_interface = input("Choose an interface [ Press ENTER to use localhost ] ▶︎ ")

        if sniffed_interface == "":
            sniffed_interface = "lo0" if os.name != "nt" else "lo"
        elif sniffed_interface not in interfaces:
            print(f"\nInterface {sniffed_interface} not found !\n\nSniffer exited.\n")
            exit()

        packets_to_sniff = input("Number of packets to sniff [ Press ENTER to sniff all packets ] ▶︎ ")

        if packets_to_sniff == "":
            packets_to_sniff = "all"
        elif isinstance(packets_to_sniff, str):
            try:
                packets_to_sniff = int(packets_to_sniff)
            except ValueError:
                print("\nInvalid number of packets !\n\nSniffer exited !\n")
                exit()

        sniffer.start_sniffing(count=packets_to_sniff, interface=sniffed_interface)

        sniffer.save_datas("sniffed_datas.json", sniffer.packet_data)

    except KeyboardInterrupt:
        print("\n\nSniffer exited.\n")
