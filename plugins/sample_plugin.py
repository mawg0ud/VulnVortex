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