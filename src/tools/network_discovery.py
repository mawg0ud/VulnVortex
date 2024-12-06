import logging
import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any


class NetworkDiscovery:
    """
    A sophisticated class for discovering devices in a network.

    Features:
    - Multithreaded IP discovery for scalability.
    - Service and device type identification using banners and reverse DNS.
    - Customizable timeout and thread settings.
    - Detailed logging for traceability.
    """

    def __init__(self, ip_range: str, max_threads: int = 50, timeout: int = 2):
        """
        Initialize the NetworkDiscovery instance.

        Args:
            ip_range (str): CIDR notation for the network range (e.g., '192.168.1.0/24').
            max_threads (int): Maximum number of threads for scanning.
            timeout (int): Timeout for each connection attempt in seconds.
        """
        self.ip_range = ipaddress.ip_network(ip_range, strict=False)
        self.max_threads = max_threads
        self.timeout = timeout
        self.logger = logging.getLogger("NetworkDiscovery")
        self.logger.setLevel(logging.INFO)

    def discover(self) -> List[Dict[str, Any]]:
        """
        Discover active devices within the specified IP range.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing discovered device details.
        """
        self.logger.info(f"Starting network discovery for range: {self.ip_range}")
        devices = []

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = {executor.submit(self._scan_ip, str(ip)): ip for ip in self.ip_range}

            for future in as_completed(futures):
                result = future.result()
                if result:
                    devices.append(result)

        self.logger.info(f"Discovery complete. Found {len(devices)} devices.")
        return devices

    def _scan_ip(self, ip: str) -> Dict[str, Any]:
        """
        Scan a single IP address for activity and details.

        Args:
            ip (str): The IP address to scan.

        Returns:
            Dict[str, Any]: Details of the device if active, otherwise None.
        """
        self.logger.debug(f"Scanning IP: {ip}")
        device_info = {
            "ip": ip,
            "hostname": None,
            "open_ports": [],
        }

        # Ping check
        if not self._is_host_alive(ip):
            self.logger.debug(f"IP {ip} is not responding to ping.")
            return None

        # Fetch hostname
        device_info["hostname"] = self._resolve_hostname(ip)

        # Scan common ports
        device_info["open_ports"] = self._scan_common_ports(ip)

        self.logger.info(f"Discovered device: {device_info}")
        return device_info

    def _is_host_alive(self, ip: str) -> bool:
        """
        Check if a host is alive using a ping method.

        Args:
            ip (str): The IP address to check.

        Returns:
            bool: True if the host responds, False otherwise.
        """
        try:
            socket.create_connection((ip, 80), timeout=self.timeout).close()
            return True
        except (socket.timeout, socket.error):
            return False

    def _resolve_hostname(self, ip: str) -> str:
        """
        Resolve the hostname of an IP address.

        Args:
            ip (str): The IP address to resolve.

        Returns:
            str: The hostname or None if not resolvable.
        """
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            self.logger.debug(f"Resolved hostname for {ip}: {hostname}")
            return hostname
        except socket.herror:
            self.logger.debug(f"Unable to resolve hostname for {ip}.")
            return None

    def _scan_common_ports(self, ip: str) -> List[int]:
        """
        Scan a set of common ports for the given IP.

        Args:
            ip (str): The IP address to scan.

        Returns:
            List[int]: A list of open ports.
        """
        common_ports = [22, 80, 443, 445, 3389]
        open_ports = []

        for port in common_ports:
            if self._is_port_open(ip, port):
                self.logger.debug(f"Port {port} is open on {ip}.")
                open_ports.append(port)

        return open_ports

    def _is_port_open(self, ip: str, port: int) -> bool:
        """
        Check if a specific port is open on the given IP.

        Args:
            ip (str): The IP address to check.
            port (int): The port to check.

        Returns:
            bool: True if the port is open, False otherwise.
        """
        try:
            with socket.create_connection((ip, port), timeout=self.timeout):
                return True
        except (socket.timeout, socket.error):
            return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Example: Discover devices on the local network
    ip_range = "192.168.1.0/24"
    discovery = NetworkDiscovery(ip_range, max_threads=100, timeout=2)

    devices = discovery.discover()

    for device in devices:
        print(f"IP: {device['ip']}, Hostname: {device['hostname']}, Open Ports: {device['open_ports']}")
