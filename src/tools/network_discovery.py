import scapy.all as scapy

class NetworkDiscovery:
    def __init__(self, target_ip_range="192.168.1.0/24"):
        self.target_ip_range = target_ip_range

    def scan(self):
        """Scans the network for active hosts."""
        arp_request = scapy.ARP(pdst=self.target_ip_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

        devices = []
        for element in answered_list:
            device_info = {
                "ip": element[1].psrc,
                "mac": element[1].hwsrc
            }
            devices.append(device_info)
        return devices

    def display_devices(self, devices):
        """Displays discovered devices in a readable format."""
        print("IP\t\t\tMAC Address\n--------------------------------------")
        for device in devices:
            print(f"{device['ip']}\t\t{device['mac']}")

if __name__ == "__main__":
    discovery = NetworkDiscovery()
    devices = discovery.scan()
    discovery.display_devices(devices)
