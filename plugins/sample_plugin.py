import logging
from src.core.Scanner import Scanner

class UnsecuredIoTPlugin:
    """
    Plugin to detect unsecured Internet of Things (IoT) devices.
    
    Features:
    - Identifies default credentials usage across IoT devices.
    - Detects open ports commonly used by IoT devices (e.g., 8080, 8883).
    - Analyzes metadata and banner information for vulnerabilities.
    - Suggests immediate remediation steps.
    """

    def __init__(self, scanner: Scanner):
        """
        Initializes the plugin with a Scanner instance.

        Args:
            scanner (Scanner): The primary scanner instance for network interaction.
        """
        self.scanner = scanner
        self.name = "Unsecured IoT Device Detector"
        self.logger = logging.getLogger(self.name)

    def run(self):
        """
        Execute the plugin's logic to scan for unsecured IoT devices.
        Returns a detailed report of vulnerabilities.
        """
        self.logger.info(f"Starting plugin: {self.name}")
        results = []

        # Define IoT-related ports to scan
        iot_ports = [8080, 8883, 1883, 5000, 5357]
        devices = self.scanner.discover_devices()

        for device in devices:
            self.logger.debug(f"Scanning device: {device['ip']}")
            open_ports = self.scanner.scan_ports(device['ip'], iot_ports)
            banners = self.scanner.fetch_banners(device['ip'], open_ports)

            for port, banner in banners.items():
                vulnerability = self.analyze_banner(banner)
                if vulnerability:
                    self.logger.warning(f"Potential vulnerability on {device['ip']}:{port} - {vulnerability}")
                    results.append({
                        "ip": device["ip"],
                        "port": port,
                        "vulnerability": vulnerability,
                        "remediation": self.get_remediation_steps(vulnerability),
                    })

        self.logger.info(f"Plugin completed. {len(results)} vulnerabilities identified.")
        return results

    def analyze_banner(self, banner: str) -> str:
        """
        Analyze the service banner for potential vulnerabilities.

        Args:
            banner (str): The service banner to analyze.

        Returns:
            str: A description of the vulnerability if found; None otherwise.
        """
        if "default credentials" in banner.lower():
            return "Device uses default credentials."
        if "outdated firmware" in banner.lower():
            return "Device is running outdated firmware."
        if "open management interface" in banner.lower():
            return "Unprotected management interface accessible."

        return None

    def get_remediation_steps(self, vulnerability: str) -> list:
        """
        Provide remediation steps based on the identified vulnerability.

        Args:
            vulnerability (str): The identified vulnerability.

        Returns:
            list: A list of recommended remediation actions.
        """
        if "default credentials" in vulnerability:
            return [
                "Change the default username and password immediately.",
                "Enable two-factor authentication if supported.",
            ]
        if "outdated firmware" in vulnerability:
            return [
                "Update the device firmware to the latest version.",
                "Enable automatic firmware updates if supported.",
            ]
        if "unprotected management interface" in vulnerability:
            return [
                "Restrict access to the management interface using a firewall.",
                "Enable HTTPS and disable unencrypted HTTP access.",
            ]

        return ["Consult the device's security documentation for further steps."]

# Sample execution when integrated with VulnVortex
if __name__ == "__main__":
    from src.utils.ConfigManager import ConfigManager
    from src.core.Scanner import Scanner

    config_manager = ConfigManager()
    scanner = Scanner(config_manager.config)
    plugin = UnsecuredIoTPlugin(scanner)

    vulnerabilities = plugin.run()
    for vuln in vulnerabilities:
        print(f"IP: {vuln['ip']}, Port: {vuln['port']}, Vulnerability: {vuln['vulnerability']}")
        print(f"Recommended Actions: {', '.join(vuln['remediation'])}")

class SamplePlugin:
    def __init__(self, scanner):
        self.scanner = scanner

    def run(self):
        """Run the plugin's main function to check for open RDP ports."""
        rdp_port = 3389
        for host in self.scanner.scan_hosts():
            if self.scanner.is_port_open(host, rdp_port):
                self.scanner.alert_manager.send_alert(f"Open RDP port detected on {host}")

def initialize(scanner):
    """Initialize the plugin with the scanner instance."""
    return SamplePlugin(scanner)
